# Docker
# run docker
docker compose -f "docker/docker-compose.yml" up -d --build

# stop all running containers
sudo docker stop $(sudo docker ps -aq)

# remove all containers
sudo docker rm $(sudo docker ps -aq)

# remove all images
sudo docker rmi $(sudo docker images -q)

# remove all volumes
sudo docker volume rm $(sudo docker volume ls -q)

# clean up everything
sudo docker system prune --all


# PGvector service
docker pull pgvector/pgvector:0.8.0-pg17-trixie
docker volume create pgvector_data
docker run --name pgvector -e POSTGRES_PASSWORD=admin1 -p 5432:5432 -v pgvector_data:/var/lib/postgresql/data -d pgvector/pgvector:0.8.0-pg17-trixie


# Container & Building
# Build the app
sudo docker compose up --build

# Go inside a container in docker
sudo docker compose exec fastapi bash


# Azure  & Deployment
# Change file permissions
chmod 600 mini-rag-dev_key.pem

# Connect to the server using SSH
ssh -i mini-rag-dev_key.pem azureuser@74.162.64.171

# See server capabilities and status
sudo apt update
sudo apt install htop
htop

# Add a new user
adduser github_user

# Add user to sudo group
sudo usermod -aG sudo github_user

# Check the current user name
whoami

# Switch the user
sudo su - github_user

# Generate SSH key to access the github user
ssh-keygen -t rsa -b 4096 -C "github_user_key" -f ~/.ssh/github_user_key -N ""

# Copy private key
scp -i mini-rag-dev_key.pem azureuser@74.162.64.171:/home/azureuser/github_user_key .

# Port Forwarding
ssh -i mini-rag-2_key.pem -L 4000:localhost:3000 azureuser@20.174.3.18


# Service
# Realod system services
sudo systemctl daemon-reload

# Start a new service
sudo systemctl start minirag.service

# check service status
sudo systemctl status minirag.service

# Show logs
sudo journalctl -u minirag -f

# Enable service on system boot
sudo systemctl enable minirag.service