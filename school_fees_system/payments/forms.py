from django import forms 
from .models import FeeStructure
from accounts.models import CustomUser
from notifications.models import Notification

class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['fee_type', 'amount', 'due_date']
        
class NotificationForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role='parent'), label="Select Parent")

    class Meta:
        model = Notification
        fields = ['parent', 'title', 'message']
