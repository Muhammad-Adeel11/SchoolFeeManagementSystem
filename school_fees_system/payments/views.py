from django.shortcuts import render, redirect
from .models import Payment, FeeStructure
from notifications.models import Notification
from accounts.models import CustomUser
from django.utils import timezone

from .utils import send_payment_receipt_email

from .forms import FeeStructureForm, NotificationForm
from django.contrib.auth.decorators import login_required, user_passes_test

# PDF 
from django.template.loader import render_to_string
from django.http import HttpResponse
import weasyprint


# STRIPE 

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse





def is_admin(user):
    return user.role == 'admin'




# @login_required
# def payment_success(request):
#     return render(request, 'payments/payment_success.html')


@login_required
def payment_cancel(request):
    return render(request, 'payments/payment_cancel.html')

# DOWNLAOD PDF
@login_required
def download_receipt_pdf(request, payment_id):
    payment = Payment.objects.get(id=payment_id, parent=request.user)
    
    html_string = render_to_string('payments/receipt_pdf.html', {'payment': payment})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="receipt_{payment.id}.pdf"'
    
    weasyprint.HTML(string=html_string).write_pdf(response)
    return response


# Notifications 
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(parent=request.user).order_by('-created_at')
    return render(request, 'payments/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, parent=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')
@login_required
@user_passes_test(is_admin)
def send_manual_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notification_list_admin')  # we'll create this view next
    else:
        form = NotificationForm()
    return render(request, 'payments/send_notification.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def notification_list_admin(request):
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'payments/notifications_admin.html', {'notifications': notifications})








# Create your views here.
@login_required
def pay_fees(request):
    if request.method == 'POST':
        try:
            amount = request.POST['amount']
            method = request.POST['payment_method']
            payment = Payment.objects.create(parent = request.user, amount_paid = amount, payment_method = method)
            # Send real eamil after payment
            print(f' email: {request.user.email}')
            send_payment_receipt_email(
                user_email=request.user.email,
                amount=payment.amount_paid,
                payment_date=payment.payment_date.strftime('%Y-%m-%d %H:%M'),
                method=payment.payment_method
            )
            return redirect('receipt')
        except FeeStructure.DoesNotExist:
            return redirect('pay_fees')
    fee_structures = FeeStructure.objects.all()
    return render(request, 'payments/pay_fees.html', {'fee_structures': fee_structures})

def fee_status(request):
    payments = Payment.objects.filter(parent=request.user)
    return render(request, 'payments/fee_status.html', {'payments': payments})

# @login_required
# def fee_status(request):
#     fee_structures = FeeStructure.objects.all()
#     payments = Payment.objects.filter(parent=request.user)
#     paid_fee_ids = payments.values_list('fee__id', flat=True)  # if you track fees
#     context = {
#         'fees': fee_structures,
#         'payments': payments,
#     }
#     return render(request, 'payments/fee_status.html', context)


def receipt(request):
    latest_payment = Payment.objects.filter(parent=request.user).last()
    return render(request, 'payments/receipt.html', {'payment': latest_payment})

# add CRUD Views for FeeStructure management

def is_admin(user):
    return user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def fee_structure_list(request):
    structures = FeeStructure.objects.all()
    return render(request, 'payments/fee_structure_list.html', {'structures': structures})

@login_required
# @user_passes_test(is_admin)
def fee_structure_create(request):
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fee_structure_list')
    else:
        form = FeeStructureForm()
    return render(request, 'payments/fee_structure_form.html', {'form': form})

@login_required
# @user_passes_test(is_admin)
def fee_structure_update(request, pk):
    structure = FeeStructure.objects.get(pk=pk)
    if request.method == 'POST':
        form = FeeStructureForm(request.POST, instance=structure)
        if form.is_valid():
            form.save()
            return redirect('fee_structure_list')
    else:
        form = FeeStructureForm(instance=structure)
    return render(request, 'payments/fee_structure_form.html', {'form': form})

@login_required
# @user_passes_test(is_admin)
def fee_structure_delete(request, pk):
    structure = FeeStructure.objects.get(pk=pk)
    structure.delete()
    return redirect('fee_structure_list')

@login_required
def pay_fees(request):
    if request.method == 'POST':
        fee_id = request.POST.get('fee_type')
        payment_method = request.POST.get('payment_method')

        try:
            fee = FeeStructure.objects.get(id=fee_id)
            Payment.objects.create(
                parent=request.user,
                amount_paid=fee.amount,
                payment_method=payment_method
            )
            return redirect('receipt')
        except FeeStructure.DoesNotExist:
            return redirect('pay_fees')

    fee_structures = FeeStructure.objects.all()
    return render(request, 'payments/pay_fees.html', {'fee_structures': fee_structures})

@login_required
def all_payments(request):
    payments = Payment.objects.all()
    return render(request, 'payments/all_payments.html', {'payments': payments})

@login_required
def make_payment(request):
    if request.method == 'POST':
        fee_id = request.POST['fee_type']
        payment_method = request.POST['payment_method']
        fee = FeeStructure.objects.get(id=fee_id)
        Payment.objects.create(
            parent=request.user,
            fee=fee,
            amount_paid=fee.amount,
            payment_method=payment_method,
            payment_date=timezone.now()
        )
        return redirect('receipt')
    fee_structures = FeeStructure.objects.all()
    return render(request, 'payments/pay_fees.html', {'fee_structures': fee_structures})







# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import FeeStructure, Payment
# from django.db import models
# from django.utils import timezone

# @login_required
# def fee_structure_list(request):
#     structures = FeeStructure.objects.all()
#     return render(request, 'payments/fee_structure_list.html', {'structures': structures})

# @login_required
# def fee_structure_create(request):
#     if request.method == 'POST':
#         fee_type = request.POST['fee_type']
#         amount = request.POST['amount']
#         due_date = request.POST['due_date']
#         FeeStructure.objects.create(fee_type=fee_type, amount=amount, due_date=due_date)
#         return redirect('fee_structure_list')
#     return render(request, 'payments/fee_structure_form.html')

# @login_required
# def fee_structure_update(request, pk):
#     fee = get_object_or_404(FeeStructure, pk=pk)
#     if request.method == 'POST':
#         fee.fee_type = request.POST['fee_type']
#         fee.amount = request.POST['amount']
#         fee.due_date = request.POST['due_date']
#         fee.save()
#         return redirect('fee_structure_list')
#     return render(request, 'payments/fee_structure_form.html', {'form': fee})

# @login_required
# def fee_structure_delete(request, pk):
#     fee = get_object_or_404(FeeStructure, pk=pk)
#     fee.delete()
#     return redirect('fee_structure_list')

# @login_required
# def all_payments(request):
#     payments = Payment.objects.all()
#     return render(request, 'payments/all_payments.html', {'payments': payments})

# @login_required
# def make_payment(request):
#     if request.method == 'POST':
#         fee_id = request.POST['fee_type']
#         payment_method = request.POST['payment_method']
#         fee = FeeStructure.objects.get(id=fee_id)
#         Payment.objects.create(
#             parent=request.user,
#             fee=fee,
#             amount_paid=fee.amount,
#             payment_method=payment_method,
#             payment_date=timezone.now()
#         )
#         return redirect('receipt')
#     fee_structures = FeeStructure.objects.all()
#     return render(request, 'payments/pay_fees.html', {'fee_structures': fee_structures})

# @login_required
# def fee_status(request):
#     # Assuming a method to know which fee paid/unpaid
#     fees = FeeStructure.objects.all()
#     for fee in fees:
#         fee.is_paid = Payment.objects.filter(parent=request.user, fee=fee).exists()
#     return render(request, 'payments/fee_status.html', {'fees': fees})

# @login_required
# def receipt(request):
#     payment = Payment.objects.filter(parent=request.user).last()
#     return render(request, 'payments/receipt.html', {'payment': payment})
