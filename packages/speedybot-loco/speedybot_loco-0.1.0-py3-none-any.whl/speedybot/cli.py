import argparse
import runpy
import os
from .cards import Cards

def main():
    parser = argparse.ArgumentParser(description="Bongo CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Token command
    token_parser = subparsers.add_parser("token", help="Set the bot token")
    token_parser.add_argument("-t", "--token", type=str, help="Bot token")

    # Webhook command
    webhook_parser = subparsers.add_parser("webhook", help="Run webhook server")
    webhook_parser.add_argument("-t", "--token", type=str, required=True, help="Bot token")
    webhook_parser.add_argument("-p", "--port", type=int, required=True, help="Port to listen on")
    webhook_parser.add_argument("--path", type=str, required=True, help="Path to send POST requests")

    # Run file command
    file_parser = subparsers.add_parser("run", help="Run a Python file")
    file_parser.add_argument("-t", "--token", type=str, required=True, help="Bot token")
    file_parser.add_argument("-f", "--file", type=str, required=True, help="Path to the Python file to run")

    args = parser.parse_args()

    if args.command == "token":
        handle_token(args.token)
    elif args.command == "webhook":
        handle_websockets(args.token, args.port, args.path)
    elif args.command == "run":
        handle_run(args.token, args.file)
    else:
        parser.print_help()

def handle_token(token):
    if not token:
        token = input("Please enter your bot token: ")
    print(f"Bot token set: {token}")

def handle_websockets(token, port, path):
    print("placeholder websocket")
    
def handle_run(token, file_path):
    os.environ["BOT_TOKEN"] = token
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return
    print(f"Running file: {file_path}")
    runpy.run_path(file_path)

if __name__ == "__main__":
    main()
