from rest_framework import serializers
from .models import Product, Manager, Review
from rest_framework.exceptions import ValidationError



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

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, min_length=3)
    description = serializers.CharField(required=False)
    price = serializers.IntegerField(required=True)
    category = serializers.FloatField(required=True)
    manager_id = serializers.IntegerField()

    def validate_manager_id(self, manager_id):
        try:
            Manager.objects.get(id=manager_id)
        except Manager.DoesNotExist:
            raise ValidationError("Manager does not found!")
        return manager_id





class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=100)
    stars = serializers.IntegerField()


