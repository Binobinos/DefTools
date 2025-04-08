import datetime


def logger(default: any):
    def timer(func):

        def wrapper(*args, **kwargs):
            start = datetime.datetime.now()
            error = None
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                result = default
                error = e
            print(f"[{start}] - [{datetime.datetime.now() - start}]  {func.__name__}(args={args}, kwargs={kwargs}) "
                  f"-> {result} - \033[5;31mErrors: {str(error).title()}\033[0m")

        return wrapper

    return timer
