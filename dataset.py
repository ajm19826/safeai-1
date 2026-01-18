dataset = [
    {"question": "solve x + 2 = 5", "answer": 0},
    {"question": "solve 2*x = 10", "answer": 1},
    {"question": "what is the derivative of x^2", "answer": 2},
    {"question": "write a for loop in python", "answer": 3},
    {"question": "what is H2O", "answer": 4},
]

answer_map = {
    0: "x = 3",
    1: "x = 5",
    2: "derivative is 2*x",
    3: "for i in range(n): ...",
    4: "H2O is water",
}

# Initial vocab (can grow dynamically)
vocab = ["solve","x","+","2","5","2*x","10","derivative","of","^2",
         "write","for","loop","in","python","what","is","H2O"]
