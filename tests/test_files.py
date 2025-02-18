import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# 테스트용 in-memory SQLite 데이터베이스 URL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# 하나의 엔진을 생성 (check_same_thread=False 필요)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 엔진을 이용해 테이블을 생성 (scope=session)
@pytest.fixture(scope="session")
def _engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()

# 각 테스트마다 새로운 연결과 트랜잭션을 생성하여 세션을 반환
@pytest.fixture(scope="function")
def db_session(_engine):
    connection = _engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

# get_db 의존성을 테스트용 세션으로 오버라이드 (자동 적용)
@pytest.fixture(autouse=True)
def override_get_db(db_session):
    def _get_db_override():
        yield db_session
    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides[get_db] = get_db

client = TestClient(app)

def test_create_file():
    payload = {
        "title": "파일 제목",
        "content": "본문",
        "created_at": "2025-02-08T13:47:00"  # ISO 8601
    }
    response = client.post("/files/", json=payload)
    assert response.status_code == 200, f"Response status: {response.status_code}"
    data = response.json()
    # 응답에 필요한 키들이 모두 있는지 확인합니다.
    assert "id" in data
    assert "hashed_id" in data
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert "created_at" in data
    assert "updated_at" in data

def test_read_files():
    # 먼저 테스트용 파일 생성
    payload = {
        "title": "테스트 파일",
        "content": "테스트 본문",
        "created_at": "2025-02-08T13:47:00"
    }
    client.post("/files/", json=payload)
    # 파일 목록 조회
    response = client.get("/files/")
    assert response.status_code == 200
    data = response.json()
    # 반환된 데이터가 리스트이고, 적어도 하나의 파일이 있는지 확인합니다.
    assert isinstance(data, list)
    assert len(data) > 0
