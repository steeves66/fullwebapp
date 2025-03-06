from common import models

def get_current_config(key_name):
    try:
        return models.KeyValueStore.objects.get(key=key_name).value
    except models.KeyValueStore.DoesNotExist:
        return ()
    

from common import public
def get_current_gateway():
    return public.get_current_config('payment_gateway')


def get_payment_gateway():
    payment_config = get_current_gateway()
    if payment_config.get('name') == 'stripe':
        return 'stripe'
    elif payment_config.get('name') == 'paypal':
        return 'paypal'
    return 'stripe'


def make_payment(request):
    # do something related to payment
    payment_gateway = get_payment_gateway()
    # process payment