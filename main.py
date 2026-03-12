import sys
import argparse
import subprocess

OPENCODE_TIMEOUT=120

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


def listen_to_events():
    return


def main():
    parser = init_argparse()
    args = parser.parse_args()

    # does the skill exist inside of the 

    listen_to_events()
# usage: opencode run "prompt" --output-format json

    """
    Endeavour to boot Opencode and then listen to an event stream and detect whether it is pulling in skills in response to given prompts.    
    """

    try:
        openCodeProcess = subprocess.run(['opencode'], timeout=OPENCODE_TIMEOUT, check=True, shell=True, encoding="utf-8", input="--output-format json --model opencode/nemotron-3-super-free")


        # decode the response from openCode
        openCodeProcess.stdout.decode("utf-8")

    except subprocess.TimeoutExpired as exc:
        print(f"Process timed out.\n{exc}")
        raise SystemExit(1, 'Opencode was hanging indefinitely. Timeout hit.')
    except subprocess.CalledProcessError as exc:
        print(f"Process failed because did not return a successful return code. Returned {exc.returncode}\n{exc}")
        raise SystemExit(1, 'Process did not return a successful return code.')
    finally:
        pass
    


    print("Starting program")


main()