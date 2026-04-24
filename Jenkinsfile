pipeline {
    agent any
    stages {
        stage('Check project') {
            steps {
                sh 'ls -la'
            }
        }
        stage('Cleanup') {
            steps {
                sh 'docker-compose down --remove-orphans || true'
                sh 'docker rm -f $(docker ps -aq --filter "publish=3000") 2>/dev/null || true'
                sh 'docker rm -f $(docker ps -aq --filter "publish=5000") 2>/dev/null || true'
                sh 'docker rm -f $(docker ps -aq --filter "publish=9090") 2>/dev/null || true'
                sh 'docker rm -f $(docker ps -aq --filter "publish=9091") 2>/dev/null || true'
                sh 'docker rm -f $(docker ps -aq --filter "publish=9092") 2>/dev/null || true'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t student-app .'
            }
        }
        stage('Deploy') {
            steps {
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
