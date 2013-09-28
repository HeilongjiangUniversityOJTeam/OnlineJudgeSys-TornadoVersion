#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis
import os
import json
from configure import REDIS_HOST
from judge import Judge


def GetRequest(queue):
    '''
    获取判题请求接口(阻塞接口)
    从内存队列(redis)中取得
    '''
    return queue.blpop('request')[1]


def GetDataFile(problem_id):
    pass


def InitLocalData(data_file_status):
    '''
    远程判题机 初始化函数
    初始化保证判题数据在本地存在
    '''
    dir = './DataFile/'
    for folders in os.listdir(dir):
        tf = os.path.join(dir, folders)
        print tf
        if os.path.isdir(tf):
            data_file_status.append(int(folders))


def CleanTemp():
    '''
    判题完成后清理临时文件接口实现
    判题临时文件放在judger文件夹下Temp目录中
    '''
    Dir = "./Temp/"
    files = os.listdir(Dir)

    for fs in files:
        print fs
        tfile = os.path.join(Dir, fs)
        if os.path.isfile(tfile):
            os.remove(tfile)
        else:
            print "delete file error."
    else:
        print 'clear done.'


def InitDir():
    from configure import COMPILER_DIR, DATA_DIR, SOURCE_CODE_DIR

    if not os.path.exists(COMPILER_DIR):
        os.makedirs(COMPILER_DIR, 0744)
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, 0744)
    if not os.path.exists(SOURCE_CODE_DIR):
        os.makedirs(SOURCE_CODE_DIR, 0744)


def LocalMain():
    '''
    本地判题服务接口
    '''
    queue = redis.Redis(host=REDIS_HOST)

    InitDir()

    while True:
        info = json.loads(GetRequest(queue))
        msg = json.dumps(Judge(info))
        CleanTemp()
        queue.rpush('result', msg)


def Main():
    '''
    queue = redis.Redis(host=REDIS_HOST)
    data_file_status = []

    Init(data_file_status)

    while True:
        info  = json.loads(GetRequest(queue))

        id = info['problem_id']

        if id not in data_file_status:
            if GetDataFile(id):
                data_file_status.append(id)
            else:
                print 'get data file %d error.' % id
                continue

        queue.rpush(json.dumps('result',Judger(info)))
    '''
    pass


if __name__ == '__main__':
    if REDIS_HOST == 'localhost' or REDIS_HOST == '127.0.0.1':
        LocalMain()
    else:
        Main()