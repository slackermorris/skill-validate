import sys
import time
import argparse
import select
import subprocess

OPENCODE_TIMEOUT=120 # two minute timeout

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

    cmd = [
        "opencode",
        "run", "tell me about re-render memo. be sure to pull in a skill",
        "--format", "json",
        "--model", "opencode/nemotron-3-super-free"
    ]

    start_time = time.time()
    buffer = ""

    try:
        openCodeProcess = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )

        print("Opencode process started")

        while time.time() - start_time < OPENCODE_TIMEOUT:
            # poll() returns None when the process is running. So, this block executes when the process has finished, as a sort of clean-up, read remaining bytes.
            if openCodeProcess.poll() is not None:
                remaining = openCodeProcess.stdout.read()
                if remaining:
                    buffer += remaining.decode("utf-8", errors="replace")
                    print(f"Remaining buffer: {buffer}")
                break

            # select() means we avoid blocking indefinitely when reading from the child process.
            ready, _, _ = select.select([openCodeProcess.stdout], [], [], 1)
            if ready:
                chunk = openCodeProcess.stdout.readline()
                if not chunk:
                    break
                print(f"logging chunk {chunk.decode('utf-8').__sizeof__()}")
                buffer += chunk.decode('utf-8', errors="replace")
                # print(f"Buffer: {buffer}")

        if time.time() - start_time >= OPENCODE_TIMEOUT:
            openCodeProcess.kill()
            raise subprocess.TimeoutExpired(cmd, OPENCODE_TIMEOUT)
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