import json
from piston.handler import BaseHandler


class FundsHandler(BaseHandler):
    allowed_methods = 'GET'

    def read( self, request, acc_no, vouchers ):
        ans = json.dumps({"Account number": acc_no, "Vouchers": vouchers})
        return ans