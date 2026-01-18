import random

class SelfTest:
    def __init__(self, memory, rules):
        self.memory = memory
        self.rules = rules

    def quiz_concept(self):
        self.memory.cursor.execute("SELECT name FROM concepts")
        concepts = [r[0] for r in self.memory.cursor.fetchall()]
        if not concepts:
            return "No concepts to quiz."
        concept = random.choice(concepts)
        props = self.memory.get_properties(concept)
        return f"What are properties of '{concept}'? Answer: {props}"

    def quiz_rule(self):
        if not self.rules.rules:
            return "No rules to quiz."
        pattern, result = random.choice(list(self.rules.rules.items()))
        return f"Predict result for pattern '{pattern}': {result}"
