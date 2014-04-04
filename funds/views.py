from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.template import loader, Context
from funds.models import Member, Account, Voucher
#from django.core.mail import send_mail


def home(request):
    return render_to_response('funds/home.html')


@csrf_exempt
def voucher_deposit(request):
    if request.POST:
        try:
            a = Account.objects.get(acc_num=str(request.POST['acc-no']))
            for voucher in request.POST['vouchers'].split(","):
                v = Voucher.objects.get(num=str(voucher).strip())
                if not v.used:
                    v.account = a
                    a.balance += v.value
                    v.used = True
                    a.save()
                    v.save()
        except Exception:
            pass
    return render_to_response('funds/deposit.html', {'title': 'deposit'})


@csrf_exempt
def login(request):
    if request.POST:
        try:
            m = Member.objects.get(username=request.POST['uname'], password=request.POST['pword'])
            request.session['username'] = request.POST['uname']
            return {
                'm': redirect('funds.views.admin_dash'),
                'a': redirect('funds.views.agent_dash'),
                'c': redirect('funds.views.client_dash'),
            }[m.role]

        except Exception:
            pass
    return render_to_response('funds/login.html', {'title': 'login'})


def admin_dash(request):
    return render_to_response('funds/admin/dash.html', {'title': 'dashboard'})


def agent_dash(request):
    return render_to_response('funds/agent/dash.html', {'title': 'dashboard'})


def client_dash(request):
    return render_to_response('funds/client/dash.html', {'title': 'dashboard', 'username': request.session['username']})


import string
import random


def generate_voucher(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def vouchers(request):
    vouchers_list = []
    for i in range(1, 10):
        vouchers_list.append(generate_voucher(11))
    t = loader.get_template('funds/admin/vouchers.html')
    c = Context({'vouchers': vouchers_list, 'title': 'vouchers'})
    return HttpResponse(t.render(c))


def send_notifications(request):
    #100 people at a time
    # large number of non-existent or broken addresses (>25)
    #send_mail('Testing', 'Here is the message.', 'taichobill@gmail.com',
    #          ['dakbill@yahoo.com'], fail_silently=False)
    return render_to_response('funds/admin/send_notifications.html', {'title': 'notificaitons'})


def balance(request):
    balance = Member.objects.get(username=request.session['username']).account.balance
    return render_to_response('funds/balance.html', {'balance': balance})


def notifications(request):
    return render_to_response('funds/notifications.html')


def payment_system(request):
    return render_to_response('funds/payment_system.html')


def mobile_money_deposit(request):
    return render_to_response('funds/mobile_money_deposit.html')