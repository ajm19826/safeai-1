import json
import numpy as np
from dataset import dataset, vocab, answer_map
from neuralnet import NeuralNetwork
from utils import encode_question, decode_answer

KNOWLEDGE_FILE = "knowledge.json"

# Load persistent knowledge
try:
    with open(KNOWLEDGE_FILE, "r") as f:
        persistent_knowledge = json.load(f)
        for item in persistent_knowledge:
            dataset.append({"question": item["question"], "answer": len(answer_map)})
            answer_map[len(answer_map)] = item["answer"]
except FileNotFoundError:
    persistent_knowledge = []

# Prepare training data
X = np.array([encode_question(d['question']) for d in dataset])
y = np.zeros((len(dataset), len(answer_map)))
for i, d in enumerate(dataset):
    y[i][d['answer']] = 1

# Initialize neural network
nn = NeuralNetwork(input_size=X.shape[1], hidden_size=10, output_size=len(answer_map), lr=0.5)
print("Training neural network on structured questions...")
nn.train(X, y, epochs=500)
print("Training complete!\n")

# Keyword responses
def keyword_response(question):
    q = question.lower()
    if "weather" in q: return "Check your local weather app!"
    if "book" in q or "read" in q: return "Try '1984' by Orwell or 'Sapiens' by Harari."
    if "coworker" in q: return "Sounds like you might need to communicate or take a break!"
    if "hello" in q or "hi" in q: return "Hello! How can I help you today?"
    if "your name" in q: return "I am SafeAI-1, your personal AI!"
    return None

# Main loop
print("SafeAI-1 is ready! Ask questions or type 'exit'.\n")
while True:
    question = input("You: ")
    if question.lower() == "exit":
        break

    # Keyword first
    response = keyword_response(question)
    if response:
        print("SafeAI-1:", response, "\n")
        continue

    # Neural network prediction
    vec = np.array([encode_question(question)])
    class_index = nn.predict(vec)[0]
    answer = decode_answer(class_index)
    print("SafeAI-1:", answer)

    # Feedback learning
    correct = input("Was this correct? (y/n): ").lower()
    if correct == "n":
        user_answer = input("Provide the correct answer: ")

        # Add new question
        dataset.append({"question": question, "answer": len(answer_map)})
        answer_map[len(answer_map)] = user_answer

        # Expand vocab dynamically
        for w in question.lower().split():
            if w not in vocab:
                vocab.append(w)

        # Rebuild training data
        X = np.array([encode_question(d['question']) for d in dataset])
        y = np.zeros((len(dataset), len(answer_map)))
        for i, d in enumerate(dataset):
            y[i][d['answer']] = 1

        # Re-init neural network with new output size
        nn = NeuralNetwork(input_size=X.shape[1], hidden_size=10, output_size=len(answer_map), lr=0.5)
        nn.train(X, y, epochs=200)  # smaller for speed

        # Save persistent knowledge
        persistent_knowledge.append({"question": question, "answer": user_answer})
        with open(KNOWLEDGE_FILE, "w") as f:
            json.dump(persistent_knowledge, f, indent=2)

        print("SafeAI-1: Got it! I will remember this for next time.\n")
