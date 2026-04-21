def classify_bridge(freq):

    if freq < 20:
        return "DANGER"

    elif 20 <= freq <= 30:
        return "WATCH"

    else:
        return "NORMAL"