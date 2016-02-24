# Browsercheck

This page will test your browser for Plivo WebSDK compatibility. You can also make a call or receive a call to test your connection.

There is an option to send an email with the results of the test.

## Config file
1. authID - Auth ID found in your [Plivo Dashboard](https://manage.plivo.com/dashboard/)
2. authToken - Auth Token found in your [Plivo Dashboard](https://manage.plivo.com/dashboard/)
3. MAILGUN_API_KEY - API KEY from your Mailgun account
4. MAILGUN_API_URL - API URL from your Mailgun account
5. MAILGUN_MAIL_TO - Defauts To address to use while sending an email
6. MAILGUN_MAIL_FROM - Default From address to use while sending an email (used only when From address is not given by the user)

## browsercheck.js
1. SOCKETIO_SERVER - Server URL