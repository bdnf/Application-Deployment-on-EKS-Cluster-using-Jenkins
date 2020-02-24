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
                  script {
                      docker.image('hadolint/hadolint:latest-debian').inside() {
                              sh 'hadolint ./Dockerfile | tee -a hadolint_lint.txt'
                              sh '''
                                  lintErrors=$(stat --printf="%s"  hadolint_lint.txt)
                                  if [ "$lintErrors" -gt "0" ]; then
                                      echo "Errors in Dockerfile were, please check output below"
                                      cat hadolint_lint.txt
                                      exit 1
                                  else
                                      echo "Dockerfile is correct!"
                                  fi
                              '''
                      }
                  }
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
