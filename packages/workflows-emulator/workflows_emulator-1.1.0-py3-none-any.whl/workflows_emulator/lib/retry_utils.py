from sys import maxsize

always = {
    'max_retries': maxsize ** 10 - 1,
}

default_backoff = {
    'initial_delay': 1,
    'max_delay': 60,
    'multiplier': 1.25,
}

never = {
    'max_retries': 0,
}
