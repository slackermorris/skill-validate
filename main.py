import sys

def main (args=None):
    # Extract arguments from the CLI but support the possibility that this function is called elsewhere.
    if args is None:
            args = sys.argv[1:]
            print(f"Arguments of the script:, {args}=")
            

main()