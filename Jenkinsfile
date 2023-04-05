pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = '832b05f4-e5c3-406f-ae25-0591bf529adb'
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
                        kubeconfigId: '7d9d96c4-efbb-4056-aeb2-a8a20748d025',
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
