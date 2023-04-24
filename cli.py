from belief_revision_agent import BeliefRevisonAgent
from sympy.parsing.sympy_parser import parse_expr

def main():
    agent = BeliefRevisonAgent()

    print("Welcome to the Belief Revision Agent!")
    print("Commands:")
    print("  check <belief>")
    print("  contract <belief>")
    print("  expand <belief>")
    print("  revise <belief>")
    print("  clear")
    print("  exit")

    while True:
        command = input("Enter command: ").strip()
        tokens = command.split()

        if len(tokens) < 1:
            print("Invalid command.")
            continue

        action = tokens[0].lower()

        if action == "exit":
            break
        
        if action != "clear":
            sentence = parse_expr(tokens[1])

        
        if action == "contract":
            agent.contract(sentence)
            print(f"Contracted belief base: {agent.belif_base}")
        elif action == "check":
            if agent.pl_resolution(sentence):
                print(f"The belief base entails {sentence}.")
            else:
                print(f"The belief base does not entail {sentence}.")
        elif action == "expand":
            agent.expand(sentence)
            print(f"Expanded belief base: {agent.belif_base}")
        elif action == "revise":
            agent.revise(sentence)
            print(f"Revised belief base: {agent.belif_base}")
        elif action == "clear":
            agent.clear()
            print(f"The belief was cleared. New belief base: {agent.belif_base}")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
