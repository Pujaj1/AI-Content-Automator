# tools/email_sender.py
import yagmail
import os
from crewai.tools import BaseTool
from datetime import date

# Ensure you have your email credentials set in your .env file
# RECIPIENT_EMAIL, SENDER_EMAIL, SENDER_APP_PASSWORD

class EmailSendingTool(BaseTool):
    name: str = "EmailSender"
    description: str = "A tool to send the final formatted LinkedIn post text to the user's email address."
    
    # We define the input argument needed for the tool's execution
    def _run(self, linkedin_post_draft: str) -> str:
        # Load environment variables
        SENDER_EMAIL = os.environ.get("SENDER_EMAIL") 
        APP_PASSWORD = os.environ.get("SENDER_APP_PASSWORD") 
        RECIPIENT_EMAIL = SENDER_EMAIL

        if not all([SENDER_EMAIL, APP_PASSWORD, RECIPIENT_EMAIL]):
             return "ERROR: Email credentials are not set. Check .env file."

        try:
            subject = f"Your Daily AI Trends LinkedIn Post Draft - {date.today().strftime('%Y-%m-%d')}"
            
            # Initialize yagmail SMTP client
            yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)
            
            # Send the email
            yag.send(
                to=RECIPIENT_EMAIL,
                subject=subject,
                contents=linkedin_post_draft 
            )
            return f"Email successfully sent to {RECIPIENT_EMAIL}."
        except Exception as e:
            return f"ERROR: Failed to send email. Details: {e}"