import os
import sys
import hashlib

def make_hash_files(image_path, image_name):
    hash_file = open(image_name+".txt","w+")
    for folder, subfolders, files in os.walk(image_path):
        for file_name in files:
            filePath = os.path.abspath(os.path.join(folder, file_name))                     #file path in image
            try:
                with open(filePath,'rb') as f:
                    data = f.read()
                    readable_hash = hashlib.sha256(data).hexdigest()     
                    hash_file.write(readable_hash)
            except:
                continue
    





if __name__=="__main__":
    image_name = sys.argv[1]
    image_path = os.getcwd()+'/'+image_name
    make_hash_files(image_path,image_name)