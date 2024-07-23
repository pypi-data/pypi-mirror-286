from wedeliver_core_plus import Topics
from wedeliver_core_plus.helpers import kafka_producers
from wedeliver_core_plus.helpers.exceptions import AppValidationError

def send_sms(message, mobiles=None,mobile=None):
    if mobile:
        mobiles = [mobile]
    if not mobiles:
        raise AppValidationError("could not send sms , there is no mobiles")
    kafka_producers.send_topic(topic=Topics().SEND_SMS, datajson=dict(
        function_name='app.business_logic.bulk_sms.send_v2.send_bulk_v2',
        function_params=dict(
            sms_message=message, mobile_numbers=mobiles
        )
    ))