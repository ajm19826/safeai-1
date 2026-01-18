import re

class RuleEngine:
    def __init__(self):
        self.rules = {}

    def add_rule(self, pattern, result):
        self.rules[pattern] = result

    def apply(self, text):
        for pat, res in self.rules.items():
            # simple placeholder replacement
            placeholders = re.findall(r"\{(\w+)\}", pat)
            if placeholders:
                regex = pat
                for ph in placeholders:
                    regex = regex.replace(f"{{{ph}}}", r"(\w+)")
                match = re.match(regex, text)
                if match:
                    return res.format(*match.groups())
            else:
                if text.lower() == pat.lower():
                    return res
        return None

    def suggest_rule(self, text):
        # Auto-discover simple "A op B" math patterns
        match = re.match(r"(\d+)\s*(\+|\-|\*|/)\s*(\d+)", text)
        if match:
            a, op, b = match.groups()
            result = str(eval(f"{a}{op}{b}"))
            pattern = "{A} " + op + " {B}"
            self.add_rule(pattern, "{A}" + op + "{B} = " + result)
            return f"Auto-rule added: {pattern} -> {a}{op}{b} = {result}"
        return None
