from flask import Flask
from flask import send_file
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for
import os
import subprocess
import json

app = Flask(__name__)

UPLOAD_FOLDER = '/home/ubuntu/flaskapp/uploads'
ALLOWED_EXTENSIONS = {'tar', 'tar.gz'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
       # with open("popularity.json","r") as pop_file:
       #     pop_json = json.load(pop_file)
        image_name = filename.split('.')[0]

        #pop_json["total"] += 1

        '''if image_name not in pop_json:
            pop_json[image_name] = 1
        else:
            pop_json[image_name] += 1
        print("popularity file ",pop_json)
        with open("popularity.json", "w") as pop_file:
            json.dump(pop_json, pop_file)'''

        subprocess.run("Deduplication-of-Docker-Images/./push_driver.sh "+str(image_name)+" "+str(app.config['UPLOAD_FOLDER'])+"/"+str(filename),shell=True)
        return ("Image sucessfully pushed", 200)
    
    return("Incorrect file format", 400)

@app.route('/pull', methods=['GET'])
def pull_image():
    image_name = request.args.get('image')
    fs = open("image_index.json",'r')
    image_data = fs.read()
    if(image_data):
        with open("popularity.json","r") as pop_file:
            pop_json = json.load(pop_file)
        #image_name = filename.split('.')[0]

        pop_json["total"] += 1

        if image_name not in pop_json:
            pop_json[image_name] = 1
        else:
            pop_json[image_name] += 1
        print("popularity file ",pop_json)
        with open("popularity.json", "w") as pop_file:
            json.dump(pop_json, pop_file)

        image_index = json.loads(image_data)
        if(image_name in image_index):
            
            #check if image in uploads
            pop_path = os.getcwd()+'/list_pop_images.json'
            fs2 = open(pop_path,'r')
            data = fs2.read()
            im_data = json.loads(data)
            lst_img = im_data["images"]
            fs2.close()
            
            if image_name in lst_img:
                pass
            else:
                subprocess.run("Deduplication-of-Docker-Images/./pull_driver.sh "+str(image_name), shell=True)
            fileobj = open(app.config['UPLOAD_FOLDER']+'/'+image_name+'.tar.gz', 'rb')
            
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
