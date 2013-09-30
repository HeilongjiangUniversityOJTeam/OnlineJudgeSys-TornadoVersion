# -*- coding:utf-8 -*-
import base64


def coding(source):
    '''
    字符串加密函数
    '''
    return base64.encodestring(source)


def uncoding(source):
    '''
    密码反向解密函数
    '''
    return base64.decodestring(source)


def FilesWriter(file_name, words):
    with open(file_name,"w") as file:
        file.write(words)


def MongoFileWriter(file):

    return

def MongoBytesFileWriter(bytes):

    return