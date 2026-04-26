from rest_framework import serializers
from .models import Productos

class ProductoCompletoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = "__all__"

class ProductoParcialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = "__all__"
