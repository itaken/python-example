#!/usr/bin/env python3

import os

f = open("text.txt", "r+")

c = f.read(3)

print(f.fileno(), f.closed, f.mode)

print(c)

print(f.tell()) # 当前文件指针

f.seek(0, os.SEEK_SET)  # 指向头部

# f.seek(-3, os.SEEK_CUR)  # 当前位置 回退

print(f.tell())

f.close()
