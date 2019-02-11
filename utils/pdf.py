from django.http import HttpResponse
from django.template.loader import render_to_string
import barcode
from io import BytesIO
from weasyprint import HTML
from barcode.writer import ImageWriter
import base64


def generate_pdf(reservation, reservation_items):
    id = reservation.id
    fp = BytesIO()
    EAN = barcode.get_barcode_class('ean13')
    ean = EAN('5901234123457', writer=ImageWriter())
    ean.save(f"/tmp/{id}")

    encoded_string = base64.b64encode(open(f"/tmp/{id}.png", "rb").read()).decode()


    encoded_string = 'data:image/png;base64,' + encoded_string

    print(encoded_string)

    html_string = render_to_string('receipt_template.html', {
        'id': reservation.id,
        'membership_number': reservation.membership_number,
        'name': reservation.name,
        'phone': reservation.phone,
        'email': reservation.email,
        'reservation': reservation,
        'reservation_items': reservation_items,
        'barcode': encoded_string
    })

    html = HTML(string=html_string)
    html.write_pdf(target=f"/tmp/{id}.pdf")

