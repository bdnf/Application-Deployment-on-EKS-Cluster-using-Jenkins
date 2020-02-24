pipeline {
  environment {
    registry = "olehbodunov/pytorch-app"
    registryCredential = 'dockerhub'
    dockerImage = ''
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
          sh './scripts/build.sh pytorch-app'
        }
      }
      stage('Test image'){
        steps {
          sh './scripts/test.sh pytorch-app'
        }
      }
      stage('Rebuild and tag image') {
          agent {
            dockerfile {
                filename 'Dockerfile'
                dir 'app'
            }
          }
          steps {
                echo 'Starting to build docker image'
                script {
                  dockerImage = docker.build registry + ":$BUILD_NUMBER"
                }

         }
      }
      stage('Push image') {
        steps{
          script {
            docker.withRegistry( '', registryCredential ) {
              dockerImage.push()
            }
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

  }
}
