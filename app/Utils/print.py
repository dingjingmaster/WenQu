
class Print(object):
    def __init__(self):
        pass

    # 前景色:红色 背景色:默认
    def red(self, s):
        print('\033[0;31;40m' + s + '\033[0m')

    # 前景色:绿色 背景色:默认
    def green(self, s):
        print('\033[0;32;40m' + s + '\033[0m')

    # 前景色:黄色 背景色:默认
    def yellow(self, s):
        print('\033[0;33;40m' + s + '\033[0m')

    # 前景色:蓝色 背景色:默认
    def blue(self, s):
        print('\033[0;34;40m' + s + '\033[0m')

    # 前景色:洋红色 背景色:默认
    def magenta(self, s):
        print('\033[0;35;40m' + s + '\033[0m')

    # 前景色:青色 背景色:默认
    def cyan(self, s):
        print('\033[0;36;40m' + s + '\033[0m')


colorPrint = Print()
