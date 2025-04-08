import os
import django
import random
import string
from faker import Faker
from decimal import Decimal
from django.core.management.base import BaseCommand
from products.models import Product, ProductCharacteristic, ProductType, Category

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "electronics_store.settings")
django.setup()

fake = Faker()

# Define possible characteristics based on product type
CHARACTERISTIC_TEMPLATES = {
    "Laptop": ["RAM", "Storage", "Processor", "Screen Size"],
    "Phone": ["Battery", "Camera", "Screen Type", "Storage"],
    "Headphones": ["Bluetooth", "Noise Cancellation", "Battery Life"],
    "TV": ["Screen Size", "Resolution", "Smart TV"],
    "Monitor": ["Refresh Rate", "Panel Type", "Resolution"],
    "Smartwatch": ["Battery Life", "Screen Size", "Water Resistance"],
}

# Function to generate a random slug
def random_slug():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

class Command(BaseCommand):
    help = "Generate test products with random characteristics"

    def add_arguments(self, parser):
        parser.add_argument(
            "count", type=int, help="Number of products to generate"
        )

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        categories = list(Category.objects.all())
        product_types = list(ProductType.objects.all())

        if not categories or not product_types:
            self.stdout.write(self.style.ERROR("Please create categories and product types first!"))
            return

        products = []
        characteristics = []

        for _ in range(count):
            product_type = random.choice(product_types)
            category = random.choice(categories)

            price = Decimal(str(round(random.uniform(100, 5000), 2)))  # Convert price to Decimal
            discount_price = price * Decimal(str(random.uniform(0.7, 0.95))) if random.choice([True, False]) else None

            product = Product(
                name=fake.unique.word().capitalize() + " " + random.choice(["Pro", "X", "Ultra", "Max"]),
                slug=random_slug(),
                description=fake.text(),
                brand=random.choice(["Apple", "Samsung", "Dell", "Sony", "LG", "Asus"]),
                price=price,
                discount_price=discount_price,
                product_type=product_type,
                category=category,
                in_stock=random.choice([True, False]),
                is_top_seller=random.choice([True, False]),
            )
            products.append(product)

        Product.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS(f"✅ Successfully created {count} products!"))

        # Generate characteristics for the created products
        for product in Product.objects.all().order_by("-id")[:count]:
            characteristic_names = CHARACTERISTIC_TEMPLATES.get(product.product_type.name, ["Feature 1", "Feature 2", "Feature 3"])

            # Ensure at least 10 characteristics by repeating the list
            while len(characteristic_names) < 10:
                characteristic_names *= 2  # Duplicate list until sufficient size

            # Randomly select 10 to 18 characteristics per product (with repetition allowed)
            num_characteristics = random.randint(10, 18)
            selected_characteristics = random.choices(characteristic_names, k=num_characteristics)  # Allows duplicates

            for char_name in selected_characteristics:
                # Generate realistic values based on characteristic type
                if "Storage" in char_name or "RAM" in char_name:
                    value = f"{random.choice([4, 8, 16, 32, 64, 128, 256, 512, 1024])}GB"
                elif "Screen Size" in char_name:
                    value = f"{random.choice([5.5, 6.1, 6.7, 13.3, 15.6, 17.3, 27, 32])} inches"
                elif "Battery" in char_name:
                    value = f"{random.choice([2000, 3000, 4000, 5000, 6000, 7000])}mAh"
                elif "Resolution" in char_name:
                    value = random.choice(["720p", "1080p", "1440p", "4K", "8K"])
                elif "Processor" in char_name:
                    value = random.choice(["Intel i3", "Intel i5", "Intel i7", "Intel i9", "Ryzen 5", "Ryzen 7", "M1", "M2"])
                elif "Refresh Rate" in char_name:
                    value = f"{random.choice([60, 75, 120, 144, 165, 240])}Hz"
                elif "Noise Cancellation" in char_name:
                    value = random.choice(["Yes", "No"])
                elif "Bluetooth" in char_name:
                    value = f"v{random.choice([4.0, 4.1, 4.2, 5.0, 5.1, 5.2])}"
                elif "Smart TV" in char_name:
                    value = random.choice(["Yes", "No"])
                elif "Water Resistance" in char_name:
                    value = random.choice(["IP67", "IP68", "None"])
                else:
                    value = fake.word().capitalize()  # Fallback: Random word to simulate a characteristic

                characteristics.append(ProductCharacteristic(product=product, name=char_name, value=value))


        ProductCharacteristic.objects.bulk_create(characteristics)
        self.stdout.write(self.style.SUCCESS(f"✅ Successfully added characteristics to {count} products!"))
