#!/usr/bin/env python3

f = open("text.txt", "r")

# print(f)

# f.write("Hello")

line = f.readline()  # 读取一行
print(line)

# itf = iter(f)  # 迭代器读取
# for line in itf:
#     print(line)


f.close()


