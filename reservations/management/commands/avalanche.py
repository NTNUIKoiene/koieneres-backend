from django.core.management.base import BaseCommand, CommandError
from urllib import request
import json
from utils.dateutils import compute_reservation_period, string_to_date
from reservations.models import ExtendedPeriod


class Command(BaseCommand):
    help = "Checks the avalanche warning"

    def handle(self, *args, **options):
        reservation_period = compute_reservation_period(ExtendedPeriod.objects.all())
        from_date = str(reservation_period["from"])
        to_date = str(reservation_period["to"])

        data = request.urlopen(
            f"https://api01.nve.no/hydrology/forecast/avalanche/v4.0.2/api/AvalancheWarningByRegion/Simple/3022/2/{from_date}/{to_date}"
        )
        data = json.load(data)
        data = map(
            lambda warning: (
                string_to_date(warning["ValidFrom"].split("T")[0]),
                int(warning["DangerLevel"]),
            ),
            data,
        )
        print(list(data))
        self.stdout.write(self.style.SUCCESS("Successfully checked avalanche warnings"))

