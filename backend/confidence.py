def score(reason_steps, success=True):
    base = min(len(reason_steps) / 10, 1.0)
    return round(base if success else base * 0.4, 2)
