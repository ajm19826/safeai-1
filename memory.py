class MemoryGraph:
    def __init__(self):
        self.concepts = {}   # concept -> properties
        self.links = {}      # concept -> related concepts

    def add_concept(self, name, value=None):
        name = name.lower()
        if name not in self.concepts:
            self.concepts[name] = set()
        if value:
            self.concepts[name].add(value.lower())

    def link(self, a, b):
        a, b = a.lower(), b.lower()
        self.links.setdefault(a, set()).add(b)
        self.links.setdefault(b, set()).add(a)

    def knows(self, concept):
        return concept.lower() in self.concepts

    def get_properties(self, concept):
        return list(self.concepts.get(concept.lower(), []))

    def related(self, concept):
        return list(self.links.get(concept.lower(), []))
