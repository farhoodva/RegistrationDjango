from .models import DriverInfo, State, City
from django.core.exceptions import ValidationError
from django import forms

# validation moved to models.py
# def validate_nid(value):
#     if len(str(value)) != 10:
#         raise ValidationError(
#             'کد ملی باید 10 رقمی باشد.',
#             params={'value': value},
#         )
#     n1 = int(value[0])
#     n2 = int(value[1])
#     n3 = int(value[2])
#     n4 = int(value[3])
#     n5 = int(value[4])
#     n6 = int(value[5])
#     n7 = int(value[6])
#     n8 = int(value[7])
#     n9 = int(value[8])
#     cn = int(value[9])
#     checksum = (n1*10)+(n2*9)+(n3*8)+(n4*7)+(n5*6)+(n6*5)+(n7*4)+(n8*3)+(n9*2)
#     remainder = checksum % 11
#     if 2 > remainder == cn or remainder >= 2 and cn == 11 - remainder:
#         return value
#     else:
#         raise ValidationError(
#             'کد ملی اشتباه است.',
#             params={'value': value},
#         )
#
#
# def validate_length_smart_card(value):
#     if len(str(value)) != 5:
#         raise ValidationError(
#             'کارت هوشمند باید 5 رقمی باشد',
#             params={'value': value},
#         )
#     return value
#
#
# def validate_length_cell(value):
#     if len(str(value)) != 11 or not str(value).startswith('09'):
#         raise ValidationError(
#             'شماره موبایل را به صورت صحیح وارد نمایید',
#             params={'value': value},
#         )
#     return value
#
#
# class DriverInfoForm(forms.ModelForm):
#
#     class Meta:
#         model = DriverInfo
#         fields = ['national_id', 'cellnumber', 'name', 'family', 'state', 'city', 'smart_card_number', 'email']
#         error_messages = {
#             'city': {
#                 'required': 'شهر نمیتواند خالی باشد'
#             }
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.fields['email'].widget.attrs.update({'placeholder': 'Example@gmail.com'})
#         # field attrs update
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control',
#                 'style': 'font-family:shabnam, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif,'
#                          ' "Apple Color Emoji",'
#                          '"Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";font-size: 14px;'
#             })
#         # setting city contents to empty intially
#         self.fields['city'].queryset = City.objects.none()
#
#         if 'state' in self.data:
#             try:
#                 state_id = (self.data.get('state'))
#                 self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
#                 # self.fields['city'].widget.attrs.update({'class': 'form-control'})
#             except (ValueError, TypeError):
#                 # populating city field based on selected state id in  html
#                 pass
#                   # invalid input from the client; ignore and fallback to empty City queryset
#         elif self.instance.pk:
#             self.fields['city'].queryset = self.instance.state.city_set.order_by('name')
#
#     national_id = forms.CharField(validators=[validate_nid], strip=True, widget=forms.TextInput(attrs={
#             'placeholder': 'کد ملی ده رقمی',
#             'type': 'number',
#
#         }),
#          )
#
#     smart_card_number = forms.CharField(strip=True, validators=[validate_length_smart_card], widget=forms.TextInput(attrs={
#         'placeholder': 'شماره کارت هوشمند',
#         'type': 'number',
#         })
#                                         )
#     name = forms.CharField(widget=forms.TextInput(attrs={
#         'placeholder': 'نام',
#     }))
#
#     family = forms.CharField(widget=forms.TextInput(attrs={
#         'placeholder': 'نام خانوادگی',
#         }))
#
#     cellnumber = forms.CharField(validators=[validate_length_cell], strip=True, widget=forms.TextInput(attrs={
#         'placeholder': 'شماره موبایل ********09',
#         'type': 'number',
#           }))
#
#     email = forms.EmailField()
#
#     state = forms.ModelChoiceField(queryset=State.objects.all(), empty_label="انتخاب استان ")
#
#
#
#
#


class DriverInfoForm(forms.ModelForm):

    class Meta:
        model = DriverInfo
        fields = ['national_id', 'cellnumber', 'name', 'family', 'state', 'city', 'smart_card_number', 'email']
        error_messages = {
            'city': {
                'required': 'شهر نمیتواند خالی باشد'
            }
        }

        widgets = {
            'national_id': forms.TextInput(attrs={
                'placeholder': 'کد ملی ده رقمی',
                # 'maxlength': '10', does not work for type number
                'type': 'number',

            }),

            'smart_card_number': forms.TextInput(attrs={
                'placeholder': 'کارت هوشمند',
                'type': 'number', }),

            'cellnumber': forms.TextInput(attrs={
                 'placeholder': 'شماره موبایل ********09',
                 'type': 'number', }),

            'name': forms.TextInput(attrs={
                'placeholder': 'نام', }),

            'family': forms.TextInput(attrs={
                'placeholder': 'نام خانوادگی', }),
                  }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # field attrs update
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'style': 'font-family:shabnam, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif,'
                         ' "Apple Color Emoji",'
                         '"Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";font-size: 14px;'
            })
        self.fields['email'].widget.attrs['placeholder'] = 'Example@gmail.com'
        # setting city contents to empty initially
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = (self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
                # self.fields['city'].widget.attrs.update({'class': 'form-control'})
            except (ValueError, TypeError):
                # populating city field based on selected state id in  html
                pass
                  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')

    state = forms.ModelChoiceField(queryset=State.objects.all(), empty_label="انتخاب استان ")


class DriverInfoEditForm(forms.ModelForm):

    class Meta:
        model = DriverInfo
        fields = ['cellnumber', 'name', 'family', 'state', 'city', 'smart_card_number', 'email']
        error_messages = {
            'city': {
                'required': 'شهر نمیتواند خالی باشد'
            }
        }

        widgets = {
            'smart_card_number': forms.TextInput(attrs={
                'placeholder': 'کارت هوشمند',
                'type': 'number', }),

            'cellnumber': forms.TextInput(attrs={
                 'placeholder': 'شماره موبایل ********09',
                 'type': 'number', }),

            'name': forms.TextInput(attrs={
                'placeholder': 'نام', }),

            'family': forms.TextInput(attrs={
                'placeholder': 'نام خانوادگی', }),
                  }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'placeholder': 'Example@gmail.com'})
        # field attrs update
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'style': 'font-family:shabnam, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif,'
                         ' "Apple Color Emoji",'
                         '"Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";font-size: 14px;'
            })
        # setting city contents to empty intially
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = (self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
                # self.fields['city'].widget.attrs.update({'class': 'form-control'})
            except (ValueError, TypeError):
                # populating city field based on selected state id in  html
                pass
                  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')

    state = forms.ModelChoiceField(queryset=State.objects.all(), empty_label="انتخاب استان ")
