import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_confirmation_email(mail_info, mailer):
    print("Sending email")
    link = mail_info["auth_url"] + mail_info["activation_code"]
    text = get_mail_text(link)
    html = get_html_from_template(mail_info["mail_template"], mail_info["username"], link)
    msg = construct_mime_message(mail_info, html, text)

    mailer.send(mail_info["from_address"], mail_info["user_address"], msg.as_string())


def get_mail_text(link):
    text = "Hi,{user}. Welcome to Morpheus.\nIn order to complete the registration process, you must follow this link ["
    text += link + "]\n"
    text += "Please remember, you won't be able to login until you complete this process.\n"
    text += "Have a nice day!\n"

    return text


def get_html_from_template(template, username, link):

    base_path = os.getcwd()
    full_path = os.path.join(base_path, "static/" + template)

    with open(full_path, 'r') as f:
        data = f.read()
        mail_html = data.replace("{user}", username).replace("{link}", link)

    return mail_html


def construct_mime_message(mail_info, html, text):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = mail_info["subject"]
    msg['From'] = mail_info["from_address"]
    msg['To'] = mail_info["user_address"]

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    return msg
