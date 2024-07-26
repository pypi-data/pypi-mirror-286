from langchain_openai import ChatOpenAI
from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_model_id(model_name):
    return model_name.split('/')[-1]

def validate_model_id(model_name):
    model_id = get_model_id(model_name)
    if model_name.lower().startswith('openai/'):
        return True
    else:
        url = f"https://huggingface.co/api/models/{model_id}"
        response = requests.head(url)
        if response.status_code == 200:
            return True
        else:
            logger.error(f"Model ID '{model_id}' validation failed with status code {response.status_code}")
            return False

def load_model(model_name):
    model_id = model_name
    try:        
        if model_name.lower().startswith('openai/'):
            model_id = get_model_id(model_name)
            logger.info(f'OpenAI model: {model_id}')
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                raise ValueError("OpenAI API key not found in environment variables.")
            return ChatOpenAI(model=model_id)
        else:
            huggingface_api_key = os.getenv('HUGGINGFACE_API_KEY')
            if not huggingface_api_key:
                raise ValueError("HuggingFace API key not found in environment variables.")
            login(huggingface_api_key)
            logger.info(f'HuggingFace model: {model_id}')
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            model = AutoModelForCausalLM.from_pretrained(model_id)
            return model, tokenizer
    except Exception as e:
        logger.error(f"Error loading model '{model_name}': {e}")
        return None, None