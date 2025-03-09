from app.schemas.ai import TextData, AIRefineData
from typing import List
from app.ai.find_foreign import find_words
from bs4 import BeautifulSoup

def refine_foreign(data: TextData) -> List[AIRefineData]:
    input_data = data.title, ' '.join(str(item) for item in data.content)
    word_list = []
    foreign_list = []
    
    for html in input_data:
        soup = BeautifulSoup(html, "html.parser")
        
        word_list.append(soup.get_text())
        
    foreign_data = find_words(word_list)
    
    for html in input_data:
        soup = BeautifulSoup(html, "html.parser")
        
        for word in foreign_data:
            find_sentences = soup.find_all(text=lambda text: text and word in text)
            
            for find_sentence in find_sentences:
                parent_tag = find_sentence.find_parent()
                id = parent_tag.get("id")
                sentence = find_sentence.strip()
                
                foreign_list.append({'id': id, 'foreign': word, 'sentence': sentence})
                
    # 여기에 dify 연결하면 됨
    
    return [  
        AIRefineData(
            target_id="e-0",
            error=[
                {
                    "code": 1,
                    "origin_word": "일빠",
                    "refine_word": "첫번째",
                    "index": 4
                },
                {
                    "code": 1,
                    "origin_word": "핸들링",
                    "refine_word": "처리",
                    "index": 20
                }
            ]
        )
    ]