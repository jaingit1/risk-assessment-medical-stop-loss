# Initialize a new Git repository
git init

# Add all files to the staging area
git add .

# Commit the files
git commit -m "Initial commit"

# Add the remote repository (replace <username> and <repository> with your GitHub username and repository name)
git remote add origin https://github.com/jaingit1/risk-assessment-medical-stop-loss.git

# Push the changes to the remote repository
git push -u origin master


# Run the docker image pushed to aws ecr locally
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 445567073878.dkr.ecr.us-east-1.amazonaws.com

docker pull 445567073878.dkr.ecr.us-east-1.amazonaws.com/risk-assessment-ecr-repository:latest

docker run -p 5000:5000 445567073878.dkr.ecr.us-east-1.amazonaws.com/risk-assessment-ecr-repository:latest

# Check connect to eks
aws eks update-kubeconfig --region us-east-1 --name risk-assessment-eks-cluster-development

# get service details
kubectl get svc

# get pods
kubectl get pods

# manual cleanup
Load Balancer, Network Interface, vpc 

# Build docker image
docker build -t streamlit-risk-assessment .\webapp_container\

# Run docker container
docker run -p 8501:8501 streamlit-risk-assessment
