from services.ai_services import find_foreign
from models.ai_model import TextData

def find_foreign_controller(data: TextData):
    return find_foreign(data)