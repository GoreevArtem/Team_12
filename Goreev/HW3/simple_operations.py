def factorial(n: int) -> int:
    if n in (0, 1):
        return 1
    return n * factorial(n - 1)


def fib(n: int) -> int:
    if n in (1, 2):
        return 1
    return fib(n - 1) + fib(n - 2)