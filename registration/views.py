from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import generic
from django.utils import timezone
from .forms import DriverInfoForm, DriverInfoEditForm
from .models import DriverInfo, City
from django.core.mail import EmailMessage
from .functions import send_sms, create_auth_code


def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id)
    return render(request, 'loaded_cities.html', {'cities': cities})


class RegistrationView(generic.View):

    def get(self, request):
        form = DriverInfoForm()
        context = {
            'form': form,

        }
        return render(self.request, 'registration.html', context)

    def post(self, request):
        form = DriverInfoForm(self.request.POST or None)
        if form.is_valid():
                # ارسال کد به ایمیل
            token = create_auth_code()
            to_email = form.cleaned_data.get('email')
            # number = form.cleaned_data.get('cellnumber')
            # send_sms(token)
            mail_subject = 'کد ثبت نام'
            message = token
            email = EmailMessage(
                mail_subject, message, to=[to_email]

            )
            try:
                email.send()
                messages.info(self.request, 'ایمیل ارسال شد')
                context = {
                    'token': token,
                    'from': form
                }
                return render(self.request, 'code_confirm.html', context)

            except:
                messages.info(self.request, 'ایمیل ارسال نشد, دوباره تلاش کنید.  ')
                return redirect('registration:registration')

        else:
        # er = ''
        # for field in form:
        #     for error in field.errors:
        #         er += str(error) + '<br>'
            return render(self.request, 'registration.html', {'form': form}, messages.warning(self.request, "خطاهای مشخص شده را اصلاح نمایید."))


def activate(request, token):
    tc = request.POST['email_token']
    d = DriverInfoForm(request.POST)
    if tc == token:
        d.save()
        messages.info(request, 'ثبت نام با موفیت انجام شد')
        return redirect('registration:registration')
    else:
        messages.info(request, 'کد وارد شده صحیح نمی باشد')
        return redirect('registration:registration')


class DriverInfoView(generic.View):

    def get(self, request):
        return render(self.request, 'driver_info_view.html')

    def post(self, request):
        nid = self.request.POST['national_id']
        if not len(str(nid)) == 10:
            messages.warning(self.request, 'کد ملی را به صورت  10 رقمی وارد کنید')
            return redirect('registration:info_view')
        else:
            nid = str(nid)

            try:
                driver = DriverInfo.objects.get(national_id=nid)
                context = {
                    'driver': driver,
                    'table_display': True
                }
                return render(self.request, 'driver_info_view.html', context)
            except ObjectDoesNotExist:
                messages.warning(self.request, 'این کد ملی در سامانه موجود نمی باشد')
                return redirect('registration:info_view')


class DriverInfoUpdate(SuccessMessageMixin, generic.UpdateView):

    model = DriverInfo
    form_class = DriverInfoEditForm
    template_name = 'driverinfo_update_form.html'
    success_url = reverse_lazy('registration:info_view')
    success_message = 'اطلاعات با موفقیت ویرایش شد'


class DriverListView(LoginRequiredMixin,generic.ListView):
    model = DriverInfo
    template_name = 'driver_list_view.html'
    context_object_name = 'drivers'
    paginate_by = 8
