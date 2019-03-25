import os
from django.core.mail import send_mail
from django.conf import settings


def send_reservation_receipt(res_id, recipient):
    message = f'''
    Hei,

    dette er en bekreftelse på koiereservasjonen din. 
    Reservasjonsnummeret er {res_id}. For å laste ned
    en kvittering kan du følge denne lenken:

    {settings.SERVER_URL}/api/publicreservationdata/{res_id}/receipt/

    Med vennlig hilsen
    NTNUI Koiene    
    '''
    send_mail('[NTNUI Koiene] Koiereservasjon', message, 'no-reply@koiene.no',
              [recipient])
