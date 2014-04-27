from django.conf.urls import *
from piston.resource import Resource
from funds.handlers import FundsHandler


class CsrfExemptResource(Resource):
    def __init__( self, handler, authentication=None ):
        super(CsrfExemptResource, self).__init__(handler, authentication)
        self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)


susu_api_resource = CsrfExemptResource(FundsHandler)

urlpatterns = patterns('',
                       url(r'^/$', 'funds.views.home', name="funds-home"),
                       url(r'^-deposit$', 'funds.views.payment_system', name="payment-system"),
                       url(r'^-voucher-deposit$', 'funds.views.voucher_deposit', name="funds-voucher-deposit"),
                       url(r'^-voucher-download$', 'funds.views.voucher_download', name="funds-voucher-download"),
                       url(r'^-mpower-deposit$', 'funds.views.mpower', name="funds-mpower-deposit"),
                       url(r'^/get-graph$', 'funds.views.get_graph', name="get-graph"),
                       #url(r'^-mobile-money-deposit$', 'funds.views.mobile_money_deposit', name="funds-mobile-money-deposit"),
                       url(r'^/login$', 'funds.views.login', name="funds-login"),
                       url(r'^/admin-dash$', 'funds.views.admin_dash', name="admin-dashboard"),
                       url(r'^/stats$', 'funds.views.stats', name="stats"),
                       url(r'^/client-stats$', 'funds.views.client_stats', name="client-stats"),
                       url(r'^/about-us$', 'funds.views.about', name="about-us"),
                       url(r'^/contact-us$', 'funds.views.contact', name="contact-us"),
                       url(r'^/agent-dash$', 'funds.views.agent_dash', name="agent-dashboard"),
                       url(r'^/client-dash$', 'funds.views.client_dash', name="client-dashboard"),
                       url(r'^-balance$', 'funds.views.balance', name="funds-balance"),
                       url(r'^-notifications$', 'funds.views.notifications', name="funds-notifications"),
                       #api
                       url(r'^-deposit-api/(?P<acc_no>.*)/(?P<vouchers>.*)$', susu_api_resource,
                           name="funds-deposit-api"),
                       #vouchers
                       url(r'^/generate-vouchers$', 'funds.views.vouchers', name="vouchers"),
                       #notifications
                       url(r'^/send-notifications$', 'funds.views.send_notifications', name="send-notifications"),

)