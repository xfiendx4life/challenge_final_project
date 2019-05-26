import hashlib
s=input()
imao=hashlib.sha256(s.encode('utf-8')).hexdigest()
print(imao)

