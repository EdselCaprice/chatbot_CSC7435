pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo "Building.."
                sh '''
                echo "doing build sttuff..."
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                echo "Running backend tests..."
                docker-compose run --rm backend python test.py

                '''
            }
        }
        stage('Deliver') {
            steps {
                echo 'Deploying with Docker Compose..'
                sh 'docker-compose down'
                sh 'docker-compose up --build -d'
                sh 'docker system prune -f'
            }
        }
    }
}