# from rest_framework import serializers
from models import Character

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Character