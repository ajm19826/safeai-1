import numpy as np
from dataset import dataset, answer_map
from utils import encode_question, decode_answer
from neuralnet import NeuralNetwork

# Prepare data
X = np.array([encode_question(item['question']) for item in dataset])
y = np.zeros((len(dataset), len(answer_map)))
for i, item in enumerate(dataset):
    y[i][item['answer']] = 1  # one-hot encoding

# Initialize network
input_size = X.shape[1]
hidden_size = 10
output_size = y.shape[1]
nn = NeuralNetwork(input_size, hidden_size, output_size, lr=0.5)

# Train the network
print("Training SafeAI-1...")
nn.train(X, y, epochs=1000)
print("Training complete!\n")

# Command-line interface
while True:
    question = input("Ask SafeAI-1 a question (or type 'exit'): ")
    if question.lower() == "exit":
        break
    q_vec = np.array([encode_question(question)])
    class_index = nn.predict(q_vec)[0]
    answer = decode_answer(class_index, answer_map)
    print("SafeAI-1:", answer, "\n")
