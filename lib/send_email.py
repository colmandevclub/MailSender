import smtplib


def send_email(my_email, password, message, to_email, smtp_server="smtp.gmail.com", smtp_port=587):
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        # Log in to the server
        server.login(my_email, password)
        server.sendmail(my_email, to_email, message)  # Send the email
        print(f"Email sent successfully to {to_email}.")
