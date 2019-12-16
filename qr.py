# -*- coding: utf-8
# генератор Qr кодов


# импорт библиотеки
import pyqrcode  # sudo pip3 install pyqrcode
import png  # sudo pip3 install pypng


def main():
    lst = []
    for i in range(1, 29):
        code = pyqrcode.create('http://qvest.asspo.ru/cgi-bin/lut.py?idLut={}'.format(i))
        image_as_str = code.png_as_base64_str(scale=6)
        str = ''
        str += '<div class="layer1"><img width="200" height="200"  src="data:image/png;base64,{}"> \n'.format(image_as_str)
        str += '<p align="center">{}</p></div> \n'.format(i)
        lst.append(str)
    return lst



if __name__ == "__main__":
    web = main()