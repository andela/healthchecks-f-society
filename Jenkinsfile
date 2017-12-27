pipeline {
    agent { docker 'python:3.5.1' }
    stages {
        stage('build') {
            steps {
                echo 'cloning github repo'
                checkout scm
                echo 'Creating virtual environment'
                sh 'mkvirtualenv genie'
            }
        }
    }
}
