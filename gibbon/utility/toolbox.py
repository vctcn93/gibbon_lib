import time
import sys


def timeit(func):
    def wrapper(*args, **kwargs):
        print('➜➜➜➜➜➜ %30s ➜➜➜➜➜➜ start...' % func.__name__)
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('░░░░░░ %30s ░░░░░░ used time -> %6.6f s' % (func.__name__, end - start))
        return result

    return wrapper


def progress_bar(num, total):
    """
    以进度条的形式打印出执行的进度
    :param num: 当前的轮数
    :param total: 总共的轮数
    :return: None
    """
    rate = float(num) / total
    ratenum = int(100 * rate)
    r = '\r[{}{}]{}%'.format('*' * ratenum, ' ' * (100 - ratenum), ratenum)
    sys.stdout.write(r)
    sys.stdout.flush()


def divide_by_quantity(quantity):
    ls = list(range(quantity))
    new = [0] * quantity

    for i in range(quantity):
        new[i] = ls[i] / (quantity - 1)

    return new


def flag(name):
    print(f'>>>>>>>> this is flag {name} >>>>>>>')
