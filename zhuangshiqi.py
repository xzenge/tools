#-*- encoding: utf-8 -*-
############含有一个装饰器#########
# def outer(func):
#     def inner(*args, **kwargs):  # 要装饰f1（），这里用这俩形式参数，可以接受任意个参数，不管f1定义几个参数
#         print "1"
#         r = func(*args, **kwargs)  # 这里要用func，不要用f1
#         print "2"
#         return r
#
#     return inner
#
#
# @outer  # 这里outer不要加括号
# def f1(a1, a2):
#     print "a1 + a2 = "
#     return a1 + a2
#
#
# f1(1, 2)
#

############含有二个装饰器#########

def outer0(func):  # 第一个
    def inner(*args, **kwargs):
        print "AAAAAAAAA"
        r = func(*args, **kwargs)
        print "BBBBBBBB"
        return r

    return inner


def outer(func):  # 第二个
    def inner(*args, **kwargs):  # 要装饰f1（），这里用这俩形式参数，可以接受任意个参数，不管f1定义几个参数
        print "1"
        r = func(*args, **kwargs)  # 这里要用func，不要用f1
        print "2"
        return r

    return inner


@outer0  # 俩装饰器，流程就是：执行f1()的时候，先执行outer0.inner(),outer0.inner().func调用outer的inner函数，也就是outer.inner()函数作为outer0的参数，
# 然后outer.inner().func再调用f1()
@outer  # 这里outer不要加括号
def f1(a1, a2):
    print "a1 + a2 = %d" % (a1 + a2)
    return 1


f1(1, 2)