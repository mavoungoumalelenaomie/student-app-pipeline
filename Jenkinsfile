pipeline {
    agent any
    
    environment {
        GITHUB_CREDENTIALS = credentials('github-token')
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-token',
                    url: 'https://github.com/mavoungoumalelenaomie/student-app-pipeline.git'
            }
        }
        
        stage('Check project') {
            steps {
                sh 'ls -la'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t student-app .'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d --build'
            }
        }
        
        stage('Check Containers') {
            steps {
                sh 'docker ps'
            }
        }
    }
}
