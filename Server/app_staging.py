from flask import Flask
from flask import send_file
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for
import os
import subprocess
import json
import datetime
import shutil

from flask_caching import Cache
import redis

app = Flask(__name__)

CACHE_FOLDER = '/home/ubuntu/flaskapp/cache'
UPLOAD_FOLDER = '/home/ubuntu/flaskapp/uploads'
ALLOWED_EXTENSIONS = {'tar', 'tar.gz'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CACHE_FOLDER'] = CACHE_FOLDER
app.config['MAX_CACHE_SIZE'] = 500
app.config['CURR_CACHE_SIZE'] = 0

def allowed_file(filename):
    return '.' in filename and \
           filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_in_cache(image_name):
    fs = open("cache.json",'r')
    cache_data = fs.read()
    cached_files = json.loads(cache_data)
    fs.close()
    if(image_name in cached_files):
        return(True)
    else:
        return(False)

def update_existing_cache(image_name):
    with open("cache.json","r") as cache_file:
        cache_data = json.load(cache_file)
    cache_data[image_name] = str(datetime.datetime.now())
    with open("cache.json", "w") as cache_file:
        json.dump(cache_data, cache_file)

def set_cache(image_name,image_size):
    with open("cache.json","r") as cache_file:
        cache_data = json.load(cache_file)
    if(app.config['MAX_CACHE_SIZE']-app.config['CURR_CACHE_SIZE'] >= image_size): #cache has space
        cache_data[image_name] = str(datetime.datetime.now())
        app.config['CURR_CACHE_SIZE']+=image_size
    else:   #cache eviction happens
        cache_sorted = sorted(cache_data, key = lambda x: datetime.datetime.strptime(cache_data[x], "%Y-%m-%d %H:%M:%S.%f"))
        index = 0
        while(app.config['MAX_CACHE_SIZE']-app.config['CURR_CACHE_SIZE'] < image_size):
            lru_image = cache_sorted[index]
            print(lru_image+" is evicted from cache")
            cache_data.pop(lru_image)
            image_file = app.config['CACHE_FOLDER']+'/'+lru_image+'.tar.gz'
            app.config['CURR_CACHE_SIZE'] -= os.path.getsize(image_file)
            os.remove(image_file)
            index+=1
        cache_data[image_name] = str(datetime.datetime.now())
        app.config['CURR_CACHE_SIZE']+=image_size

    print("Current Cache Size: (in bytes)",app.config['CURR_CACHE_SIZE'])
    with open("cache.json", "w") as cache_file:
        json.dump(cache_data, cache_file)
    original = app.config['UPLOAD_FOLDER']+'/'+image_name+'.tar.gz'
    target = app.config['CACHE_FOLDER']+'/'+image_name+'.tar.gz'
    shutil.copyfile(original, target)
    print(image_name +" is set to cache")
        



@app.route('/push', methods = ['POST'])
def push_image():
    if ('file' not in request.files):
        return ("No file sent", 400)

    file = request.files['file']

    if (file.filename == ''):
        return ("No filename given to the sent file", 400)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       
        image_name = filename.split('.')[0]

        subprocess.run("Deduplication-of-Docker-Images/./push_driver.sh "+str(image_name)+" "+str(app.config['UPLOAD_FOLDER'])+"/"+str(filename),shell=True)
        return ("Image sucessfully pushed", 200)
    
    return("Incorrect file format", 400)


@app.route('/pull', methods=['GET'])
def pull_image():
    image_name = request.args.get('image')
    fs = open("image_index.json",'r')
    image_data = fs.read()
    if(image_data):
        image_index = json.loads(image_data)
        if(image_name in image_index):

            #Update popularity
            with open("popularity.json","r") as pop_file:
                pop_json = json.load(pop_file)
            pop_json["total"] += 1
            if image_name not in pop_json:
                pop_json[image_name] = 1
            else:
                pop_json[image_name] += 1
            print("popularity file ",pop_json)
            with open("popularity.json", "w") as pop_file:
                json.dump(pop_json, pop_file)
            
            #Open image list file
            pop_path = os.getcwd()+'/list_pop_images.json'
            fs2 = open(pop_path,'r')
            data = fs2.read()
            im_data = json.loads(data)
            lst_img = im_data["images"]
            fs2.close()

            #check if image in cache
            if(image_in_cache(image_name)):
                print(image_name+" is in cache")
                update_existing_cache(image_name)
                fileobj = open(app.config['CACHE_FOLDER']+'/'+image_name+'.tar.gz', 'rb')
            else:
                print(image_name + " is not in cache")
                #check if image in uploads
                if image_name in lst_img:
                    print(image_name + " is popular")
                else:
                    print(image_name + " is not popular")
                    subprocess.run("Deduplication-of-Docker-Images/./pull_driver.sh "+str(image_name), shell=True)
                
                image_file = app.config['UPLOAD_FOLDER']+'/'+image_name+'.tar.gz'
                fileobj = open(image_file, 'rb')
                image_size = os.path.getsize(image_file)
                if(image_size<app.config['MAX_CACHE_SIZE']):
                    set_cache(image_name,image_size)


            
            #update pop_registry if required
    
            pop_path2 = os.getcwd() + '/popularity.json'
            fs3 = open(pop_path2,'r')
            data = fs3.read()
            pop_data = json.loads(data)
            total = pop_data["total"]
            my_pop = pop_data[image_name]
            fs3.close()

            threshold = 0.2
            pop_frac = int(my_pop)/int(total)
            
            if pop_frac >= threshold:
                if image_name in lst_img:
                    #was not added in uploads
                    pass
                else:
                    #added by reconstruction.py
                    lst_img.append(image_name)
                    with open(pop_path,"w") as pop_file2:
                         json.dump(im_data, pop_file2)
            else:
                if image_name in lst_img:
                    #remove folder from list and uploads
                    os.remove(app.config['UPLOAD_FOLDER']+'/'+image_name+'.tar.gz')
                    lst_img.remove(image_name)
                    with open(pop_path, "w") as pop_file2:
                        json.dump(im_data, pop_file2)
                else:
                    #remove only from uploads
                    os.remove(app.config['UPLOAD_FOLDER']+'/'+image_name+'.tar.gz')
            
            return send_file(fileobj,mimetype='application/zip')
        else:
            return("Requested image doesn't exist", 404)
    return("Registry is empty", 404)



@app.route('/test_one')
def hello_one():
    # return 'Hello, One . Welcome!'
    fileobj = open('test.zip', 'rb')
    return send_file(fileobj,mimetype='application/zip') 

@app.route('/test_two')
def hello_two():
    return 'Hello, Two . Welcome!'


if __name__ == '__main__':
    app.run()
