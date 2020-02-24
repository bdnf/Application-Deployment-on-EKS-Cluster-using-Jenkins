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
      stage('Push image') {
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
      stage('Deploy Image') {
        steps{
          script {
            docker.withRegistry( '', registryCredential ) {
              dockerImage.push()
            }
          }
        }
      }
  }
}
