#pushes image to registry
chmod +x Deduplication-of-Docker-Images/push_driver.sh
Deduplication-of-Docker-Images/./push_driver.sh $1

#reconstructs image from registry
chmod +x Deduplication-of-Docker-Images/pull_driver.sh
Deduplication-of-Docker-Images/./pull_driver.sh $1