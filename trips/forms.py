from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import Reservation, Coupon

class ReservationForm(forms.ModelForm):
    coupon_code = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter coupon code (optional)')
        })
    )
    
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'number_of_people', 
                 'preferred_date', 'special_requirements']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_people': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'preferred_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': forms.DateInput.format_value(forms.DateInput(), timezone.now().date())
            }),
            'special_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Any special requirements or preferences?')
            }),
        }
    
    def clean_coupon_code(self):
        code = self.cleaned_data.get('coupon_code')
        if code:
            try:
                coupon = Coupon.objects.get(code=code)
                if not coupon.is_valid():
                    raise forms.ValidationError(_('This coupon code has expired or is no longer valid.'))
                return code
            except Coupon.DoesNotExist:
                raise forms.ValidationError(_('Invalid coupon code.'))
        return code
