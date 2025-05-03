import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def mail(msg: str):
    # Email details
    sender_email = "ac244@njit.edu"  # Your email address
    sender_password = "ouzi hcyz gfyn aprf"  # Your email password or an app password
    receiver_email = "buereddyhiteshreddy28@gmail.com"  # Recipient's email address
    pdf_file_path = "/Users/ashutoshchalise/Downloads/chatbot/AI-chatbot/backend/Hitesh_Reddy.pdf"  # Path to the PDF file
    subject = "Hello"
    body = f"""Hello John,
    Thanks for joining the chat this is the chat summary
    Summary:{msg}

Please Find the details about the plan below"""

    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Attach PDF file
    try:
        with open(pdf_file_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {pdf_file_path.split('/')[-1]}")
            message.attach(part)
    except FileNotFoundError:
            print(f"Error: PDF file not found at {pdf_file_path}")
            exit()

    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your SMTP server and port
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")