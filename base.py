import platform
import random
import string


if platform.system() == 'Windows':
    import winreg

user_agent = f"HoMoLab/114.514 (Authcode: {''.join((''.join(random.sample(string.digits + string.ascii_letters, 32))).lower())})"
app_version = '0.0.1'
first_open = True


def systemColorSet():
    """
    从注册表中获取系统颜色
    :return:
    """

    color = '006400'
    light = 1
    return f'{int(color[0:2], 16)}, {int(color[2:4], 16)}, {int(color[4:6], 16)}', light