pipeline {
    agent any
    environment {
        OPENAI_API_KEY = credentials('openai-api-key')
        SECRET_KEY = credentials('flask-secret-key')
        PINECONE_API_KEY = credentials('pinecone-api-key')
        SLACK_TOKEN = credentials('slack-token')
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
                teamDomain: 'jenkins-alertsglobal',
                channel: '#all-jenkins-alerts',
                color: 'good',
                message: "✔ SUCCESS: Job '${env.JOB_NAME}' build #${env.BUILD_NUMBER}",
                tokenCredentialId: 'slack-token',
                botUser: true,
                username: 'Jenkins',
                iconEmoji: ':jenkins:'
            )
        }

        failure {
            slackSend(
                teamDomain: 'jenkins-alertsglobal',
                channel: '#all-jenkins-alerts',
                color: 'danger',
                message: "❌ FAILED: Job '${env.JOB_NAME}' build #${env.BUILD_NUMBER}",
                tokenCredentialId: 'slack-token',
                botUser: true,
                username: 'Jenkins',
                iconEmoji: ':jenkins:'
            )
        }

        unstable {
            slackSend(
                teamDomain: 'jenkins-alertsglobal',
                channel: '#all-jenkins-alerts',
                color: 'warning',
                message: "⚠️ UNSTABLE: Job '${env.JOB_NAME}' build #${env.BUILD_NUMBER}",
                tokenCredentialId: 'slack-token',
                botUser: true,
                username: 'Jenkins',
                iconEmoji: ':jenkins:'
            )
        }
    }
}