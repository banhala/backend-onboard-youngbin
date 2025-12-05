import csv
import os

from django.core.management.base import BaseCommand

from product.models import Product


class Command(BaseCommand):
    help = "Import products from dummy_product.csv"

    def handle(self, *args, **options):
        csv_file_path = os.path.join("dummy_product.csv")

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found: {csv_file_path}"))
            return

        with open(csv_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            products = []

            for row in reader:
                products.append(
                    Product(
                        name=row["name"],
                        thumbnail=row["thumbnail"],
                        price=int(row["price"]),
                    )
                )

            Product.objects.bulk_create(products, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {len(products)} products")
        )
