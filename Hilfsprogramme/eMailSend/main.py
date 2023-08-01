# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText

def send_email(subject, content):
    with open('email_credentials.txt', 'r') as f:
        sender_email = f.readline().strip()
        sender_password = f.readline().strip()

    recipient_email = "sat.solver.solution@gmail.com"

    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP_SSL('mail.gmx.net', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("E-Mail erfolgreich gesendet!")
    except Exception as e:
        print(f"E-Mail konnte nicht gesendet werden: {e}")



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

    # Beispiel: Verwenden der send_email-Funktion
    subject = "Test E-Mail"
    content = "Das ist eine Test-E-Mail, gesendet über GMX.de mit Python."
    subject = "config-04-tetromino.txt"
    content = " Dauer: 232 Sekunden. Ausführung für config-04-tetromino.txt"
    send_email(subject, content)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
