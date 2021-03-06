#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import redis
import pymongo
import threading
import time

sync_queue = redis.Redis(host='localhost')


class MongoScannerThreading(threading.Thread):
    '''
    数据库扫描线程
    定时扫描数据库中为未处理的请求
    PS:目前编写的为临时版本,定时提取数据库中所有的为处理的文件加入内存队列
    目标实现增量提交
    '''

    def __init__(self, p, mongodb, redisdb):
        threading.Thread.__init__(self)
        self.period = p
        self.mongo_db = mongodb
        self.redis_db = redisdb

    def scanner(self):
        requests = self.mongo_db.judge_queues.find({'result': None})

        for item in requests:
            problem = self.mongo_db.problems.find_one({'_id': item['problem_id']})
            req = {
                '_id': item['_id'],
                'problem_id': item['problem_id'],
                'language_type': item['language_type'],
                'time_limit': problem['time_limit'],
                'memory_limit': problem['memory_limit'],
                'source_file_name': item['code_file'].split('/')[-1],
                'data_files': problem['data_files']
            }
            #print req
            self.redis_db.rpush('request', json.dumps(req))

    def run(self):
        while True:
            #print 'scanner start...',
            #print time.strftime("%Y-%m-%d %A %X", time.localtime())
            self.scanner()
            time.sleep(self.period)


class ResultListenerThreading(threading.Thread):
    '''
    提交处理结果内存队列监听线程
    目前实现的为同步接口,等待内存队列中有新的结果后,将其处理添加到数据库中
    未来新增异步接口,提供判题结果异步处理
    '''

    def __init__(self, mongodb, redisdb):
        threading.Thread.__init__(self)
        self.mongo_db = mongodb
        self.redis_db = redisdb

    def run(self):
        while True:
            res = self.redis_db.blpop('result')[1]
            res = json.loads(res)

            request = self.mongo_db.judge_queues.find_one({'_id': res['_id']})
            if not request:
                print 'result id error,do not exist id %d.' % res['_id']
                continue
            del res['_id']
            request['result'] = res

            problem = self.mongo_db.problems.find_one({'_id': request['problem_id']})
            if not problem:
                print 'problem not found.'
                continue
            problem['info'][res['type']] += 1

            user = self.mongo_db.users.find_one({'user_name': request['user_name']})
            if not user:
                print 'user find err'
                continue
            user['info'][res['type']] += 1
            if res['type'] == 'Yes':
                if request['problem_id'] not in user['solved']:
                    user['solved'].append(request['problem_id'])
                if request['problem_id'] in user['trying']:
                    user['trying'].remove(request['problem_id'])
            else:
                if request['problem_id'] not in (user['solved'] + user['trying']):
                    user['trying'].append(request['problem_id'])

            self.mongo_db.problems.save(problem)
            self.mongo_db.users.save(user)
            self.mongo_db.judge_queues.save(request)


def AddRequest(req):
    '''
    向请求内存队列添加新的请求接口
    '''
    global sync_queue
    sync_queue.rpush('request', req)


def main():
    '''
    判题核心进程
    包含两个子线程
    scan_threading: 扫描数据库未处理请求线程
    answer_threading: 判题结果处理线程
    '''
    global sync_queue
    request_db = pymongo.Connection('localhost', 27017).Gaea

    scan_threading = MongoScannerThreading(120, request_db, sync_queue)
    scan_threading.setDaemon(True)
    scan_threading.start()

    answer_threading = ResultListenerThreading(request_db, sync_queue)
    answer_threading.setDaemon(True)
    answer_threading.start()

    while True:
        cmd = raw_input()
        if cmd == 'exit':
            break


if __name__ == '__main__':
    main()