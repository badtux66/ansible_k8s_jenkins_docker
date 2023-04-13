FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y sudo maven && \
    echo 'jenkins ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers && \
    rm -rf /var/lib/apt/lists/*

USER jenkins
