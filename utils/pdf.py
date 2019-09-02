# import base64
# from io import BytesIO

# import barcode
# from barcode.writer import ImageWriter
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# from weasyprint import HTML


# def generate_pdf(response, reservation, reservation_items):
#     id = reservation.id
#     fp = BytesIO()
#     EAN = barcode.get_barcode_class('ean13')
#     ean = EAN('5901234123457', writer=ImageWriter())
#     ean.save(f"/tmp/{id}")

#     encoded_string = ""
#     with open(f"/tmp/{id}.png", "rb") as f:
#         encoded_string = base64.b64encode(f.read()).decode()

#     encoded_string = 'data:image/png;base64,' + encoded_string

#     html_string = render_to_string(
#         'receipt_template.html', {
#             'id': reservation.id,
#             'membership_number': reservation.membership_number,
#             'name': reservation.name,
#             'phone': reservation.phone,
#             'email': reservation.email,
#             'reservation': reservation,
#             'reservation_items': reservation_items,
#             'barcode': encoded_string
#         })

#     html = HTML(string=html_string)
#     html.write_pdf(response)
