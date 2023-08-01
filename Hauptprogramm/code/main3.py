import os
import json
import time
import smtplib
import datetime
from email.message import EmailMessage

class EmailManager:
    def __init__(self):
        self.processed_entries = set()
        self.max_email_size = 14 * 1024 * 1024  # 14 MB

    def read_credentials(self):
        with open('email_credentials.txt', 'r') as f:
            self.sender_email = f.readline().strip()
            self.sender_password = f.readline().strip()

    def calculate_file_sizes(self, entries):
        for entry in entries:
            files = [entry['ram_cpu_file'], entry['log_file']]
            if entry['clauselCalculator'] == 'SATISFIABLE':
                files.append(entry['img_file'])
            total_size = sum(os.path.getsize(file) for file in files if os.path.isfile(file))
            entry['total_size'] = total_size
        return entries

    def process_output_file(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
        entries = [json.loads(line.replace("'", '"')) for line in lines]
        new_entries = [entry for entry in entries if entry['time'] not in self.processed_entries]
        return new_entries

    def log_successful_email(self, entry):
        with open("sent_emails.txt", "a") as log_file:
            log_file.write(f"{entry['time']} {entry['img_folder']}\n")
        self.processed_entries.add(entry['time'])  # Aktualisieren Sie die verarbeiteten Einträge


    def extract_img_content(self, entry):
        return entry['img_folder'].split('/')[1]

    def send_email_with_multiple_entries(self, entries):
        files = []
        body_content = ""
        for entry in entries:
            files.append(entry['ram_cpu_file'])
            files.append(entry['log_file'])
            img_content = self.extract_img_content(entry)
            body_content += f"{entry['clauselCalculator']}; {entry['time']}; {img_content}\n"
            if entry['clauselCalculator'] == 'SATISFIABLE':
                files.append(entry['img_file'])
        subject = self.extract_img_content(entries[0])
        self.send_email(subject, body_content, files)
        for entry in entries:
            self.log_successful_email(entry)

    def send_email(self, subject, content, attachments):
        recipient_email = "sat.solver.solution@gmail.com"
        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = recipient_email

        for attachment in attachments:
            with open(attachment, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(attachment)
                img_content = attachment.split('/')[1]
                new_file_name = f"{img_content}_{file_name}"
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=new_file_name)

        while True:  # Wir verwenden eine Schleife, um den E-Mail-Versand erneut zu versuchen, bis er erfolgreich ist
            try:
                with smtplib.SMTP_SSL('mail.gmx.net', 465) as server:
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(msg)
                    print("E-Mail erfolgreich gesendet!")
                    time.sleep(20)  # 20 Sekunden warten, nachdem die E-Mail erfolgreich gesendet wurde
                    break  # Brechen Sie die Schleife ab, wenn die E-Mail erfolgreich gesendet wurde
            except Exception as e:
                print(f"E-Mail konnte nicht gesendet werden: {e}")
                print("Warte 5 Minuten, bevor ein erneuter Versuch unternommen wird...")
                time.sleep(300)  # 5 Minuten warten

    def run(self):
        self.read_credentials()
        while True:
            if os.path.exists('terminate-email.txt'):
                print("Terminate-Datei gefunden, beende das Programm...")
                break
            new_entries = self.process_output_file('output.txt')
            entries_with_size = self.calculate_file_sizes(new_entries)
            self.process_multiple_entries(entries_with_size)
            time.sleep(60)  # Warte 60 Sekunden

    def process_multiple_entries_space(self, entries):
        current_email_size = 0
        current_email_entries = []
        for entry in entries:
            entry_size = entry['total_size']
            if current_email_size + entry_size > self.max_email_size:
                if current_email_entries:
                    self.send_email_with_multiple_entries(current_email_entries)
                current_email_size = 0
                current_email_entries = []
            if entry_size < self.max_email_size:
                current_email_size += entry_size
                current_email_entries.append(entry)
            if current_email_size >= self.max_email_size:
                self.send_email_with_multiple_entries(current_email_entries)
                current_email_size = 0
                current_email_entries = []
        if current_email_entries:
            self.send_email_with_multiple_entries(current_email_entries)

    def process_multiple_entries(self, entries):
        current_email_entries = []
        for i, entry in enumerate(entries):
            # Überprüfen Sie, ob der Eintrag bereits verarbeitet wurde, bevor Sie ihn hinzufügen
            if entry['time'] not in self.processed_entries:
                current_email_entries.append(entry)
                # Senden Sie die E-Mail, nachdem 5 Einträge hinzugefügt wurden
                if (i + 1) % 5 == 0:
                    self.send_email_with_multiple_entries(current_email_entries)
                    current_email_entries = []
        # Senden Sie die übrigen Einträge, wenn es weniger als 5 waren
        if current_email_entries:
            self.send_email_with_multiple_entries(current_email_entries)


if __name__ == "__main__":
    manager = EmailManager()
    manager.run()
