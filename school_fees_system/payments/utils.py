# from django.core.mail import send_mail
# from django.conf import settings

# def send_payment_receipt_email(user_email, amount, payment_date, method):
#     subject = 'Payment Receipt - School Fees'
#     message = f'''
# Dear Parent,


# Thank you for your payment.memoryview

# Details:
# Amount paid: ${amount}
# Payment Date: {payment_date}
# Payment Method: {method}


# Regards,
# School Management
#     '''
#     from_email = settings.DEFAULT_FROM_EMAIL
#     recipient_list = [user_email]
#     print(f' from: {from_email}, recipient: {recipient_list}')
#     send_mail(subject, message, from_email, recipient_list)

#  This way we keep email sending cleanly separated from views (DRY principle).

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_payment_receipt_email(user_email, amount, payment_date, method):
    subject = 'Payment Receipt - School Fees'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    # Render HTML email content
    html_content = render_to_string('emails/payment_receipt.html', {
        'amount': amount,
        'payment_date': payment_date,
        'method': method
    })

    # Create the email
    email = EmailMultiAlternatives(subject=subject, body='Payment Receipt', from_email=from_email, to=recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()
