from app.schemas.ai import TextData, AIRefineData
from typing import List
from app.ai.find_foreign import find_words
from bs4 import BeautifulSoup
from app.ai.dify import dify

async def refine_foreign(data: TextData) -> List[AIRefineData]:
    input_data = data.title, ' '.join(str(item) for item in data.content)
    word_list = []
    foreign_dict = dict()
    
    for html in input_data:
        soup = BeautifulSoup(html, "html.parser")
        
        word_list.append(soup.get_text())
        
    foreign_data = find_words(word_list)
    
    for html in input_data:
        soup = BeautifulSoup(html, "html.parser")
        
        for word in foreign_data:
            find_sentences = soup.find_all(text=lambda text: word in text)
            
            for find_sentence in find_sentences:
                parent_tag = find_sentence.find_parent()
                id = parent_tag.get("id")
                sentence = find_sentence.strip()
            
                if id in foreign_dict.keys() and foreign_dict[id]['sentence'] == sentence:
                    foreign_dict[id]['origin_word'].append(word)
                else:
                    foreign_dict[id] = {"origin_word": [word], "sentence": sentence}
    
    responses = []
    
    for key in foreign_dict.keys():
        response = await dify(foreign_dict[key])
        
        responses.append(
            {
                "target_id": key,
                "error": [
                    {
                        "code": 1,
                        "origin_word": item,
                        "refine_word": response[item],
                        "index": foreign_dict[key]['sentence'].find(item)
                    }     
                    for item in response.keys()                 
                ]
            }
        )
        
    return responses