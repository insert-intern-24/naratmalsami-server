from app.schemas.file import File
from datetime import datetime
from typing import List
import uuid

def create_file() -> File:
    file_id = str(uuid.uuid4())
    file_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    file = File(
        id=file_id, 
        title=None, 
        content=None, 
        datetime=file_datetime
    )
    
    return file

def file_list() -> List[File]:
    
    return [
        File(
            id='test_id',
            title='test_title',
            content='test_content',
            datetime='test_datetime'
        ),
        File(
            id='test_id2',
            title='test_title2',
            content='test_content2',
            datetime='test_datetime2'
        )
    ]