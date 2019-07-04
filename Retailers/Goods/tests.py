import hashlib
import re

a='ll'
password=hashlib.sha1(a.encode('utf8')).hexdigest()
print(password)