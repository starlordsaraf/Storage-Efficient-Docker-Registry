import requests, zipfile, io
import json
import os
import sys

#files = {'file': open('test.tar.gz','rb'),'image_name':'test'}

files = {'file': open(sys.argv[1],'rb')}

r = requests.post("http://3.94.193.223:8080/push", files=files)

print(r.text)
