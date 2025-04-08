from modeltranslation.translator import TranslationOptions, register

from .models import Product, ProductType, Category, ProductCharacteristic

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(ProductType)
class ProductTypeTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):    
    fields = ('name', 'description', )

@register(ProductCharacteristic)
class ProductCharacteristicTranslationOptions(TranslationOptions):
    fields = ('name', 'value', )