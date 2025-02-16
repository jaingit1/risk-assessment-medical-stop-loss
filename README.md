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
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com
docker pull <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/<your-repo-name>:latest
docker run -p 5000:5000 <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/<your-repo-name>:latest
