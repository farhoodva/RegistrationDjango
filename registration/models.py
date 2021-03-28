from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
# from registration.functions import validate_nid


# validators
def validate_nid(value):
    if len(str(value)) != 10:
        raise ValidationError(
            'کد ملی باید 10 رقمی باشد. ',
            params={'value': value},
        )
    n1 = int(value[0])
    n2 = int(value[1])
    n3 = int(value[2])
    n4 = int(value[3])
    n5 = int(value[4])
    n6 = int(value[5])
    n7 = int(value[6])
    n8 = int(value[7])
    n9 = int(value[8])
    cn = int(value[9])
    checksum = (n1*10)+(n2*9)+(n3*8)+(n4*7)+(n5*6)+(n6*5)+(n7*4)+(n8*3)+(n9*2)
    remainder = checksum % 11
    if 2 > remainder == cn or remainder >= 2 and cn == 11 - remainder:
        return value
    else:
        raise ValidationError(
            'کد ملی اشتباه است. ',
            params={'value': value},
        )


def validate_length_smart_card(value):
    if len(str(value)) != 5:
        raise ValidationError(
            'کارت هوشمند باید 5 رقمی باشد. ',
            params={'value': value},
        )
    return value


def validate_length_cell(value):
    if len(str(value)) != 11 or not str(value).startswith('09'):
        raise ValidationError(
            'شماره موبایل را به صورت صحیح وارد نمایید.',
            params={'value': value},
        )
    return value
# end validation


class DriverInfo(models.Model):
    # changes admin name to کد ملی
    national_id = models.CharField('کد ملی', max_length=100, unique=True, primary_key=True,
                                   error_messages={
                                       'unique': 'این کد ملی قبلا ثبت شده است. '
                                   }, validators=[validate_nid])
    smart_card_number = models.CharField('شماره کارت هوشمند', max_length=50, unique=True,
                                         error_messages={
                                             'unique': 'این کارت هوشمند قبلا ثبت شده است. '
                                         }, validators=[validate_length_smart_card])

    name = models.CharField('نام', max_length=20)
    family = models.CharField('نام خانوادگی', max_length=20)
    cellnumber = models.CharField('شماره همراه', max_length=110, validators=[validate_length_cell])
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True, )
    city = models.ForeignKey('City', on_delete=models.SET_DEFAULT, default=1)
    email = models.EmailField()
    date_added = models.DateTimeField('تاربخ ثبت نام', default=timezone.now)

    class Meta:
        ordering = ['national_id']
        verbose_name_plural = 'لیست اسامی'

    def __str__(self):
        return self.national_id

    def get_driver_info_update_url(self):
        return reverse('registration:info_update', kwargs={
            'pk': self.national_id
        })


class State(models.Model):
    name = models.CharField('استان', max_length=50, )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'استان ها'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField('شهر', max_length=50)
    state = models.ForeignKey('State', on_delete=models.CASCADE)

    class Meta:
        ordering = ['state']
        verbose_name_plural = 'شهرها'

    def __str__(self):
        return self.name
