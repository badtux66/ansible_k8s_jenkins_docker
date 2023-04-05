pipeline {
  agent any

  environment {
    DOCKER_REGISTRY = "your-dockerhub-username"
    DOCKER_IMAGE = "myapp"
    DOCKER_TAG = "${env.BUILD_NUMBER}"
    K8S_NAMESPACE = "default"
    K8S_DEPLOYMENT = "myapp"
    K8S_CONTAINER = "myapp"
  }

  stages {
    stage('Build') {
      steps {
        sh "docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG} ."
      }
    }

    stage('Push') {
      steps {
        sh "docker login -u ${DOCKER_REGISTRY} -p your-dockerhub-password"
        sh "docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}"
      }
    }

    stage('Deploy') {
      steps {
        kubernetesDeploy(
          kubeconfigId: 'kubeconfig',
          configs: 'k8s/deployment.yml',
          enableConfigSubstitution: true,
          namespace: "${K8S_NAMESPACE}"
        )
      }
    }

    stage('Expose') {
      steps {
        kubernetesDeploy(
          kubeconfigId: 'kubeconfig',
          configs: 'k8s/service.yml',
          enableConfigSubstitution: true,
          namespace: "${K8S_NAMESPACE}"
        )
      }
    }

    stage('URL') {
      steps {
        script {
          def nodePort = sh(returnStdout: true, script: "kubectl get svc/${K8S_DEPLOYMENT} -n ${K8S_NAMESPACE} -o jsonpath='{.spec.ports[0].nodePort}'").trim()
          def nodeIP = sh(returnStdout: true, script: "kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type==\"ExternalIP\")].address}'").trim()
          echo "URL: http://${nodeIP}:${nodePort}"
        }
      }
    }
  }
}
