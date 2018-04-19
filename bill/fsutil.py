# coding=utf8

import hashlib
import os
import datetime
import random
import pdb 

 
def handle_uploaded_file(path, stream):
    shortname, ext = os.path.splitext(stream.name)
    
    if ext == '.xls':
        f = open(path, 'wb')
        for chunk in stream.chunks():
            f.write(chunk)
        f.close()
        return path
    else:
        return -1
 
