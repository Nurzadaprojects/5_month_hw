from rest_framework import serializers
from product.models import Product, Manager, Review



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = 'id name age birth_year'.split()

class ProductSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer()
    reviews = ReviewSerializer(many=True)
    class Meta:
        model = Product
        fields = 'id title manager color reviews'.split()
        # depth = 1



