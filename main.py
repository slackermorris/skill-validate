import sys
import argparse


class ImprovedErrorArgumentParser(argparse.ArgumentParser):
     def error(self, message):
          print(f"\nError: {message}\n")
          self.print_help()
          sys.exit(2)


def init_argparse() -> argparse.ArgumentParser:
     parser = ImprovedErrorArgumentParser()

     parser.add_argument('-a', '--action', choices=["usage", "fix"], required=True)
     parser.add_argument('skill_name')

     return parser

def main ():
    print('Start of function')

    parser = init_argparse()

    args = parser.parse_args()

    print(f"Arguments of the script:, {args}=")

    print('End of function')
            

main()