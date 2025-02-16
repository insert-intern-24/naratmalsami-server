from hashids import Hashids
from app.config import settings

hashids = Hashids(salt=settings.hashids_salt, min_length=settings.hashids_min_length)

def encode_id(id: int) -> str:
    return hashids.encode(id)
