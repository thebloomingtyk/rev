from rest_framework import serializers
from .models import Product, ProductCategory, ProductSpecification, ProductVariant
from seller.models import Seller


class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'category_name']


class ProductSpecificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductSpecification
        # fields = ['id', 'name']
        fields = '__all__'


class ProductVariantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'


# def validate_field1(value):
#
#     if not value:
#         raise serializers.ValidationError("Field1 is required. Please provide a value.")
#     return value


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = ProductCategorySerializer() #many=True, source='category_set'
    variants = ProductVariantSerializer(many=True, read_only=True) #many=True, source='productvariant_set'
    specification = ProductSpecificationSerializer()

    # TODO add the owner serialized
    # owner = SellerSerializer()

    class Meta:
        model = Product
        fields = ['product_title', 'image', 'category', 'specification', 'description', 'variants']
        
        # fields = '__all__' TODO : BRINGS POPPING WITH A BUNCH OF FIELDS
        # fields = ['product_title', 'image', 'description', 'specification.name', 'variants', 'inventory', 'category']

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        specification_data = validated_data.pop('specification')
        # variants_data = validated_data.pop('variants')

        # seller_data = validated_data.pop('owner')
        # seller, _ = Seller.objects.get_or_create(**seller_data)
        
        category_id = category_data.get('id')
        category_name = category_data.get('name')
        
        if category_id:
            category, _ = ProductCategory.objects.get_or_create(id=category_id)
        elif category_name:
            category, _ = ProductCategory.objects.get_or_create(name=category_name)
        else:
            raise serializers.ValidationError("Category is required. Please provide a value.")
        
        specification_id = specification_data.get('id')
        specification_name = specification_data.get('name')
        if specification_id:
            specification, _ = ProductSpecification.objects.get_or_create(id=specification_id)
        elif specification_name:
            specification, _ = ProductSpecification.objects.get_or_create(name=specification_name)
        else:
            raise serializers.ValidationError("Specification 'id' or 'name' is required.")
        
        # variants_json = serializers.JSONRenderer().render(variants_data)

        product = Product.objects.create(
            category=category,
            specification=specification,
            # variants_json=variants_json,
            **validated_data
        )

        # Handle variants creation
        # for variant_data in variants_data:
        #     ProductVariant.objects.create(product=product, **variant_data)

        return product








        # specification, _ = ProductSpecification.objects.get_or_create(**specification_data)
        # category, _ = ProductCategory.objects.get_or_create(**category_data)

        # # product = Product.objects.create(owner=seller, specification=specification, category=category, **validated_data)
        # product = Product.objects.create(specification=specification, category=category, **validated_data)

        # for variant_data in variants_data:
        #     ProductVariant.objects.create(product=product, **variant_data)
            
        # return product
