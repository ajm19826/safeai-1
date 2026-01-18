from utils import tokenize, is_math

class Reasoner:
    def __init__(self, rule_engine, memory, neural, planner):
        self.rules = rule_engine
        self.memory = memory
        self.neural = neural
        self.planner = planner

    def think(self, text, thoughts):
        tokens = tokenize(text)
        thoughts.append(f"Tokens: {tokens}")

        plan = self.planner.plan(text, thoughts)

        for step in plan:
            if step == "answer":
                rule = self.rules.apply(text)
                if rule:
                    thoughts.append("Answered using rule")
                    self.neural.train(tokens, 0)
                    return rule, True

            if step == "math" and is_math(tokens):
                try:
                    expr = "".join(tokens)
                    result = eval(expr)
                    thoughts.append(f"Math solved: {expr}")
                    self.neural.train(tokens, 0)
                    return result, True
                except:
                    thoughts.append("Math failed")

            if step == "learn_concept":
                thoughts.append("Potential concept detected")
                return "Tell me more so I can learn.", False

            if step == "explore":
                thoughts.append("Exploration mode activated")
                related = []
                for t in tokens:
                    related.extend(self.memory.related(t))
                if related:
                    return f"Related concepts: {set(related)}", True

        self.neural.train(tokens, 2)
        thoughts.append("Plan execution failed")
        return "I don't know yet.", False
