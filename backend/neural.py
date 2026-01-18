import numpy as np

class NeuralAssist:
    def __init__(self, input_size=20, hidden=150, output_size=3):
        self.W1 = np.random.randn(input_size, hidden) * 0.1
        self.W2 = np.random.randn(hidden, output_size) * 0.1

    def encode(self, tokens):
        vec = np.zeros(20)
        for i, t in enumerate(tokens[:20]):
            vec[i] = sum(ord(c) for c in t) % 100 / 100
        return vec

    def forward(self, x):
        h = np.tanh(x @ self.W1)
        o = h @ self.W2
        return o

    def predict(self, tokens):
        x = self.encode(tokens)
        o = self.forward(x)
        return np.argmax(o)  # 0=math, 1=concept, 2=unknown

    def train(self, tokens, target):
        x = self.encode(tokens)
        y = np.zeros(3)
        y[target] = 1

        # Forward
        h = np.tanh(x @ self.W1)
        o = h @ self.W2

        # Backprop
        error = o - y
        dW2 = np.outer(h, error)
        dW1 = np.outer(x, (1 - h**2) * (error @ self.W2.T))

        self.W2 -= 0.01 * dW2
        self.W1 -= 0.01 * dW1
