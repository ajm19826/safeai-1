from reasoning import Reasoner
from rules import RuleEngine
from memory import MemoryGraph
from neural import NeuralAssist
from planner import Planner
from reinforcement import Reinforcement
from confidence import score

LOG_FILE = "logs.txt"

rules = RuleEngine()
memory = MemoryGraph()
neural = NeuralAssist()
planner = Planner(memory, rules)
reinforce = Reinforcement()

reasoner = Reasoner(rules, memory, neural, planner)

def log(thoughts):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        for t in thoughts:
            f.write("[THOUGHT] " + t + "\n")
        f.write("\n")

print("SafeAI-1 (Step 6: Autonomous AI Agent)")
print("Commands:")
print("  @improve: A + B -> A+B")
print("  @learn: water = H2O")
print("  exit\n")

while True:
    user = input("You: ")
    if user == "exit":
        break

    thoughts = [f"Input: {user}"]

    if user.startswith("@improve:"):
        left, right = user.replace("@improve:", "").split("->")
        rules.add_rule(left.strip(), right.strip())
        print("SafeAI-1: Rule learned.")
        continue

    if user.startswith("@learn:"):
        left, right = user.replace("@learn:", "").split("=")
        memory.add_concept(left.strip(), right.strip())
        memory.link(left.strip(), right.strip())
        print("SafeAI-1: Concept learned.")
        continue

    response, success = reasoner.think(user, thoughts)
    conf = score(thoughts, success)

    if success:
        reinforce.reward()
    else:
        reinforce.punish()

    thoughts.append(f"Confidence: {conf}")
    log(thoughts)

    print(f"SafeAI-1 ({conf}): {response}")
