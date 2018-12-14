ode ('ec2-slave'){
 echo 'Hello World'

 stage('Checkout'){
      dir('Weather') {
          git url: 'https://github.com/zeevso/opsschool3-coding.git'
      }
  }

 stage('Setup and Run'){
     sh '''#!/bin/bash
     cd Weather/home-assignments/session1
     pip install -y requests
     python3 weather.py
     '''
     }
}
