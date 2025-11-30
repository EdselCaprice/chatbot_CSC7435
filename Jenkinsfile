pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo "Building.."
                bat 'docker compose build'
            }
        }
        
        stage('Test') {
            steps {
                echo "Running backend tests..."
                bat 'docker compose run --rm backend python test.py'
            }
        }
        
        stage('Deliver') {
            steps {
                echo 'Deploying with Docker Compose..'
                bat 'docker compose down || exit 0'
                bat 'docker compose up --build -d'
                bat 'docker system prune -f'
            }
        }
    }
    
    post {
        success {
            echo '========================================='
            echo 'Pipeline completed successfully!'
            echo 'Frontend: http://localhost:3000'
            echo 'Backend:  http://localhost:5000'
            echo '========================================='
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}