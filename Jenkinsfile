pipeline {

    agent any

    environment {
        DOCKER_USER = "psbd"
        DOCKER_CREDENTIALS = "dockerhub-credentials"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test User Service') {
            steps {
                bat '''
                cd user-service
                py -3.11 -m pip install -r requirements.txt
                py -3.11 -m pytest
                '''
            }
        }

        stage('Test Order Service') {
            steps {
                bat '''
                cd order-service
                py -3.11 -m pip install -r requirements.txt
                py -3.11 -m pytest
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                bat 'docker compose build'
                bat 'docker build -t psbd/user-service:latest ./user-service'
                bat 'docker build -t psbd/order-service:latest ./order-service'
            }
        }

        stage('Docker Hub Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    bat 'docker login -u "%DOCKER_USERNAME%" -p "%DOCKER_PASSWORD%"'
                }
            }
        }

        stage('Push User Service') {
            steps {
                bat 'docker push psbd/user-service:latest'
            }
        }

        stage('Push Order Service') {
            steps {
                bat 'docker push psbd/order-service:latest'
            }
        }

        stage('Deploy') {
            steps {
                bat 'docker compose up -d'
            }
        }

        stage('Smoke Test') {
            steps {
                bat 'curl.exe http://localhost:8001/'
                bat 'curl.exe http://localhost:8002/'
            }
        }
    }

    post {
        success {
            echo 'CI/CD PIPELINE SUCCESSFUL'
        }

        failure {
            echo 'CI/CD PIPELINE FAILED'
        }

        always {
            echo 'Pipeline Completed'
        }
    }
}