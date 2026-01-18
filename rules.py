import re

class RuleEngine:
    def __init__(self):
        self.rules = []

    def add_rule(self, left, right):
        pattern = re.sub(r"\d+", r"(\\d+)", left.lower())
        self.rules.append((re.compile(pattern), right))

    def apply(self, text):
        for pattern, output in self.rules:
            match = pattern.fullmatch(text.lower())
            if match:
                try:
                    values = map(int, match.groups())
                    return str(eval(output.format(*values)))
                except:
                    return output
        return None
