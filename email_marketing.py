import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai

# Fetch API key and email credentials from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")

if not gemini_api_key or not email_address or not email_password:
    raise ValueError("Missing API key or email credentials. Set them as environment variables.")

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

def generate_email_content(event_name, recipient_name, event_details, call_to_action):
    """
    Uses Gemini AI to generate a personalized email for event promotion.
    """
    prompt = f"""
    Write a compelling email for {recipient_name} about {event_name}. Include the details: {event_details}.
    End with a strong call to action: {call_to_action}.
    """
    
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    
    if response and hasattr(response, 'text'):
        return response.text
    else:
        return "Error: Could not generate email content."

def get_user_input():
    """Gets event details from the user."""
    event_name = input("Enter the event name: ")
    recipient_name = input("Enter recipient's name: ")
    event_details = input("Enter event details: ")
    call_to_action = input("Enter the call-to-action (e.g., 'Register now!'): ")
    
    return event_name, recipient_name, event_details, call_to_action

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(to_email, subject, body):
    """Sends an email using SMTP."""
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Get user input
event_name, recipient_name, event_details, call_to_action = get_user_input()

# Generate AI-powered email content
email_body = generate_email_content(event_name, recipient_name, event_details, call_to_action)

# Print the email for preview
print("\nGenerated Email:\n")
print(email_body)

# Ask for recipient's email and send
to_email = input("\nEnter recipient's email: ")
subject = f"You're Invited: {event_name}!"
send_email(to_email, subject, email_body)
