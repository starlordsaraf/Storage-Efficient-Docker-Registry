# Storage-Efficient-Docker-Registry
A deduplicated Docker registry that improves storage

 The registry contains the scripts for both Client and Server machines to setup and interact with the Docker registry.
# Server
    a. app.py - Script for only file level deduplicated Docker Regsitry (Basic Implementation)
    b. app_pop.py - Script for deduplicated registry with Popularity Based Storage (Intermediate Implementation)
    c. app_staging.py - Script for deduplicated registry with Popularity Based Storage and Time Based Staging Storage (Final most efficient implementation)
## To use the storage efficient Docker Registry on a remote server :
1. Pull this git repo on the server machine and use the Sever folder.
2. Setup nginx and GUnicorn setup to run the server remotely .
3. Ensure the machine has TCP port for incoming and outgoing requests at port 80.
4. Start nginx server using : sudo service nginx start
5. Start Flask server via Gunicorn for the Final Implemenatation: gunicorn3 --timeout 1000 app_staging:app
6. The version of the application can be run by changing the script name in the gunicorn command.


# Client
## To push an image to the remote Registry
1. Pull the Client folder code of the repo on the client machine. 
2. If the image is to be retrived from DockerHub run, ./get_image.sh image_name. This generates the .tar.gz file for the given image
2. To push the image run, python3 push_client.py image.tar.gz

## To pull an image from the remote registry
1. Open a client like a web browser or any other machine and make a call to the server as follows:
    http://server_ip:8080/pull?image=imagename
2. The image will be recieved by the machine and the download starts.
