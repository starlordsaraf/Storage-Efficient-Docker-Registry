sudo docker pull $1
sudo docker save $1 > $1.tar
gzip $1.tar
