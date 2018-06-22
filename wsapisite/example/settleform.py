from django import forms
import os

from .wsapi import WSAPI

# set these in some secure way in your environment rather than in source code.
# os.environ['WSAPI_CLIENT_ID'] = '...'
# os.environ['WSAPI_API_KEY'] = '...'
# os.environ['WSAPI_API_HOST'] = 'https://my.ipgpay.com'


class SettleForm(forms.Form):
    order_id = forms.CharField()
    amount = forms.CharField()

    def __init__(self, request, *args, **kwargs):
        client_id = os.environ.get('WSAPI_CLIENT_ID', '')
        api_key = os.environ.get('WSAPI_API_KEY', '')
        api_host = os.environ.get('WSAPI_API_HOST', '')

        self.api = WSAPI(client_id, api_key, api_host)
        self.request = request

        super(SettleForm, self).__init__(*args, **kwargs)

    def settle_order(self):
        form_data = self.cleaned_data
        settlement_data = self.api.order_settle(form_data)

        self.request.session['last_settlement'] = settlement_data.toJSON()

    def clean(self):
        return self.cleaned_data
