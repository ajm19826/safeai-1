# dataset.py

dataset = [
    {"question": "solve x + 2 = 5", "answer": 0},
    {"question": "solve 2*x = 10", "answer": 0},
    {"question": "what is the derivative of x^2", "answer": 1},
    {"question": "what is the derivative of x^3", "answer": 1},
    {"question": "integrate x dx", "answer": 1},
    {"question": "write a for loop in python", "answer": 2},
    {"question": "write a while loop in python", "answer": 2},
    {"question": "define a function in python", "answer": 2},
    {"question": "what is H2O", "answer": 3},
    {"question": "what is CO2", "answer": 3},
    {"question": "what planet is closest to the sun", "answer": 3},
    {"question": "solve x^2 - 4 = 0", "answer": 0},
]

answer_map = {
    0: "x = 3 (or other solution)",               # math solving
    1: "calculus answer (derivative/integral)",   # calculus
    2: "Python code example",                      # coding
    3: "science answer (fact explanation)",       # science
}

# Vocabulary for encoding
vocab = ["solve", "x", "+", "2", "5", "2*x", "10", "derivative", "of", "^2", "^3", "integrate", "dx",
         "write", "for", "while", "loop", "in", "python", "define", "a", "function",
         "what", "is", "H2O", "CO2", "planet", "closest", "to", "sun"]
