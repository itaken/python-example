#! /usr/bin/python3
from io import BytesIO
from captcha.image import ImageCaptcha

'''
   生成验证码
   @since 2017-02-27
   @link https://pypi.python.org/pypi/captcha
         https://github.com/lepture/captcha
'''

image = ImageCaptcha(fonts=[])

captcha_str = "test"

data = image.generate(captcha_str)
assert isinstance(data, BytesIO)

image.write(captcha_str, "./output/captcha.png")
