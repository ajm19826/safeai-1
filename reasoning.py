from utils import tokenize, is_math

class Reasoner:
    def __init__(self, rule_engine, memory, neural):
        self.rules = rule_engine
        self.memory = memory
        self.neural = neural

    def think(self, text, thoughts):
        tokens = tokenize(text)
        thoughts.append(f"Tokens: {tokens}")

        # Neural intuition
        hint = self.neural.predict(tokens)
        thoughts.append(f"Neural hint: {['math','concept','unknown'][hint]}")

        # 1️⃣ Rules
        rule_result = self.rules.apply(text)
        if rule_result:
            thoughts.append("Rule engine succeeded")
            self.neural.train(tokens, 0)
            return rule_result, True

        # 2️⃣ Math
        if hint == 0 and is_math(tokens):
            try:
                expr = "".join(tokens)
                result = eval(expr)
                thoughts.append(f"Math evaluated: {expr}")
                self.neural.train(tokens, 0)
                return result, True
            except:
                thoughts.append("Math failed")

        # 3️⃣ Concept memory
        if hint == 1:
            for t in tokens:
                if self.memory.knows(t):
                    props = self.memory.get_properties(t)
                    thoughts.append(f"Concept recall: {t}")
                    self.neural.train(tokens, 1)
                    return ", ".join(props), True

        self.neural.train(tokens, 2)
        thoughts.append("All reasoning paths failed")
        return "I don't know yet.", False
