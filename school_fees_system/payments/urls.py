from django.urls import path
from . import views

urlpatterns = [
    path('pay/', views.pay_fees, name='pay_fees'),
    # stripe
 
  
   
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    # pdf
    path('receipt/download/<int:payment_id>/', views.download_receipt_pdf, name='download_receipt_pdf'),
    # notifications 
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/admin/', views.notification_list_admin, name='notification_list_admin'),
    path('notifications/send/', views.send_manual_notification, name='send_manual_notification'),
    
    
    
    
    
    path('status/', views.fee_status, name='fee_status'),
    path('receipt/', views.receipt, name='receipt'),
    path('payments/', views.all_payments, name='all_payments'),
    
    # path('make-payment/', views.make_payment, name='make_payment'),
    
    path('fee-structure/', views.fee_structure_list, name='fee_structure_list'),
    path('fee-structure/create/', views.fee_structure_create, name="fee_structure_create"),
    path('fee-structure/update/<int:pk>/', views.fee_structure_update, name="fee_structure_update"),
    path('fee-structure/delete/<int:pk>/', views.fee_structure_delete, name='fee_structure_delete'),
]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('fee-structures/', views.fee_structure_list, name='fee_structure_list'),
#     path('fee-structure/create/', views.fee_structure_create, name='fee_structure_create'),
#     path('fee-structure/update/<int:pk>/', views.fee_structure_update, name='fee_structure_update'),
#     path('fee-structure/delete/<int:pk>/', views.fee_structure_delete, name='fee_structure_delete'),

#     path('payments/', views.all_payments, name='all_payments'),
#     path('pay/', views.make_payment, name='make_payment'),
#     path('status/', views.fee_status, name='fee_status'),
#     path('receipt/', views.receipt, name='receipt'),
# ]
