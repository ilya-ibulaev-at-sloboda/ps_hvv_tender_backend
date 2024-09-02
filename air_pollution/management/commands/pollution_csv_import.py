import csv
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.conf import settings
from air_pollution.models import Pollution


class Command(BaseCommand):
    """
    Import pollution data from a CSV
    Run with `python manage.py pollution_csv_import <path_to_csv>`
    Example `python manage.py pollution_csv_import air_pollution/data/air-pollution.csv`
    """

    help = "Import pollution data from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", nargs="+", type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            batch_size = 10000
            path = settings.BASE_DIR / options["csv_path"][0]
            # print(path)

            with open(settings.BASE_DIR / options["csv_path"][0], "r") as f:
                reader = csv.DictReader(f)

                pollution_objects = []

                for row in reader:
                    pollution_objects.append(
                        Pollution(
                            entity=row["Entity"],
                            iso=row["Code"],
                            year=row["Year"],
                            nitrogen_oxide=row["Nitrogen oxide (NOx)"],
                            sulphur_dioxide=row["Sulphur dioxide (SO₂) emissions"],
                            carbon_monoxide=row["Carbon monoxide (CO) emissions"],
                            organic_carbon=row["Organic carbon (OC) emissions"],
                            non_methane_volatile_organic_compounds=row[
                                "Non-methane volatile organic compounds (NMVOC) emissions"
                            ],
                            black_carbon=row["Black carbon (BC) emissions"],
                            ammonia=row["Ammonia (NH₃) emissions"],
                        )
                    )

                    # When the batch size is reached, bulk create the objects
                    if len(pollution_objects) >= batch_size:
                        Pollution.objects.bulk_create(pollution_objects)
                        self.stdout.write(
                            f"imported {len(pollution_objects)} pollution objects..."
                        )
                        pollution_objects = []  # Clear the list after bulk create

                # Create any remaining objects in the final batch
                if pollution_objects:
                    Pollution.objects.bulk_create(pollution_objects)
                    self.stdout.write(
                        f"imported {len(pollution_objects)} pollution objects..."
                    )

        except FileNotFoundError:
            raise CommandError('File "%s" does not exist' % options["csv_path"][0])
        except csv.Error:
            raise CommandError(
                'File "%s" is not a valid CSV file' % options["csv_path"][0]
            )
        except KeyError as e:
            raise CommandError(
                'CSV file "%s" does not have the required columns: %s'
                % (options["csv_path"][0], e)
            )
        except IntegrityError as e:
            raise CommandError(
                'Error importing CSV file "%s": %s' % (options["csv_path"][0], e)
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully imported pollution data from "%s"'
                    % options["csv_path"][0]
                )
            )
