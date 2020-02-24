def IMAGE_NAME="pytorch-app"

pipeline {

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
          sh './scripts/build.sh ${IMAGE_NAME}'
        }
      }
      stage('Test image'){
        steps {
          sh './scripts/test.sh ${IMAGE_NAME}'
        }
      }
      stage('Deploy') {
          agent {
            dockerfile {
                filename 'Dockerfile'
                dir 'app'
            }
          }
          steps {
                echo 'Starting to build docker image'
                script {
                      def customImage = docker.build("${IMAGE_NAME}:${env.BUILD_ID}")
                      customImage.push()
                }

         }
      }
  }
}
