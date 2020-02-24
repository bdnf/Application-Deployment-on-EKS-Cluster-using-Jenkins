pipeline {

  agent any
  stages {
      stage('Lint HTML') {
        steps {
          sh 'pwd && ls && tidy -q -e */*/*.html'
        }
      }
      stage('Lint Dockerfile') {
              agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir 'app'
                }
              }
              steps {
                sh 'docker run --rm -i hadolint/hadolint < Dockerfile'
              }
      }
      stage('Deploying now') {
          agent {
            dockerfile {
                filename 'Dockerfile'
                dir 'app'
            }
          }
          steps {
                echo 'Starting to build docker image'
                script {
                      def customImage = docker.build("pytorch-app:${env.BUILD_ID}")
                      customImage.push()
                }

         }
      }
  }
}
