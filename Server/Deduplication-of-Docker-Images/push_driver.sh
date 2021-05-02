<<///
Driver script for push to the registry.
1. Deduplication is performed after each push is made to the registry.
2. The newly pushed Docker Image is the argumnet sent to the applicaton.
3. The registry directory is created.
4. metadata.json is maintained to store information of each unique file in the registry.
5. image_index.json tracks the hashed files used by each pushed image, used during reconstruction for pulls.

Run Command: 
    chmod +x Deduplication-of-Docker-Images/setup.sh
    Deduplication-of-Docker-Images/./setup.sh <DockerImage name>
///

mkdir -p registry 
echo "size of registry before $1 is pushed :" >> test_out.txt
du -h registry | tail -n 1 >> test_out.txt
du registry | tail -n 1 >> test_out.txt

mkdir -p pop_registry

#create metadata file if it doesn't exist
if [ -e metadata.json ];
then
    echo "Metadata File exists"
else
    touch metadata.json
    echo "Metadata File created"
fi

#create image index file if it doesn't exist
if [ -e image_index.json ];
then
    echo "Image Index File exists"
else
    touch image_index.json
    echo "Image Index File created"
fi

#create popularity.json index file if it doesn't exist
if [ -e popularity.json ];
then
    echo "Popularity.json exists"
else
    touch popularity.json
    echo {'total':0} > popularity.json
    echo "Popularity.json file created"
fi

#create list_pop_images file if it doesn't exist
if [ -e list_pop_images.json ];
then
    echo "list_pop_images exists"
else
    touch list_pop_images.json
    echo {'images':[]} > list_pop_images.json
    echo "list_pop_images.json file created"
fi

#run file retrieval script
chmod +x Deduplication-of-Docker-Images/deduplicate_driver.sh
Deduplication-of-Docker-Images/./deduplicate_driver.sh $1 $2