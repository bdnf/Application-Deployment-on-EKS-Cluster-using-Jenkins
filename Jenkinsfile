pipeline {
  environment {
    registryCredential = 'dockerhub'
    DOCKER_IMAGE_NAME = 'pytorch-app'
    TAG_COMMIT = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
    CLUSTER_NAME='eks-cluster-dev'
    DEPLOYMENT_NAME="model-ml"
    UPDATED_IMAGE_NAME="will be updated"
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
                 script {
                    env.UPDATED_IMAGE_NAME = '${USERNAME}/${DOCKER_IMAGE_NAME}:${TAG_COMMIT}'
                 }
                 sh 'echo Updated image name is: ${UPDATED_IMAGE_NAME}'
               }
        }
      }
      stage('Deploy application') {
        steps {
          sh 'echo "Deploying app on EKS Cluster"'
          dir('k8s-manifests') {
              withAWS(credentials: 'aws-credentials', region: 'us-east-1') {
                      sh "aws eks update-kubeconfig --name ${CLUSTER_NAME}"
                      sh 'kubectl apply -f model-deploy.yaml'
                      sh 'kubectl apply -f model-svc.yaml'
                      sh 'echo "Updating for newer image version"'
                      script {
                        sh 'kubectl set image deployments/${DEPLOYMENT_NAME} ${DEPLOYMENT_NAME}=${UPDATED_IMAGE_NAME}'
                      }
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
