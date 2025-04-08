from django.db import models
from django.utils.text import slugify
import random
from django.urls import reverse
import string

def random_slug():
    """
    A function that generates a random slug of length 3 using lowercase letters and digits.
    """
    return ''.join(random.choises(string.ascii_lowercase + string.digits) for _ in range(3))


class Category(models.Model):
    name = models.CharField("Category", max_length=120, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children',null=True, blank=True)
    image_link = models.ImageField("Image", upload_to='categories/%Y/%m/%d', blank=True, null=True)
    slug = models.SlugField("URL",max_length=120, unique=True, null=False, editable=True)

    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(random_slug() + '-ahmad' + self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_category_path(self):
        """Returns a list of category names from the root to this category."""
        path = []
        category = self
        while category:
            path.append(category.name)
            category = category.parent
        return " > ".join(reversed(path))
    
    def get_absolute_url(self):
        return reverse('app:category_detail', kwargs={'category_slug': self.slug})

class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField("URL",max_length=250)
    published_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    images = models.ImageField("Image", upload_to='product_images/%Y/%m/%d', null=True, blank=True)
    image_2 = models.ImageField("Image2", upload_to='product_images/%Y/%m/%d', null=True, blank=True)
    image_3 = models.ImageField("Image3", upload_to='product_images/%Y/%m/%d', null=True, blank=True)
    image_4 = models.ImageField("Image4", upload_to='product_images/%Y/%m/%d', null=True, blank=True)
    in_stock = models.BooleanField(default=True)  
    is_top_seller = models.BooleanField(default=False)  

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    def discount_percentage(self):
        if self.discount_price:
            return ((self.price - self.discount_price) / self.price) * 100
        return 0
    
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[str(self.slug)])

class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, related_name='characteristics', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
