
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from .models import CustomUser
from .forms import CustomUserCreationForm # , CustomAuthenticationForm
from payments.models import Payment, FeeStructure
from notifications.models import Notification
from django.db.models import Sum, Count
from django.db import models
from django.contrib.auth.decorators import login_required

# download pdf
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.utils.timezone import localtime

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('parent_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        # email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username , password=password)  # email = email
        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('parent_dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')


# def admin_dashboard(request):
#     return render(request, 'accounts/admin_dashboard.html')
def admin_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('login')
    
    total_parents = CustomUser.objects.filter(role='parent').count()
    payment_methods = Payment.objects.values('payment_method').annotate(total=Count('id'))
    total_revenue = Payment.objects.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_payments = Payment.objects.count()
    total_fee_structures = FeeStructure.objects.count()

    context = {
        'total_parents': total_parents,
        'payment_methods': payment_methods,
        'total_revenue': total_revenue,
        'total_payments': total_payments,
        'total_fee_structures': total_fee_structures,
    }
    return render(request, 'accounts/admin_dashboard.html', context)

# def parent_dashboard(request):
#     return render(request, 'accounts/parent_dashboard.html')
def parent_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'parent':
        return redirect('login')  # Force correct login
    
    payments = Payment.objects.filter(parent=request.user).order_by('-payment_date')
    total_paid = payments.aggregate(total=models.Sum('amount_paid'))['total'] or 0
    notification_count = Notification.objects.filter(parent=request.user, is_read=False).count()
    return render(request, 'accounts/parent_dashboard.html', {
        'payments': payments,
        'total_paid': total_paid,
        'notification_count': notification_count,
        })

def export_payments_csv(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('login')
    
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename="payments.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Parent', 'Amount Paid', 'payment Method', 'Date'])
    
    payments = Payment.objects.all()
    
    for payment in payments:
        writer.writerow([
            payment.parent.username,
            payment.amount_paid,
            payment.payment_method,
            localtime(payment.payment_date).strftime('%Y-%m-%d %H:%M')
        ])
    return response

def export_payments_pdf(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('login')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="payments.pdf"'
    
    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)
    y = 800
    
    p.drawString(200, 820, 'Payments Report')
    
    payments = Payment.objects.all()
    
    for payment in payments:
        text = f"{payment.parent.username} | ${payment.amount_paid} | {payment.payment_method} | {localtime(payment.payment_date).strftime('%Y-%m-%d')}"
        p.drawString(50, y, text)
        y -= 20
        if y <= 50: # Create a new page if content too long
            p.showPage()
            y = 800
            p.setFont("Helvetica", 12)
            
    p.showPage()
    p.save()
    return response

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             if user.is_staff:
#                 return redirect('admin_dashboard')
#             else:
#                 return redirect('parent_dashboard')
#     return render(request, 'accounts/login.html')

# class CustomLoginView(LoginView):
#     form_class = CustomAuthenticationForm
#     template_name = 'accounts/login.html'
    
#     def get_success_url(self):
#         if self.request.user.role == 'admin':
#             return 'admin-dashboard'  # Customize for your needs
#         return 'parent-dashboard'  # Customize for your needs



# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from payments.models import Payment, FeeStructure

# from django.db import models

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             if user.is_staff:
#                 return redirect('admin_dashboard')
#             else:
#                 return redirect('parent_dashboard')
#     return render(request, 'accounts/login.html')

# def user_register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = User.objects.create_user(username=username, password=password)
#         return redirect('login')
#     return render(request, 'accounts/register.html')

# @login_required
# def admin_dashboard(request):
#     total_revenue = Payment.objects.all().aggregate(total=models.Sum('amount_paid'))['total'] or 0
#     total_payments = Payment.objects.count()
#     total_fee_structures = FeeStructure.objects.count()
#     context = {
#         'total_revenue': total_revenue,
#         'total_payments': total_payments,
#         'total_fee_structures': total_fee_structures,
#     }
#     return render(request, 'accounts/admin_dashboard.html', context)

# @login_required
# def parent_dashboard(request):
#     payments = Payment.objects.filter(parent=request.user)
#     return render(request, 'accounts/parent_dashboard.html', {'payments': payments})

# def user_logout(request):
#     logout(request)
#     return redirect('login')
