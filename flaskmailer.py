import credentials
from filegenerator import txt_to_string

from flask import Flask
from flask_mail import Mail, Message

credentials = credentials.readcredentials()

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": credentials["email"],
    "MAIL_PASSWORD": credentials["password"]
}

app.config.update(mail_settings)
mail = Mail(app)

#Example
MY_DICT = { 
    "firstname": "name",
    "lastname": "surname",
    "gender": "M",
    "email" : ["emails"],
    "attachments": ["files"]
    }
    
def flaskmailer(person):
    """
    Input: dictionary with personal information to customize the e-mails.
    Purpose: send e-mails with html formatting.
    Output: none.
    """
    
    with app.app_context():
        
        if   person["gender"] == "M": salutation = "Estimado"
        elif person["gender"] == "F": salutation = "Estimada"
        
        
        msg = Message(subject="¡Fotos de perfil para iniciar tu vida profesional!",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=person["email"]
                      )
        msg.html= txt_to_string("emailtemplate.html", False).replace("{0}",
                                                                 salutation).replace("{1}",
                                                                                     person["firstname"])
        for attachment in person["attachments"]:
            #attachment_name = attachment[attachment.rindex("\\")+1:]
            attachment_name = "Attachment_" + person["firstname"] + "-" + person["lastname"]\
                              + "_" + str( 1 + person["attachments"].index(attachment) )
            with app.open_resource(attachment) as fp:
                msg.attach(attachment_name, "image/jpeg", fp.read())

        mail.send(msg)
        
    return None
        
if __name__ == '__main__':
    flaskmailer(person)