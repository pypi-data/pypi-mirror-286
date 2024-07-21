import time


def retry(func, retries=3, delay=0, backoff=2, exceptions=(Exception,)):
    """
    重试装饰器

    :param func: 需要重试的函数
    :param retries: 重试次数，默认为3次
    :param delay: 初始延迟时间，单位为秒，默认不等待
    :param backoff: 延迟时间的增加倍数，默认为2，意味着每次重试之间的延迟会指数增长
    :param exceptions: 需要捕获并触发重试的异常类型，默认为所有Exception的子类
    """

    def wrapper(*args, **kwargs):
        attempt = 0
        while attempt <= retries:
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                print(f'Attempt {attempt + 1} failed with error: {e}')
                if attempt < retries:
                    wait_time = delay * backoff ** attempt
                    print(f'Retrying in {wait_time} seconds...')
                    time.sleep(wait_time)
                    attempt += 1
                else:
                    raise  # 如果达到最大重试次数，抛出最后一次的异常

    return wrapper
