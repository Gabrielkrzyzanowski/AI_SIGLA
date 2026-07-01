import pandas as pd 
from ollama_wrapper import OllamaWrapper

#Calling the model API with a prompt 
def caller( 
    prompt : str, 
    model : str, 
    system_prompt : str, 
    temperature : float, 
    top_p : float,
): 
    client = OllamaWrapper() 
    try: 
        for token in client.generate_stream( 
            prompt = prompt, 
            model = model, 
            system_prompt = system_prompt, 
            temperature = temperature, 
            top_p = top_p,
            ): 
            print(token, end="") 
    except RuntimeError as e: 
        raise RuntimeError(f"Generator failed: {e}") 

if __name__ == '__main__':
    prompts = pd.read_csv("prompts.csv") 
    prompts_df = pd.DataFrame(prompts) 

    caller( 
        prompt = prompts_df.iat[0,0], 
        model = "gemma4:e4b-it-qat", 
        system_prompt = "You are a helpfull assistance", 
        temperature = 0.7, 
        top_p = 0.9,
    )


