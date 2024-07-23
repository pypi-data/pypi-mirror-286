import argparse
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from response_generator import ResponseGenerator

class Chat99:
    def __init__(self, api_key):
        self.generator = ResponseGenerator(api_key)

    def chat(self):
        console = Console()
        console.print(Panel("Welcome to Chat99"))
        while True:
            user_input = Prompt.ask("You")
            if user_input.lower() in ["exit", "quit"]:
                break
            response = self.generator.generate_response(user_input)
            console.print(Markdown(response))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat99 CLI")
    parser.add_argument('--api_key', type=str, required=True, help='Your API key for Anthropic')
    args = parser.parse_args()
    chat_app = Chat99(api_key=args.api_key)
    chat_app.chat()
