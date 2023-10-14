# pylint:disable = all
import platform


def get_info(rattan_gcov):
    x = 5
    if platform.system() == "Linux":
        x = 4
    return list(map(lambda x : (x.split(':')[0].strip().rstrip()), rattan_gcov.splitlines()))[x:]
