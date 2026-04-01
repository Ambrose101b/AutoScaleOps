pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                // This pulls the latest code from your GitHub repo
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "Building the AutoScaleOps Docker image..."
                // We build the image and tag it as latest
                sh 'docker build -t autoscaleops-app:latest .'
            }
        }
        
        stage('Clean Up Previous Deployments') {
            steps {
                echo "Removing old containers to make room for the new one..."
                // The '|| true' prevents Jenkins from failing if no container exists yet
                sh 'docker stop autoscale-dashboard || true'
                sh 'docker rm autoscale-dashboard || true'
            }
        }

        stage('Deploy Container') {
            steps {
                echo "Deploying the new container..."
                // We run the new container on port 9000
                // Note: We will configure the .env file in Jenkins later
                sh 'docker run -d -p 9000:8000 --name autoscale-dashboard autoscaleops-app:latest'
            }
        }
    }
}