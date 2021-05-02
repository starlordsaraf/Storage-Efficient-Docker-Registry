<<///
This script retrives the file systems of existing images to be deduplicated.
Argument passed : $1 < Docker_image_name:image_version >
                  $2 <Path of .tar.gz file pushed by client>

Run Command: 
    Deduplication-of-Docker-Images/./push_driver.sh <DockerImage name>
///

cd /home/ubuntu/flaskapp/uploads
mkdir $1
tar -xvf $2 -C $1  
rm $2

find $1/ -type f -iname "*.tar" -print0 -execdir tar xf {} \; -delete
# echo "size of original image directory for $1 :" >> test_out.txt
# du -h $1 | tail -n 1  >> test_out.txt                    #size of original directory
# du $1 | tail -n 1 >> test_out.txt
cd ..
python3 Deduplication-of-Docker-Images/deduplicate.py $1
echo "\n\n"
