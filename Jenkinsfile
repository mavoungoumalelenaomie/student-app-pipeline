pipeline {
    agent any

    stages {

        stage('Check project') {
            steps {
                dir('/var/jenkins_home/student-app') {
                    sh 'ls'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('/var/jenkins_home/student-app') {
                    sh 'docker build -t student-app ./app'
                }
            }
        }

        stage('Deploy') {
            steps {
                dir('/var/jenkins_home/student-app') {
                    sh 'docker compose down || true'
                    sh 'docker compose up -d --build'
                }
            }
        }

        stage('Check Containers') {
            steps {
                sh 'docker ps'
            }
        }
    }
}
