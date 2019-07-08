import  hashlib
a='ll'
b=hashlib.sha1(a.encode('utf8')).hexdigest()
print(b)