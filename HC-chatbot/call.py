
from twilio.rest import Client

account_sid = 'ACf4f769d4e2aa048ef66d3385b5d5231d'
auth_token = 'fd7e7ad54891f382601b32bdd22df6ae'
client = Client(account_sid, auth_token)

call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+447741152781',
                        from_='+447741152781'
                    )

print(call.sid)
