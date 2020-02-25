pipeline {
  environment {
    registryCredential = 'dockerhub'
    DOCKER_IMAGE_NAME = 'pytorch-app'
    TAG_COMMIT = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
    CLUSTER_NAME='eks-cluster-dev'
  }
  agent any
  stages {
      stage('Lint HTML') {
        steps {
          sh 'pwd && ls && tidy -q -e */*/*.html'
        }
      }
      stage('Lint Dockerfile') {
        steps {
          sh './scripts/lint.sh'
        }
      }
      stage('Build image'){
        steps {
          sh './scripts/build.sh ${DOCKER_IMAGE_NAME}'
        }
      }
      stage('Test image'){
        steps {
          sh './scripts/test.sh ${DOCKER_IMAGE_NAME}'
        }
      }
      stage('Push image') {
        steps{
          withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub',
                usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]) {
                 sh 'docker login -u ${USERNAME} -p ${PASSWORD}'
                 sh 'docker tag ${DOCKER_IMAGE_NAME} ${USERNAME}/${DOCKER_IMAGE_NAME}:${TAG_COMMIT}'
                 sh 'docker push ${USERNAME}/${DOCKER_IMAGE_NAME}:${TAG_COMMIT}'
               }
        }
      }
      stage('Deploy application') {
        steps {
          sh 'echo "Deploying app on EKS Cluster"'
          dir('k8s-manifests') {
              withAWS(credentials: 'aws-credentials', region: 'eu-east-1') {
                      sh "aws eks update-kubeconfig --name ${CLUSTER_NAME}"
                      sh 'kubectl apply -f model-deploy.yaml'
                      sh 'kubectl apply -f model-svc.yaml'
                  }
              }
        }
      }
    }
    post {
      always {
          sh 'echo "Cleaning up"'
          sh 'docker system prune'
          sh 'docker logout'
        }
    }
}
