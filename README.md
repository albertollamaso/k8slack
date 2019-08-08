# k8slack - Kubernetes logs from Pods to Slack

## Overview

k8slack is an open source integration between Kubernetes and Slack.

You can get logs from your running Pods in your kubernetes cluster and upload them to a Slack channel with one command.

<p align="center"><img width="60%" src="images/command.gif"/></p>

## Installation

Following is the step by step to get the integration working.

- Go to https://api.slack.com/apps and create an App in Slack under your workspace

Example:

<p align="center"><img width="60%" src="images/create_app.png"/></p>

- Inside the created App, let's create a Slash command which is going to be the command we are going to execute in Slack in order to get the logs.

- Configure the parameters of the Slash command.

Example:

<p align="center"><img width="60%" src="images/slash_command.png"/></p>


- Now we need to create a Bot User under the same App in order to get the token for the integration

- Once the Bot User under Slack is created, let's get the Bot User OAuth Access Token

Example:

<p align="center"><img width="60%" src="images/oauth.png"/></p>



Too much theory, let's get hands dirty and run our Integration. 

### Requirements

- The server where the App is running  need to be exposed to Internet on ports 80/443
- The server where the App is running need to be allowed to access the Kubernetes Master nodes and make API requests to the K8s cluster.
- A valid K8s config file. AN example one is provided `k8s.config.yaml`
- We need a valid domain name and SSL certificates in order to get the Integration working under HTTPS
- We need to define 2 Environment variables:
  SLACK_API_TOKEN (This is the Bot User OAuth Access Token we got from Slack before)
  SLACK_CHANNEL (This is the channel in Slack where we want to post the logs from k8s Pods)

  Example:
```
export SLACK_API_TOKEN="xoxb-2222222222-1111111111-xpHCtsVospk9OMP20yBDxDC"
export SLACK_CHANNEL="#k8s_logs"
```

### Running and Testing

- Once you have defined the environment variables, let's run the docker image:

`docker run -d k8slogs`

- Let's go to Slack and test our integration

Usage: `/slack_command logs pod_name namespace`

Example:

Get logs from nginx Pod running under `qa` namespace
`/k8s logs nginx qa`

# Issues and Bug Reports

Feel free to report a bug or make a request for new features here in Github.

## Contributions

Github pull requests are the recommended way to contribute to this project.

## License

Main License: GPLv2.

Each source code file refers to the license and copyright details in the top of the file. Most of the code is licensed under GPLv2, some parts of the code are licensed under BSD.
