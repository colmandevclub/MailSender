import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
from dotenv import load_dotenv

from lib.send_email import send_email

load_dotenv()  # take environment variables from .env.
# Gmail SMTP server configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_USERNAME = "colmandevclub@gmail.com"  # replace with your Gmail address
GMAIL_PASSWORD = os.environ["PASSWORD"]  # replace with your Gmail app password

subject = "ברוכים הבאים למועדון המפתחים!"

file_path = "resources/Acceptence.xlsx"
df = pd.read_excel(file_path, sheet_name='Acceptence')

for index, row in df.iterrows():
    print(f"Row {index + 1}:")
    print(f"Name: {row['first_name']}")
    print(f"Date: {row['test_day']}")
    print(f"Email: {row['email']}")
    print("-----")  # Separator between rows for clarity

    # Create a multipart message
    email_message = MIMEMultipart()
    email_message["From"] = "ColmanDevClub <" + GMAIL_USERNAME + ">"
    email_message["To"] = row['email']
    email_message["Subject"] = subject

    # HTML content for RTL formatting
    # with open("emails_content/invitation.html", "r", encoding="utf-8") as message_file:
    #     html_message = message_file.read()

    html_message = f"""<html>
    <body style="direction: rtl; text-align: right; font-size: 16px">
        <p style="margin-bottom: 10px">שלום {row['first_name']},</p>
        <p style="font-weight: bold; font-size: 20px; margin-bottom: 10px">אנו שמחים להודיע לך שעברת בהצלחה את המיונים למועדון המפתחים של המכללה למנהל!</p>
        <p>המפגש הראשון שלנו (ולאורך כל השנה) יתקיים ביום ראשון <b>17 בנובמבר 2024</b>, בשעות <b>19:00-22:00</b>, בכיתה <b>103 בבניין י"ג</b>.</p>
        <p>נשמח לראות אותך שם, ולהתחיל ביחד מסע של למידה, צמיחה ושיתוף פעולה.</p>
        <br>
        <p style="font-weight: bold;">להצטרפות לקבוצת הוואטסאפ של חברי המועדון:</p>
        <ul>
            <li><a href="{os.environ["WHATSAPPLINK"]}">לחץ כאן להצטרפות לקבוצה</a></li>
        </ul>
        <br>
        <p>בברכה,</p>
        <p>צוות מועדון המפתחים</p>
    </body>
</html>
"""

    # Attach the email body message in HTML with RTL formatting
    email_message.attach(MIMEText(html_message, "html", "utf-8"))

    try:
        # Connect to Gmail's SMTP server and start TLS encryption
        send_email(
            password=GMAIL_PASSWORD,
            my_email=GMAIL_USERNAME,
            to_email=row["email"],
            message=email_message.as_string()
        )
    except Exception as e:
        print(f"Error sending email to {row['email']}: {e}")
