<<///
Script to get hash of all files in a directory
Directory name is passed as the argument
Hashes are sent to a text file will same name as the directory.

Run Command:
    chmod +x GetHashOfAllFiles.sh
    ./GetHashOfAllFiles.sh <dir_name>
///

for i in $(find $1 -type f);
do 
    sha256sum $i;
done > $1.txt