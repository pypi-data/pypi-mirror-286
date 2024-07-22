from io import BytesIO
import requests
from urllib.parse import quote

__version__ = "1.0.10"

__all__ = ["api"]


class HorridAPI:
    """Horrid API Wrapper Class"""

    @staticmethod
    def joke():
        """Fetches a joke from the Horrid API."""
        api = f'https://horrid-api.onrender.com/joke'
        res = requests.get(api).json()
        return res['joke']

    @staticmethod
    def truth():
        """Fetches a truth statement from the Horrid API."""
        api = f'https://horrid-api.onrender.com/truth'
        res = requests.get(api).json()
        return res['truth']

    @staticmethod
    def dare():
        """Fetches a dare from the Horrid API."""
        api = f'https://horrid-api.onrender.com/dare'
        res = requests.get(api).json()
        return res['dare']

    @staticmethod
    def ai(query: str, prompt: str):
        """Fetches a response from the Horrid API's Ai endpoint."""
        query = quote(query)
        api = f'https://horrid-api.onrender.com/ai'
        headers = {"Content-Type": "application/json"}
        data = {"query": query, "prompt": prompt}        
        res = requests.post(api, headers=headers, json=data).json()
        return res['response']

    @staticmethod
    def qr(query: str):                
        api = f'https://horrid-api.onrender.com/qr?text={query}'
        response = requests.get(url)
        img = BytesIO(response.content)
        return img
        
    @staticmethod
    def gpt(query: str):        
        prompt = quote(query)
        api = f'https://horrid-api.onrender.com/gpt?query={prompt}'
        res = requests.get(api).json()
        return res['response']        
        
    @staticmethod
    def llama(query: str):
        """Fetches a response from the Horrid API's llama endpoint."""
        prompt = quote(query)
        api = f'https://horrid-api.onrender.com/llama?query={prompt}'
        res = requests.get(api).json()
        return res['response']        

# Instead of creating an instance and shadowing the built-in function
# Use the class methods directly
api = HorridAPI()
