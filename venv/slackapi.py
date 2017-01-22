import os
import webbrowser
from slackclient import SlackClient
from requests_oauthlib import OAuth2Session
from flask import Flask,render_template, request,json

app = Flask(__name__)

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_CLIENT_ID = '131365986039.131370051526'
SLACK_CLIENT_SECRET = '251f69502376b3b25974583ae18fbf84'
SCOPE = ['chat:write:bot', 'channels:read']
REDIRECT_URL = 'https://slack.com/oauth/authorize'
REDIRECT_URI = 'https://mail.google.com/'
print(SLACK_CLIENT_ID);
oauth = OAuth2Session(SLACK_CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI)
authorization_url, state = oauth.authorization_url(REDIRECT_URL)
webbrowser.open(authorization_url, new=2)

#access_response = slack_client.api_call(
#	'oauth.access',
#	client_id=SLACK_CLIENT_ID,
#	client_secret=SLACK_CLIENT_SECRET,
#	code=CODE,
#	redirect_uri=REDIRECT_URI,
#)

slack_client = SlackClient(SLACK_TOKEN)

@app.route('/')
def hello():
    return render_template('editor.html')

def list_channels():
	'''list_channels returns an array of channel information objects.
	   Each object contains the name and the id of the channel
	'''
	channels_call = slack_client.api_call('channels.list')
	if channels_call.get('ok'):
		list_of_channels = []
		for c in channels_call['channels']:
			list_of_channels.append({'name':c['name'], 'id': c['id']})
		return list_of_channels
	return None

def post_message(channel_id, body):
	slack_client.api_call(
		'chat.postMessage',
		channel=channel_id,
		text=body,
		username='bottie',
		icon_emoji=':robot_face'
	)



if __name__ == '__main__':
    app.run()
	#channels = list_channels()
	#if channels:
	#	post_message(channels[0]['id'], 'Hello world!')
	#else:
	#	print('Unable to authenticate')
