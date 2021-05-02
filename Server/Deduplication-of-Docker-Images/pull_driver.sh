<<///
Driver script for pull to the registry
1. files are gathered from the registry based on metadata.json and image_index.json 
   for reconstruction of the image directory.
2. The reconstructed directory is converted to a tar ball 
3. The tar ball is loaded to Docker as an image.

Run Command: 
    chmod +x Deduplication-of-Docker-Images/pull_driver.sh
    Deduplication-of-Docker-Images/./pull_driver.sh <DockerImage name>
///


python3 Deduplication-of-Docker-Images/reconstruction.py $1    # reconstructs the image file system

cd uploads
tar -cvf $1.tar -C $1 $(ls $1)             # convert to .tar file
gzip $1.tar
rm -rf $1
cd ..
echo "$1 successfully sent"