#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   get_navi_link.py
@Time    :   2019/03/23 17:55:27
'''

# here put the import lib
import execjs
import os

realid = 'd8952be5-e5a2-4b8b-b554-cccf5824617f'
page_id = 'DcOOwrcBACAIBMOAwpVAcilpw7/CkcK0w79wwpdBMDzCqyRYwrvCty/DjwLDjRErwovDi8OXwpNzUWYpDXfDgMKnwo/CgMKKw6tiw6bDjnXDn0DDr8KIZj9lYxHCgsKHGUPDjRRpw7wCbsKawpQOW1BERXnDvEclw4M7woJyNsKxwoY5USfCgcKZwqTCjsOnwrTDiMOPRV/ChcKawrbCgQFhTcOLw4oDHAbDrgXCoMOZw7TCixQgH8OHw7jDgcKfw7gHwo3CkB4='


def create_navi_link():
    """create the navi_link
    
    Returns:
        [str] -- [navi_id]
    """

    paths = os.path.dirname(__file__)
    print(paths)
    file_path = paths + '/GetNaviLink/naviLink.js'
    print(file_path)
    ctx = execjs.compile(open(file_path).read())
    navi_id = ctx.call('Navi', page_id)
    print("navi_id is: %s" % navi_id)
    return navi_id


if __name__ == "__main__":
    create_navi_link()
