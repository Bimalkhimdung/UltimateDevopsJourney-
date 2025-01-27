from django.shortcuts import render
from rest_framework.decorators import *
from rest_framework.response import Response
from .models import User
from .models import legal_info
# Create your views here.
@api_view(['GET','POST','DELETE'])
def user(request):
        return Response({'user_id = User.objects.all().values()'})

@api_view(['GET'])
def legal_info(request):
        legal_details = legal_info.objects.all().values()
        return Response(list(legal_details))