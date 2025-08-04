class NotificationService:
    def send_email(self, email, message):
        print(f"Simulated Email to {email}: {message}")
    
    def send_sms(self, number, message):
        print(f"Simulated SMS to {number}: {message}")