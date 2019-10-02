from django.core.management.base import BaseCommand, CommandError
from urllib import request
import json
from utils.dateutils import compute_reservation_period, string_to_date
from reservations.models import ExtendedPeriod, Cabin, CabinClosing


class Command(BaseCommand):
    help = "Checks the avalanche warning"

    def handle(self, *args, **options):
        reservation_period = compute_reservation_period(ExtendedPeriod.objects.all())
        from_date = str(reservation_period["from"])
        to_date = str(reservation_period["to"])

        nve_url = f"https://api01.nve.no/hydrology/forecast/avalanche/v4.0.2/api/AvalancheWarningByRegion/Simple/3022/2/{from_date}/{to_date}"
        mock_url = "http://www.mocky.io/v2/5d94f6972f00006d008ffa62"

        # Load and process avalanche data
        data = request.urlopen(mock_url)
        data = json.load(data)
        data = list(
            filter(
                lambda warning: warning[1] >= 3,
                map(
                    lambda warning: (
                        string_to_date(warning["ValidFrom"].split("T")[0]),
                        int(warning["DangerLevel"]),
                    ),
                    data,
                ),
            )
        )

        if len(data) == 0:
            self.stdout.write(self.style.SUCCESS("No warnings above 3 found"))
            self.stdout.write(
                self.style.SUCCESS("Successfully checked avalanche warnings")
            )
            return

        kamtjonn = Cabin.objects.get(name="Kamtjønnkoia")
        # Close cabin on dates
        for date, level in data:
            self.stdout.write(f"Closing on {str(date)}. Warning level {level}")
            closing = CabinClosing(
                cabin=kamtjonn,
                from_date=date,
                to_date=date,
                comment=f"Avalanche Warning",
            )
            closing.save()

        self.stdout.write(self.style.SUCCESS("Successfully checked avalanche warnings"))

