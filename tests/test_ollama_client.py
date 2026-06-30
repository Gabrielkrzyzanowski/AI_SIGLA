import pytest
import requests
from shared_utils import OllamaWrapper 


BASE_URL = 'http://localhost:11434'

def is_ollama_connected():
    "Test that the server is up, responding, and returns a 200 OK status"
    try: 
        response = requests.get(f'{BASE_URL}/api/tags', timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False

@pytest.mark.skipif(
    not is_ollama_connected(), 
    reason='Local Ollama server is not running'
)
class TestClient:

    @pytest.fixture(autouse=True)
    def setup(self,): 
        self.client = OllamaWrapper(base_url=BASE_URL) 
    @pytest.fixture 
    def payload(self,): 
        return [
            "If the connection is properly stablished answer 'Hello World!'.", 
            "gemma4:e4b-it-qat",
            "You are a model used for connection tests. Only answer what is asked.",
            0.7,
            0.9,
        ]

    def test_generate_stream(self, payload): 
        """Verifies that the client can successfully stream tokens from a real server."""
        generator = self.client.generate_stream(*payload) 
        tokens = list(generator) 
        full_response= "".join(tokens).strip()

        assert "Hello World!" in full_response