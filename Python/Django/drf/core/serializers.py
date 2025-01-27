from rest_framework import serializers
from models import User
from models import legal_info
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id','firstname','middlename','lastname','address','phonenumber']

        
