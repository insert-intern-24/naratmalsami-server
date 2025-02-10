from services.ai_services import find_foreign
from models.ai_model import TextData

def foreign_test(data: TextData):
    return find_foreign(data)