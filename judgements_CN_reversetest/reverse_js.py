#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   reverse_js.py
@Time    :   2019/03/12 17:06:01
'''

# here put the import lib
import execjs
import os


def create_guid():
    """This function is for create guid
    
    Returns:
        string -- uid
    """

    paths = os.path.dirname(__file__)
    # print(paths)
    file_path = paths + '/ListContentPage/g_uid.js'
    ctx = execjs.compile(open(file_path).read())
    uid = ctx.call('ref')
    print("g_uid is: %s" %uid)
    return uid


def create_cookie_key():
    """This function is for create cookie_key
    
    Returns:
        string -- cookie_key
    """

    paths = os.path.dirname(__file__)
    # print(paths)
    file_path = paths + '/get_key.js'
    ctx = execjs.compile(open(file_path).read())
    key = ctx.call('getKey')
    print("cookie_key is: %s" %key)
    return key


if __name__ == "__main__":
    create_guid()
    create_cookie_key()




