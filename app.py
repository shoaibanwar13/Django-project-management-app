from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import requests
import random
from collections import defaultdict
from textblob import TextBlob  # For spelling correction
import asyncio  # For asynchronous operations
from fastapi.middleware.cors import CORSMiddleware

# Ensure nltk resources are downloaded
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt')

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/pszemraj/flan-t5-large-grammar-synthesis"
headers = {"Authorization": "Bearer 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"}  # Replace with your token

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Pydantic model for request body
class TextInput(BaseModel):
    text: str

# A simple glossary of terms you want to preserve
preserved_terms = set([
    "ERP", "AI", "machine learning", "deep learning", 
    "data science", "enterprisingness", "imagination", "provision"
])

# Helper function to map nltk POS tags to WordNet POS tags
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

# Get synonyms with context awareness
def get_best_synonym(word, pos):
    synonyms = []
    for syn in wordnet.synsets(word, pos=pos):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace('_', ' ')
            if synonym.lower() != word.lower() and len(synonym.split()) == 1:
                synonyms.append((synonym, lemma.count()))

    synonyms = sorted(synonyms, key=lambda x: x[1], reverse=True)
    top_synonyms = [syn[0] for syn in synonyms[:3]] if synonyms else []
    return random.choice(top_synonyms) if top_synonyms else word

# Function to identify important terms using NLTK's named entity recognition
def extract_named_entities(text):
    words = word_tokenize(text)
    pos_tags = pos_tag(words)
    named_entities = nltk.ne_chunk(pos_tags)
    entities = set()

    for chunk in named_entities:
        if hasattr(chunk, 'label'):
            entities.add(' '.join(c[0] for c in chunk))

    return entities

# Paraphrase function with synonym replacement
def paraphrase_sentence(sentence):
    corrected_sentence = str(TextBlob(sentence).correct())
    named_entities = extract_named_entities(corrected_sentence)
    words = word_tokenize(corrected_sentence)
    preserved_words = words[:3]
    remaining_words = words[3:]

    paraphrased_sentence = preserved_words
    for word, tag in pos_tag(remaining_words):
        if word in preserved_terms or word in named_entities:
            paraphrased_sentence.append(word)
        else:
            wordnet_pos = get_wordnet_pos(tag)
            if wordnet_pos:
                synonym = get_best_synonym(word, wordnet_pos)
                paraphrased_sentence.append(synonym)
            else:
                paraphrased_sentence.append(word)
    
    return ' '.join(paraphrased_sentence)

# Asynchronous function to query the Hugging Face API
async def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Retry mechanism with exponential backoff
async def query_with_retry(payload, max_retries=5, delay=2):
    for attempt in range(max_retries):
        response = await query(payload)
        if "error" in response and "loading" in response["error"]:
            await asyncio.sleep(delay)
            delay *= 2  # Exponential backoff
        else:
            return response
    raise HTTPException(status_code=500, detail="API is still loading after multiple attempts.")

# FastAPI endpoint for text processing
@app.post("/generate/")
async def process_text_with_api(input: TextInput):
    paraphrased_text = paraphrase_sentence(input.text)
    response = await query_with_retry({"inputs": paraphrased_text})
    
    if "error" not in response:
        refined_text = response[0].get('generated_text', '')
        return {"paraphrased_text": paraphrased_text, "generated_text": refined_text}
    else:
        raise HTTPException(status_code=500, detail=f"API error: {response['error']}")
