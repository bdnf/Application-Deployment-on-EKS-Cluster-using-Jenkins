pipeline {
  environment {
    REGISTRY= "olehbodunov"
    registryCredential = 'dockerhub'
    DOCKER_IMAGE_NAME = 'pytorch-app'
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
          withCredentials([$class: 'UsernamePasswordMultiBinding', string(credentialsId: 'dockerhub'), usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']) {
                 sh 'docker login -u ${USERNAME} -p ${PASSWORD}'
                 sh 'docker tag ${DOCKER_IMAGE_NAME} ${USERNAME}/${DOCKER_IMAGE_NAME}'
                 sh 'docker push ${USERNAME}/${DOCKER_IMAGE_NAME}'
               }
        }
      }
      stage('Deploy application') {
        steps {
          sh 'echo "Deploying app on EKS Cluster"'
          dir('k8s-manifests') {
              withAWS(credentials: 'aws-credentials', region: 'eu-east-1') {
                      sh "aws eks --region eu-east-1 update-kubeconfig --name eks-cluster-dev"
                      sh 'kubectl apply -f model-deploy.yaml'
                      sh 'kubectl apply -f model-svc.yaml'
                  }
              }
        }
      }
      stage('Cleanup') {
      steps {
        sh 'echo "Cleaning up"'
        sh 'docker system prune'
        sh 'docker logout'
        }
      }

  }
}
