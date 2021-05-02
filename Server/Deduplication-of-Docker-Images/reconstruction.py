import json
import os
import sys
import shutil
import time


def get_image_data(image_name):
    '''
    Gets files needed for val;id images.
    Parameters <str>:
        image_name: name of the image being pulled
    Returns <List>:
      [..] : List of file hashes required to reconstruct the image
    '''
    image_index_path = os.getcwd()+'/image_index.json'
    fs = open(image_index_path,'r')
    image_data = fs.read()
    image_index = json.loads(image_data)
    return(image_index[image_name])
    
        

def reconstruct(image_name, image_data):
    '''
    Uses image_index.json and metadat.json to recinstruct the image file system.
    Parameters <str,list>:
        image_name: name of image being reconstructed
        image_data: list of hashes of the files required to reconstruct the image directory
    Returns:
        None
    '''
    metadata_path = os.getcwd()+'/metadata.json'
    f = open(metadata_path,'r')
    data = f.read()
    metadata = json.loads(data)

    for hash_val in image_data:
        src = metadata['files'][hash_val]['registry_path']        # get path of file in registry
        for dest in metadata['files'][hash_val][image_name]:      
            os.makedirs(os.path.dirname(dest), exist_ok=True)     # creates the file system
            shutil.copy(src, dest)                                # copies the file from registry to directory

    

if __name__=="__main__":
    image_name = sys.argv[1]
    print("Reconstructing "+image_name+" ...")
    start_time = time.time()
    registry_path = os.getcwd()+'/registry'
    image_data = get_image_data(image_name)        #checks if requested image has been pushed 
    reconstruct(image_name,image_data)
    print("\n\n for "+image_name+" :\n")
    print("took %s seconds to reconstruct image from the registry\n\n" % (time.time() - start_time))
    print('Reconstruction Successfull')



