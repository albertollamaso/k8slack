import os
import sys
import slack
import requests
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask import request

client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
channel = os.environ['SLACK_CHANNEL']
app = Flask(__name__)  # create the Flask app


def parse_body(body):
	#print(body, file=sys.stderr) # Debug
	try:
		body = body.split("&")
		for parameter in body:
			parameter = parameter.split("=")
			if (parameter[0] == "user_name"):
				user_name = parameter[1]
			if (parameter[0] == "token"):
				token = parameter[1]
			if "text" in parameter[0]:
				text = parameter[1]
				text = text.split("+")
				command = text[0]
				pod_name = text[1]
				environment = text[2]
				print("command: %s , pod_name: %s , environment: %s , user_name: %s , parameter: %s , token: %s " %
				      (command, pod_name, environment, user_name, parameter, token), file=sys.stderr)  # Debug
				return(user_name, token, command, pod_name, environment)
	except (IndexError, ValueError) as e:
		print(e, file=sys.stderr)
		return "ERROR: expecting 3 parameters, /$slack_command logs $pod_name $environment", 200

def slack_message(pod, user_name):
	response = client.chat_postMessage(
		channel=channel,
		text="Sending requested logs for pod %s - requested by %s :point_down:" % (pod, user_name))
	assert response["ok"]
	assert response["message"]["text"]
	return

def slack_upload(pod):
	response = client.files_upload(
		channels=channel,
		file="%s.txt" % pod)
	assert response["ok"]
	os.system("rm -rf %s.txt" % pod)
	return "Processing...", 200

def kubectl_get_logs(pod_name, environment):
	pod = os.popen('kubectl get pods -n %s | grep -i %s' % (environment, pod_name)).read()
	if (len(pod) == 0):
		return(pod)
	pod = pod.split()
	pod = pod[0]
	os.system("kubectl logs %s -n %s >> %s.txt" % (pod, environment, pod))
	return (pod)

@app.route('/', methods=['POST'])
def slack():
	user_name, token, command, pod_name, environment = parse_body(request.get_data().decode('utf8'))
	# Handle logs command (to be refactored)
	if(command == "logs"):
		pod = kubectl_get_logs(pod_name, environment)
		if (len(pod) == 0):
			return "ERROR: couldn't find pod: %s for environment: %s" % (pod_name, environment), 200
		slack_message(pod, user_name)
		slack_upload(pod)

	return "Not Found", 404


app.run(debug=True, port=5002)  # run app in debug mode on port 5002
