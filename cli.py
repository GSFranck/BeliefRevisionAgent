from belief_revision_agent import BeliefRevisionAgent
from sympy import symbols

def main():
    agent = BeliefRevisionAgent()

    print("Welcome to the Belief Revision Agent!")
    print("Commands:")
    print("  expand <belief>")
    print("  contract <belief>")
    print("  check <belief>")
    print("  postulates")
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

        if len(tokens) < 2 and action != "postulates":
            print("Invalid command.")
            continue

        belief = None
        if action != "postulates":
            belief = symbols(tokens[1])

        if action == "expand":
            agent.expand(belief)
            print(f"Expanded belief base: {agent.belief_base}")
        elif action == "contract":
            agent.contract(belief)
            print(f"Contracted belief base: {agent.belief_base}")
        elif action == "check":
            if agent.check_entailment(belief):
                print(f"The belief base entails {belief}.")
            else:
                print(f"The belief base does not entail {belief}.")
        elif action == "postulates":
            agent.agm_postulates()
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
