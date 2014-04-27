from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.template import loader, Context
from funds.models import Member, Account, Voucher
#from django.core.mail import send_mail
import json


def home(request):
    return render_to_response('funds/home.html')


@csrf_exempt
def voucher_deposit(request):
    import datetime

    error = 'false'
    msg = None
    if request.POST:
        try:
            a = Account.objects.get(acc_num=str(request.POST['acc-no']))
            vouchers_unprocessed = request.POST['vouchers'].split(",")
            vouchers_processed = []
            vouchers_used = []
            for voucher in vouchers_unprocessed:
                vouchers_processed.append(str(voucher).strip())
            vouchers = Voucher.objects.filter(num__in=vouchers_processed)
            for voucher in vouchers:
                vouchers_processed.remove(str(voucher.num))
                if not voucher.used:
                    voucher.account = a
                    a.balance += voucher.value
                    voucher.used = True
                    voucher.date_used = datetime.date.today()
                    a.save()
                    voucher.save()
                else:
                    vouchers_used.append(str(voucher.num))
            if vouchers_processed or vouchers_used:
                error = 'true'
                msg = ''
                if vouchers_processed and vouchers_used:
                    msg += '<p>These vouchers were wrong ' + ','.join(vouchers_processed) + '</p>'
                    msg += '<p>These vouchers were used ' + ','.join(vouchers_used) + '</p>'
                elif vouchers_used:
                    msg += '<p>These vouchers were used ' + ','.join(vouchers_used) + '</p>'
                else:
                    msg += '<p>These vouchers were wrong ' + ','.join(vouchers_processed) + '</p>'
                print msg
        except Exception, e:
            print e.args[0]
            pass
    return render_to_response('funds/deposit.html', {'title': 'deposit', 'error': error, 'error_message': msg})


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
    return render_to_response('funds/home.html', {'title': 'home'})


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
    import json
    f = open(settings.TEMPLATE_DIRS[0] + '/funds/admin/vouchers.json', 'w')
    f.write(json.dumps(vouchers_list))
    f.close()

    t = loader.get_template('funds/admin/vouchers.html')
    c = Context({'vouchers': vouchers_list, 'title': 'vouchers'})
    return HttpResponse(t.render(c))

def voucher_download(request):
    fsock = open(settings.TEMPLATE_DIRS[0] + '/funds/admin/vouchers.json', 'r')
    response = HttpResponse(fsock, mimetype='application/json')
    response['Content-Disposition'] = "attachment; filename=%s.json" % ('vouchers')
    return response


def send_notifications(request):
    #100 people at a time
    # large number of non-existent or broken addresses (>25)
    #send_mail('Testing', 'Here is the message.', 'taichobill@gmail.com',
    #          ['dakbill@yahoo.com'], fail_silently=False)
    return render_to_response('funds/admin/send_notifications.html', {'title': 'notificaitons'})


def balance(request):
    member = Member.objects.get(username=request.session['username'])
    month_total = 0
    import datetime

    month_vouchers = Voucher.objects.filter(date_used__month=datetime.date.today().month)
    for mv in month_vouchers:
        month_total += mv.value
    last_month_savings = member.account.balance - month_total
    increments = []
    val = last_month_savings
    for mv in month_vouchers:
        val += mv.value
        increments.append(val)

    return render_to_response('funds/balance.html',
                              {'member': member, 'title': 'balance',
                               'month_vouchers_and_increments': zip(month_vouchers, increments),
                               'last_month_savings': last_month_savings, 'balance': member.account.balance})


def notifications(request):
    return render_to_response('funds/notifications.html')


def payment_system(request):
    return render_to_response('funds/payment_system.html')


def mobile_money_deposit(request):
    return render_to_response('funds/mobile_money_deposit.html')


def stats(request):
    return render_to_response('funds/admin/stats.html')


def contact(request):
    return render_to_response('contact.html')


def about(request):
    return render_to_response('about.html')


def mpower(request):
    pass


def client_stats(request):
    return render_to_response('funds/client/stats.html')


@csrf_exempt
def get_graph(request):
    import datetime
    import time

    month_vouchers = Voucher.objects.filter(date_used__month=datetime.date.today().month).order_by('date_used')
    #handle same day contributions
    data_points = []
    value_pairs = []
    for v in month_vouchers:
        value_pairs.append((int(v.value), str(v.date_used +datetime.timedelta(1))))
    import itertools
    for key, group in itertools.groupby(value_pairs, key=lambda x: x[1][:11]):
        sum = 0
        for element in group:
            sum += element[0]
        date_list = str(key).split('-')
        data_points.append([int(time.mktime(datetime.datetime.strptime(
            date_list[2] + '/' + date_list[1] + '/' + date_list[0],
            "%d/%m/%Y").timetuple())) * 1000, sum])
    data = {
        "rangeSelector": {"selected": 1},
        "title": {"text": "Contribution for this month"},
        "series": [
            {"name": "series name", "color": "green", "data": data_points, "tooltip": {"valueDecimals": 2}}
        ]
    }
    import json

    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')