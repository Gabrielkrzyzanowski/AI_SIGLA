import json
import requests 


class OllamaWrapper:
    "A class to interact with ollama instances via port '11434'." 
    def __init__(self, 
        base_url: str = 'http://localhost:11434'
        ):
        self.base_url = base_url
        self.session = requests.Session() #reuses the same TCP connection for multiple requests 

    def generate_stream(
        self,
        prompt: str,
        model: str ,
        system_prompt: str,
        temperature: float,
        top_p: float,  
    ): 
        url = f'{self.base_url}/api/generate'
        payload = {
                "model": model,
                "system": system_prompt,
                "prompt": prompt,
                "options": {
                    "temperature": temperature,
                    "top_p": top_p,
                },
            }
        try: 
            response = self.session.post( 
                url,
                json=payload,
                stream=True,
            )
            response.raise_for_status() 

            for line in response.iter_lines(): 
                if not line:  
                    continue 
                if line: 
                    try: 
                        chunck = json.loads(line.decode('utf-8')) 
                        token = chunck.get('response', '') 
                        if token: 
                            yield token 
                    except json.JSONDecodeError as e:
                        raise ValueError(f'Error trying to decode the json file: {e}') 
        except requests.RequestException as e: 
            raise RuntimeError(f'Ollama API communication failed: {e}')

