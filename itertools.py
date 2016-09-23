import itertools as its
#words = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
words = "ABCDE"
r = its.product(words,repeat=3)
dic = open("pass.txt","a")
for i in r:
    dic.write("".join(i))
dic.close()