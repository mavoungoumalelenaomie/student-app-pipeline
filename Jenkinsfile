pipeline {
    agent any
    stages {
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
