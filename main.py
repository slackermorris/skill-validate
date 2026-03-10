import argparse



def init_argparse() -> argparse.ArgumentParser:
     parser = argparse.ArgumentParser(
          description="Perform 'health' checks on an Agent Skill"
     )

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