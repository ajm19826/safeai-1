import numpy as np
from dataset import vocab

def encode_question(question):
    vector = np.zeros(len(vocab))
    words = question.lower().replace("^2", " ^2").replace("^3", " ^3").split()
    for i, word in enumerate(vocab):
        if word.lower() in words:
            vector[i] = 1
    return vector

def decode_answer(class_index, answer_map):
    return answer_map.get(class_index, "I don't know the answer.")
