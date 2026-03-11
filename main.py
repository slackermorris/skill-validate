import sys
import argparse
import os
import threading
import httpx
from opencode_ai import Opencode
import opencode_ai


class NoContentTypeClient(httpx.Client):
    def send(self, request, **kwargs):
        if not request.content and "content-type" in request.headers:
            request.headers.pop("content-type")
        return super().send(request, **kwargs)


http_client = NoContentTypeClient()


class ImprovedErrorArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"\nError: {message}\n")
        self.print_help()
        sys.exit(2)


def init_argparse() -> argparse.ArgumentParser:
    parser = ImprovedErrorArgumentParser()
    parser.add_argument("-u", "--url", default=None, help="OpenCode server URL")
    parser.add_argument("-p", "--prompt", required=True, help="Prompt to send")
    parser.add_argument("--provider", default="anthropic", help="Provider ID")
    parser.add_argument("--model", default="claude-sonnet-4-20250514", help="Model ID")
    return parser


def listen_to_events(client: Opencode, stop_event: threading.Event):
    try:
        stream = client.event.list()
        for events in stream:
            print(f"Event: {events}")
            if stop_event.is_set():
                break
    except opencode_ai.APIConnectionError as e:
        print(f"Connection error: {e.__cause__}")
    except Exception as e:
        print(f"Event stream error: {e}")


def main():
    parser = init_argparse()
    args = parser.parse_args()

    base_url = args.url or os.environ.get("OPENCODE_BASE_URL", "http://127.0.0.1:54321")
    print(f"Connecting to: {base_url}")

    client = Opencode(base_url=base_url, http_client=http_client)

    stop_event = threading.Event()
    event_thread = threading.Thread(target=listen_to_events, args=(client, stop_event))
    event_thread.start()

    try:
        print("Creating session...")
        session = client.session.create()
        print(f"Session created: {session.id}")

        print(f"Sending prompt: {args.prompt}")
        response = client.session.chat(
            id=session.id,
            model_id=args.model,
            provider_id=args.provider,
            parts=[{"type": "text", "text": args.prompt}],
        )
        print(f"Response: {response}")

    except opencode_ai.APIConnectionError as e:
        print(f"The server could not be reached: {e.__cause__}")
    except opencode_ai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
    except opencode_ai.APIStatusError as e:
        print(f"Non-200 status code: {e.status_code}")
        print(e.response)
    finally:
        stop_event.set()
        event_thread.join()
        print("Done")


main()