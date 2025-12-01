pipeline {
    agent any
    environment {
        OPENAI_API_KEY = credentials('openai-api-key')
        SECRET_KEY = credentials('flask-secret-key')
        PINECONE_API_KEY = credentials('pinecone-api-key')
    }
    stages {
        stage('Build') {
            steps {
                echo "Building.."
                sh '''
                    # Create .env file from Jenkins credentials
                    cat > backend/.env << EOF
OPENAI_API_KEY=${OPENAI_API_KEY}
SECRET_KEY=${SECRET_KEY}
PINECONE_API_KEY=${PINECONE_API_KEY}
EOF
                    docker compose build
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                echo "Running backend tests..."
                docker compose run --rm backend python test.py

                '''
            }
        }
        stage('Deliver') {
            steps {
                echo 'Deploying with Docker Compose..'
                sh 'docker compose down || true'
                sh 'docker compose up --build -d'
                sh 'docker system prune -f'
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
            slackSend(
                color: 'good',
                message: "✅ SUCCESS: Pipeline '${env.JOB_NAME}' [${env.BUILD_NUMBER}] completed successfully.\nFrontend: http://localhost:3000\nBackend: http://localhost:5000"
            )
        }
        failure {
            echo 'Pipeline failed!'
            slackSend(
                color: 'danger',
                message: "❌ FAILURE: Pipeline '${env.JOB_NAME}' [${env.BUILD_NUMBER}] failed!\nCheck console: ${env.BUILD_URL}console"
            )
        }
    }
}