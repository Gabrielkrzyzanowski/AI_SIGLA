import click
from ollama_wrapper import OllamaWrapper 

@click.group()
def cli(): 
    pass 

@cli.command()
@click.option( 
    "--prompt", "-p", 
    required = True,
    help = "Text for the model to generate a response from.",
)
@click.option( 
    "--model", "-m", 
    default = "gemma4:e4b-it-qat",
    help = "Model name",
)
@click.option( 
    "--system", "-s", 
    default = "You are a helpful assistant.",
    help = "System prompt for the model to generate a response from.",
)
@click.option( 
    "--temperature", "-t",
    type = float,
    default = 0.7,
    help = "Controls randomness in generation (0.0 = deterministic, 1.0 = creative).",
)
@click.option( 
    "--top-p", 
    type = click.FloatRange(0.0, 1.0),
    default = 0.9,
    help = "Cumulative probability threshold for nucleus sampling",
)
def ask( 
    prompt: str, 
    model: str, 
    system: str, 
    temperature: float, 
    top_p: float,
):
    """Send a prompt to the LLM with custom parameters"""
    client = OllamaWrapper() 
    click.echo(click.style(f"Processing request with {model}...", fg="green"))
    click.echo(click.style(f"Config -> Temp: {temperature} | Top_p: {top_p}\n", fg="magenta"))

    try: 
        for token in client.generate_stream(
            prompt = prompt, 
            model = model, 
            system_prompt = system, 
            temperature = temperature, 
            top_p = top_p,
            ): 
            click.echo(token,nl=False)
        click.echo() 
    except RuntimeError as e:
        click.echo(click.style(f'\nAn error occurred: {e}', fg='red'), err=True)

if __name__ == "__main__":     
    cli()