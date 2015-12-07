import string
import random

from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from werkzeug.exceptions import NotFound
from gevent import monkey
import requests

from flask import Flask, Response, request, render_template, url_for, redirect

import plivo

import config

monkey.patch_all()

app = Flask(__name__)
app.debug = True

authID = config.authID
authToken = config.authToken

MAILGUN_API_KEY = config.MAILGUN_API_KEY
MAILGUN_API_URL = config.MAILGUN_API_URL
MAILGUN_MAIL_TO = config.MAILGUN_MAIL_TO
MAILGUN_MAIL_FROM = config.MAILGUN_MAIL_FROM

def random_str_generator():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))

class ConfNamespace(BaseNamespace):
    def __init__(self, *args, **kwargs):
        super(ConfNamespace, self).__init__(*args, **kwargs)
        self.logger = app.logger
        self.log('ConfNamespace started')
        self.plivo = plivo.RestAPI(authID, authToken)

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def recv_disconnect(self):
        """Client disconnected handler.
        - Delete endpoint
        - Close connection
        """
        r = self.plivo.delete_endpoint({'endpoint_id':self.socket.endpoint_id})
        self.log(r)
        self.disconnect(silent=True)
        return True

    def on_get_endpoint(self):
        """Got request to create endpoint."""
        password = random_str_generator()
        params = {
            'username':'browcheck',
            'password':password,
            'alias':'browcheck'
        }
        r = self.plivo.create_endpoint(params)
        #self.log(r)
        eid = r[1]['endpoint_id']
        username = r[1]['username']
        self.socket.endpoint_id = eid

        self.log('endpoint %s created. username = %s' % (eid, username))

        self.emit('endpoint', {'username':username, 'password':password})

    def on_issue_report(self, browserData, callState, issueReporter, reporterEmail, issueDesc):
        print 'browserData'
        print browserData

        print 'callState'
        print callState

        print 'issue Desc'
        print issueDesc

        # mailFrom = "Browsercheck-" + issueReporter + "<" + MAILGUN_MAIL_FROM + ">"
        mailSubject = "Browsercheck Issue Report from " + reporterEmail
        mailContents = {
        'browserData': browserData,
        'callState': callState,
        'reporterEmail': reporterEmail
        }
        return requests.post(
        MAILGUN_API_URL,
        auth=("api", MAILGUN_API_KEY),
        data={"from": reporterEmail or MAILGUN_MAIL_FROM,
              "to": MAILGUN_MAIL_TO,
              "subject": mailSubject,
              "text": str(mailContents)})




@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
    try:
        socketio_manage(request.environ, {'': ConfNamespace}, request)
    except:
        app.logger.error("Exception while handling socketio connection",
                         exc_info=True)
    return Response()

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
