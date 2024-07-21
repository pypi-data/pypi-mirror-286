# -*- coding: utf-8 -*-
import re
import time
import functools
import traceback


def get_features(message: str, lora_name: str = None):
    feature = {
        "message": message,
        "max_input_len": 10240,
        "max_output_len": 10240,
        "lora_name": lora_name,
    }
    return [feature]


def extract_json_content(text):
    # 正则表达式匹配 json 和之间的内容
    pattern = r"```json\s+(.*?)\s+```"
    # 使用re.search找到第一个匹配的内容
    match = re.search(pattern, text, re.DOTALL)
    if match:
        # 返回匹配的内容
        return match.group(1)
    else:
        return text


def retry(tries=10, wait=1, backoff=2, exceptions=(Exception,)):
    """Configurable retry decorator, Useage:

    @retry(tries=3)
    def func():
       pass

    This is equivalent to:  func = retry(retries=3)(func)
    """

    def dec(function):
        @functools.wraps(function)
        def function_with_retry(*args, **kwargs):
            current_wait = wait
            count = 1
            while True:
                try:
                    return function(*args, **kwargs)
                except exceptions as e:
                    if wait == 0:
                        msg = f"failed to call {function.__name__}, info: {e}"
                        print(msg)
                        traceback.print_exc()
                        raise
                    else:
                        if count < tries or tries < 0:
                            if tries < 0:
                                msg = f"failed to call {function.__name__} [{count}/Inf], info: {e}"
                            else:
                                msg = f"failed to call {function.__name__} [{count}/{tries}], info: {e}"
                            print(msg)
                            time.sleep(current_wait)
                            current_wait *= backoff
                            if kwargs is None:
                                kwargs = {}
                            kwargs["retry"] = tries - count
                            count += 1
                        elif count == tries:
                            msg = f"failed to call {function.__name__} [{count}/{tries}], info: {e}"
                            print(msg)
                            raise e

        return function_with_retry

    return dec
