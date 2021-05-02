import os
import sys
import hashlib
import json
import shutil
import time


def update_metadata(image_path, image_name):
    '''
    Updates metadata.json by parsing all the files of the pushed image.
    Each file is hashed using SHA256 encoding and metadata.json is updated based
    on the following criteria:
    1. new file, new image, new path: a new record is created with the hash as the key.
    2. old file, new image, new path: the record of the file is updated for image and path.
    3. old file, old image, new path: the record of the file and it's image is updated for path.
    4. old file, old image, old path: no changes, arises when same image is pushed twice.
    Paramters <str,str>:
        image_path: path of the temporary directory made on pushing a new image.
        image_name: name of the image pushed
    Returns:
        None

    '''
    metadata_path = os.getcwd()+'/metadata.json'
    f = open(metadata_path,'r')
    data = f.read()
    if(data):
        metadata = json.loads(data)
    else:
        metadata = dict()
        metadata['files'] = dict()
        metadata['file_count'] = 0
    

    image_index_path = os.getcwd()+'/image_index.json'
    fs = open(image_index_path,'r')
    image_data = fs.read()
    if(image_data):
        image_index = json.loads(image_data)
    else:
        image_index = dict()
        
    if(image_name not in image_index):
        image_index[image_name] = []

    for folder, subfolders, files in os.walk(image_path):
        for file_name in files:
            filePath = os.path.abspath(os.path.join(folder, file_name))                     #file path in image
            try:
                with open(filePath,'rb') as f:
                    data = f.read()
                    readable_hash = hashlib.sha256(data).hexdigest()                            #sha256 hash of file

                    if(readable_hash not in metadata['files']):                                 #completely new file
                        metadata['file_count']+=1                                               #increment number of unique files
                        metadata['files'][readable_hash] = dict()
                        metadata['files'][readable_hash][image_name] = dict()
                        metadata['files'][readable_hash][image_name] = [filePath]
                        registry_file_path = update_registry(filePath, metadata['file_count'])  #add file to registry and get new path
                        metadata['files'][readable_hash]['registry_path'] = registry_file_path

                    else:
                        if(image_name not in metadata['files'][readable_hash]):                 #file exists but for a different image
                            metadata['files'][readable_hash][image_name] = [filePath]
                        else:   
                            if(filePath not in metadata['files'][readable_hash][image_name]):   #file exists for this image but for a different path
                                metadata['files'][readable_hash][image_name].append(filePath)
                
                    if(readable_hash not in image_index[image_name]):                           #update image indices
                        image_index[image_name].append(readable_hash)
            except:
                continue

                

    #print(json.dumps(metadata, indent = 4))

    with open(metadata_path, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=4, sort_keys=True)
    
    with open(image_index_path, 'w') as image_index_file:
        json.dump(image_index, image_index_file, indent=4, sort_keys=True)



def update_registry(file_path, file_count):
    '''
    Updates the main registry with the unique files.
    Parameters <str,int>:
        file_path: path of the file in temporary directory of the pushed image
        file_count: total number of unique files in the registry
    Returns <str>:
        path of file in the registry
    '''
    src = file_path
    registry_file_name = file_path.split('/')[-1]                     #get name of actual file
    dst = registry_path+"/"+str(file_count)+"_"+registry_file_name    #create incremental name for file
    shutil.copy(src,dst)
    return(dst)



def teardown():
    '''
    Deletes the temporary file made for the image after updating the registry.
    '''
    shutil.rmtree(image_path)


if __name__=="__main__":
    print("Deduplicating registry..........\n")
    start_time = time.time()
    image_name = sys.argv[1]
    image_path = os.getcwd()+'/uploads/'+image_name
    registry_path = os.getcwd()+'/registry'
    update_metadata(image_path,image_name)
    teardown()
    print("\n\n for "+image_name+" :\n")
    print("took %s seconds to push image to the registry\n\n" % (time.time() - start_time))


