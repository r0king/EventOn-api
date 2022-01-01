import base64
from plugins.googleapi.Google import Create_Service
from email.mime.text import MIMEText

def create_mail_service(user_id):

    CLIENT_SECRET_FILE = 'plugins/googleapi/Credentials/keys.json'
    API_SERVICE_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES, user_id=user_id)
    return service

def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['bcc'] = to
  message['from'] = sender
  message['subject'] = subject
  raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
  return {
    'raw': raw_message.decode("utf-8")
  }

def send_message(user_id,subject,to, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  to = ','.join(to)
  raw_message = create_message(sender=user_id,to=to,subject=subject,message_text=message)
  Mailer = create_mail_service(user_id=user_id)
  
  try:
    message = (Mailer.users().messages().send(userId=user_id, body=raw_message)
               .execute())
    
    return {
      "id":message['id'],
      "subject":subject,
      "labelIds":message['labelIds']
    }
  except Exception as e:
    print ('An error occurred: %s' % e)


def send_mapped_message(user_id: str,subject: str, message: str,map_data: str ,mail_col:int):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  """
  Mailer = create_mail_service(user_id=user_id)
  Mails = []
  try:
    #send mail to each person in the sender's list
    for user in map_data:
      raw_message = create_message(sender=user_id,to=user[mail_col],subject=subject,message_text=message)
      
      mail = (Mailer.users().messages()
                .send(userId=user_id, body=raw_message)
                .execute())
      Mails.append({
        "id":mail['id'],
        "reciverId":user[mail_col],
        "subject":subject,
        "labelIds":mail['labelIds']
      })
    
    return Mails
  except Exception as e:
    print ('An error occurred: %s' % e)

