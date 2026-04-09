import sys
from pathlib import Path
import time
import argparse
import select
import subprocess
import json

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
    parser.add_argument("skill_name")
    return parser

def main():

    """
    Endeavour to boot Opencode and then listen to an event stream and detect whether it is pulling in skills in response to given prompts.    
    """


    print("Starting program")
    
    # Validate the arguments
    parser = init_argparse()
    args = parser.parse_args()

    # Validate the files
    eval_set_file = validate_and_get_file(args.skill_name)
    eval_set = eval_set_file['evals']

    print(f"Running {len(eval_set)} evals for {args.skill_name}")

    eval_results = dict



    for eval in eval_set:
        print(f"Handling eval: {eval['id']}")

        cmd = [
            "opencode",
            "run", eval['prompt'],
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

                # select() means we avoid blocking indefinitely when reading from the child process because we know there is data to be read.
                ready, _, _ = select.select([openCodeProcess.stdout], [], [], 1)
                if ready:
                    chunk = openCodeProcess.stdout.readline()
                    if not chunk:
                        break

                    chunk_decoded = chunk.decode('utf-8', errors="replace")
                    decoded_chunk_as_json = json.loads(chunk_decoded)
                    print(f"decoded {decoded_chunk_as_json}")


                    if decoded_chunk_as_json.get('part', {}).get('tool') == 'skill':
                        print("Yeah, we have a skill")
                        eval_results[eval['id']] = True

                    print(f"Logging the decoded chunk: {chunk_decoded}")

                    buffer += chunk_decoded

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
            print("Cleaning up the Opencode subprocess")
            openCodeProcess.kill()
            pass
        




    


    print("Finishing program")




def validate_and_get_file(skill_name: str = ""):
    print("Checking if relevant files exist")

    # confirm that a matching skill exists
    skill_dir = Path(f"~/.config/opencode/skills/{skill_name}").expanduser()

    if not skill_dir.exists():
        raise SystemExit("This skill does not exist. Are you sure you typed it correctly?")
    
    # confirm that the eval-set exists
    eval_set_path = skill_dir / "assets" / "evals" / "eval-set.json"
    if not eval_set_path.exists():
        raise SystemExit("There is no eval set to process for this skill. Please ensure one exists.")
    
    print("Reading eval set for prompt testing scenarios")
    eval_set = json.load(Path.open(eval_set_path))
    return eval_set


main()