import smtplib
import ssl
import os
import imghdr
from email.message import EmailMessage


def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey, we just saw a new customer!")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    user_send = "dimitrov.s.dev@gmail.com"
    password = os.getenv("PASSWORD")
    receiver = "dimitrov.s.dev@gmail.com"
    gmail.login(user_send, password)
    gmail.sendmail(user_send, receiver, email_message.as_string())
    gmail.quit()

    # host = "smtp.gmail.com"
    # port = 587
    # context = ssl.create_default_context()
    #
    # with smtplib.SMTP_SSL(host, port, context=context) as server:
    #     server.login(user, password)
    #     server.sendmail(user, receiver)


if __name__ == "__main__":
    send_email(image_path="images/100image.png")

