from app.services.ai import find_foreign
from app.schemas.ai import TextData

def find_foreign_controller(data: TextData):
    return find_foreign(data)