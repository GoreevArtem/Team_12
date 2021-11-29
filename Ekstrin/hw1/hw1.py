from datetime import datetime


def all_eq(lst: list):
    max_l = max(len(x) for x in lst)
    return [x + '_' * (max_l - len(x)) for x in lst]


def log(show_args=True):
    def inner_log(func):
        def inner(*args, **kwargs):
            print(f'timestamp: {datetime.now()}')
            if show_args:
                print(f'args: {args}\n'
                      f'kwargs: {kwargs}')
            return func(*args, *kwargs)

        return inner

    return inner_log


@log(True)
def hello(*args, **kwargs):
    print('Hello!')
