pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'a32cc0d9-1566-4a3f-b393-e47009698e52'
        DOCKERHUB_REPO = 'edipoz/todo-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/badtux66/todo.git'
            }
        }

        stage('Build') {
            steps {
                script {
                    def mvnHome = tool 'Maven'
                    sh "${mvnHome}/bin/mvn clean package"
                }
            }
        }

        stage('Docker build and push') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKERHUB_CREDENTIALS) {
                        def app = docker.build("${DOCKERHUB_REPO}:${env.BUILD_NUMBER}")
                        app.push()
                    }
                }
            }
        }

        stage('Kubernetes Deploy') {
            steps {
                script {
                    kubernetesDeploy(
                        configs: 'k8s-deployment.yaml',
                        kubeconfigId: '060fc020-b1e1-493c-957e-3005aa75bfe7',
                        enableConfigSubstitution: true
                    )
                }
            }
        }

        stage('Expose application') {
            steps {
                script {
                    sh "kubectl expose deployment todo-deployment --type=LoadBalancer --name=todo-service"
                }
            }
        }

        stage('Get application URL') {
            steps {
                script {
                    def appUrl = sh(script: "kubectl get svc todo-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}'", returnStdout: true).trim()
                    echo "Application is running at: http://${appUrl}:8080"
                }
            }
        }
    }
}
