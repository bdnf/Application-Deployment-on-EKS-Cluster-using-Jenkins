pipeline {

  agent any
  stages {
      stage('Lint HTML') {
        steps {
          sh 'pwd && ls && tidy -q -e */*/*.html'
        }
      }
      stage('Build') {
        steps {
          sh 'echo "Hello World"'
          sh '''
                    echo "Multiline shell steps works too"
                    ls -lah
                 '''
        }
      }
      stage('Deploying now') {
          agent {
            dockerfile {
                filename 'Dockerfile'
                dir 'app'
                label 'pytorch-app'
            }
          }

          steps {
            echo "Docker Created"
          }
       }
  }
}
