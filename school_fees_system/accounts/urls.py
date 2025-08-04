from django.urls import path
from . import views
# from .views import CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'),name = 'logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('parent-dashboard/', views.parent_dashboard, name='parent_dashboard'),
        # new
    path('export-payments/csv/', views.export_payments_csv, name='export_payments_csv'),
    path('export-payments/pdf/', views.export_payments_pdf, name='export_payments_pdf'),
]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('login/', views.user_login, name='login'),
#     # path('register/', views.register, name='register'),
#     path('register/', views.user_register, name='register'),
#     path('logout/', views.user_logout, name='logout'),
#     path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
#     path('parent/dashboard/', views.parent_dashboard, name='parent_dashboard'),
# ]
