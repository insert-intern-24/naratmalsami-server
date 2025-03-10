import os
import re
import numpy as np
from dotenv import load_dotenv
from konlpy.tag import Hannanum
from konlpy import jvm
java_home = os.environ.get('JAVA_HOME')

if java_home is None:
    java_home = '/Users/kwon5700/Library/Java/JavaVirtualMachines/openjdk-23.0.1/Contents/Home'

os.environ['JAVA_HOME'] = java_home

from tensorflow.keras.models import load_model
from jamo import h2j, j2hcj
from tensorflow.keras.preprocessing.sequence import pad_sequences
from app.schemas.ai import TextData

load_dotenv()
os.environ['JAVA_HOME'] = os.environ.get('JAVA_HOME')

jvm.init_jvm()

h = Hannanum()

jamo_dict = {
    'ㄱ': 1, 'ㄲ': 2, 'ㄳ': 3, 'ㄴ': 4, 'ㄵ': 5, 'ㄶ': 6, 'ㄷ': 7, 'ㄸ': 8, 'ㄹ': 9, 'ㄺ': 10, 
    'ㄻ': 11, 'ㄼ': 12, 'ㄽ': 13, 'ㄾ': 14, 'ㄿ': 15, 'ㅀ': 16, 'ㅁ': 17, 'ㅂ': 18, 'ㅃ': 19, 'ㅄ': 20, 
    'ㅅ': 21, 'ㅆ': 22, 'ㅇ': 23, 'ㅈ': 24, 'ㅉ': 25, 'ㅊ': 26, 'ㅋ': 27, 'ㅌ': 28, 'ㅍ': 29, 'ㅎ': 30, 
    'ㅏ': 31, 'ㅐ': 32, 'ㅑ': 33, 'ㅒ': 34, 'ㅓ': 35, 'ㅔ': 36, 'ㅕ': 37, 'ㅖ': 38, 'ㅗ': 39, 'ㅘ': 40, 
    'ㅙ': 41, 'ㅚ': 42, 'ㅛ': 43, 'ㅜ': 44, 'ㅝ': 45, 'ㅞ': 46, 'ㅟ': 47, 'ㅠ': 48, 'ㅡ': 49, 'ㅢ': 50, 
    'ㅣ': 51, ' ': 52, 'a': 53, 'b': 54, 'c': 55, 'd': 56, 'e': 57, 'f': 58, 'g': 59, 'h': 60, 'i': 61, 'j': 62, 
    'k': 63, 'l': 64, 'm': 65, 'n': 66, 'o': 67, 'p': 68, 'q': 69, 'r': 70, 's': 71, 't': 72, 
    'u': 73, 'v': 74, 'w': 75, 'x': 76, 'y': 77, 'z': 78, '.': 79
}

model = load_model('/Users/kwon5700/Desktop/naratmalsami-server/app/ai/naratmalsami-ai.keras')

def find_words(input_data: TextData):
    
    foreign = set()
    alpha = r'[a-zA-Z]'
    
    for datas in input_data:
        for data in h.nouns(datas):
            origin_data = data
            
            if re.search(alpha, origin_data):
                foreign.add(origin_data)
            else:
                token = [jamo_dict.get(i, 80) for i in j2hcj(h2j(data))]
                
                token = pad_sequences([token], maxlen=25, padding='post', truncating='post', value=0)
        
                prediction = model.predict(np.expand_dims(token, axis=-1)) 
                
                prediction = list(prediction)
                
                if prediction[0][0] >= 0.4:
                    foreign.add(origin_data)
    
    return list(foreign)