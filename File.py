

import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

email_user = 'YOUR EMAIL'
email_pass = 'YOUR OWN CREATED GOOGLE APP PASSWORD FROM SETTINGS'

recipient_email = 'EMAIL'
subject = 'Time Limit Exceeded Alert'

smtp_server = 'smtp.gmail.com'
smtp_port = 587

file_path = 'File path'
df = pd.read_excel(file_path)

time_limit = timedelta(days=1)

df['Created At'] = pd.to_datetime(df['Created At'], format='%d/%m/%Y %I:%M:%S %p')

current_time = datetime.now()
exceeded_entries = df[(df['Payment Status'] == 'INITIATED') & (current_time - df['Created At'] > time_limit)]

if not exceeded_entries.empty:
    df.loc[exceeded_entries.index, 'Exceeded Time Limit'] = 'Yes'

    filtered_file_path = '/Users/omji/Desktop/Mail automation/fiatpayments_2024-07-11T10_20_41.177251Z.xlsx'
    exceeded_entries.to_excel(filtered_file_path, index=False)

    email_body = "Please find attached the entries where Payment Status is 'INITIATED' and Created At has exceeded 1 day."

    # Set up the email
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the Excel file
    with open(filtered_file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename=Exceeded_entries.xlsx')
    msg.attach(part)

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_user, email_pass)

    # Send the email
    server.send_message(msg)
    server.quit()
    print("Alert email with Excel attachment sent successfully!")

else:
    print("No entries have Payment Status 'INITIATED' and exceeded the time limit.")
