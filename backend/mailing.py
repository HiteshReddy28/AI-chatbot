import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def mail(msg: str):
    # Email details
    
    sender_email = "pramodreddy20011@gmail.com"  # Your email address
    sender_password = "ouzi hcyz gfyn aprf"  # Your email password or an app password
    receiver_email = "ac244@njit.edu"  # Recipient's email address
    pdf_file_path = "/Users/ashutoshchalise/Downloads/chatbot/AI-chatbot/backend/Extended_Payment_Plan_Confirmation.pdf"  # Path to the PDF file
    subject = "Confirmation of Extended Payment Plan – Cognute Bank Loan Account"
    body = f"""Dear John Doe,

We appreciate your continued commitment to resolving your loan obligations with Cognute Bank.

Following our recent discussion and based on your current situation, we have finalized the 3-Month Extension Plan for your personal loan. Below are the details of your updated repayment structure:

Extended Payment Plan Summary:
• Plan Type: 3-Month Loan Extension
• Extended Term: 63 months (originally 60 months)
• Original Monthly Payment: $188.71
• New Monthly Payment: $180.80
• Interest Rate: 5% (unchanged)
• Loan Amount: $10,000
• Yearly Saving: $94.92
• Next Payment Due: March 15, 2024
• Payment Method: Auto Debit

Loan Details:
• Loan ID: LN987654
• Loan Type: Personal Loan
• Remaining Balance: $7,500
• Loan Purpose: Medical Expenses
• Start Date: January 1, 2022
• End Date (Revised): April 1, 2027
• Payment Status: Active
• Late Payments: 0
• Prepayment Penalty: Yes
• Collateral Required: No

Customer Information:
• Customer ID: CUST123456
• Name: John Doe
• Date of Birth: June 15, 1985
• Phone: +1 (234) 567-890
• Email: ac244@njit.edu
• Address: 123 Main St, Anytown, CA 12345, USA

Employment:
• Employer: ABC Corp
• Job Title: Software Engineer
• Status: Full-Time
• Annual Income: $85,000
• Years Employed: 5

If you agree to the terms of this revised plan, please confirm by replying to this email or signing the attached document. Once confirmed, this plan will be activated, and your new repayment schedule will begin accordingly.

Should you have any questions, feel free to contact us at +1 (862)-505-7154 or support@cognutebank.com.

We appreciate your prompt attention to this matter.

Sincerely,
Cognute Bank Collections Team
support@cognutebank.com
+1 (862)-505-7154"""

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