from django.db import models


class ProductCategory(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Product Categories'


# TODO - product specification and product variant should be in a separate app
# TODO or the technical difference between the two should be clear

class ProductSpecification(models.Model):
    # product_name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    description = models.TextField()
    strength = models.CharField(max_length=50, blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True)

    # product_name = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.weight}: {self.value}"


class Product(models.Model):
    # TODO add the owner field
    # owner = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/products/')
    description = models.TextField()
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    # price_per_item = models.DecimalField(max_digits=10, decimal_places=2)

    specification = models.ForeignKey('ProductSpecification',
                                      on_delete=models.SET_NULL, related_name='specifications', blank=True, null=True)
    # variant = models.ForeignKey('ProductVariant', on_delete=models.SET_NULL, null=True, blank=True)
    inventory = models.PositiveIntegerField()
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.product_title

    class Meta:
        ordering = ['product_title']
    
    
class ProductVariant(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE), 
    product_specification = models.ForeignKey('ProductSpecification', on_delete=models.CASCADE, blank=True, null=True)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    sku = models.CharField(max_length=50, unique=True)
    quantity = models.PositiveIntegerField()
    
    # TODO sku should be unique for each product variant, and should be auto generated, and it should be a property of the product variant

    def __str__(self):
        return self.sku
    
    
# class Product(models.Model):
#     product_title = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='images/products/')
#     description = models.TextField()
#     specification = models.ForeignKey('ProductSpecification',
#                                       on_delete=models.SET_NULL, related_name='specifications', blank=True, null=True)
#     inventory = models.PositiveIntegerField()
#     category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)

# product title, image, and description. The fields from the specification, inventory, category should not be shown exept for the category name, product specification name and the variant name should be shown as te list so they can be chosen when creating a new product



