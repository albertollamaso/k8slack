FROM amd64/ubuntu:16.04
LABEL maintainer="albertollamaso@gmail.com"

# Install basic packages and dependencies
RUN apt-get update && apt-get install -y \
	vim \
	net-tools --fix-missing \
	wget \
	curl \
	sudo \
	bzip2 \
	build-essential \
	libxrender1 \
	libxext-dev \
	nginx \
	git

# Environment Variables
ENV WEBSOCKET_CLIENT_CA_BUNDLE=DigiCertGlobalRootCA.crt
ENV SLACK_API_TOKEN="xoxb-2222222222-1111111111-xpHCtsVospk9OMP20yBDxDC"
ENV SLACK_CHANNEL="#k8s_logs"


# install python
RUN apt-get update -y
RUN sudo apt install -y software-properties-common
RUN sudo add-apt-repository ppa:deadsnakes/ppa
RUN sudo apt update -y
RUN sudo apt install -y python3.7
RUN sudo apt install -y python3-pip

# Configure Nginx
RUN rm -rf /etc/nginx/*
COPY nginx/ /etc/nginx/
RUN ls -la /etc/nginx/*

# Install kubectl
RUN sudo apt-get update && sudo apt-get install -y apt-transport-https
RUN curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
RUN echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
RUN sudo apt-get update
RUN sudo apt-get install -y kubectl

# Configure k8s config file
RUN mkdir /root/.kube
COPY k8s.config.yaml /root/.kube/config


# Copy the repository
RUN python3.7 -m pip install --upgrade pip
COPY . /opt/app
WORKDIR /opt/app/
RUN pip3 install -r requirements.txt

EXPOSE 80
COPY docker-entrypoint.sh /opt/app/
ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]

# End of file