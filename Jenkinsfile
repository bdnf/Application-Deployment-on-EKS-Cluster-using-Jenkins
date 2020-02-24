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
          sh './scripts/build.sh pytorch-app'
        }
      }
      stage('Test image'){
        steps {
          sh './scripts/test.sh pytorch-app'
        }
      }
      stage('Push image to DockerHub') {
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
