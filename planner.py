class Planner:
    def __init__(self, memory, rules):
        self.memory = memory
        self.rules = rules

    def plan(self, text, thoughts):
        plan = []

        thoughts.append("Planning next actions")

        if "?" in text:
            plan.append("answer")

        if "=" in text:
            plan.append("learn_concept")

        if any(op in text for op in "+-*/"):
            plan.append("math")

        if not plan:
            plan.append("explore")

        thoughts.append(f"Plan created: {plan}")
        return plan
