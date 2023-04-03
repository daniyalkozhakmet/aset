from datetime import date
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.db import connection
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from base.models import User
from base.serializer import UserSerializerWithToken,UserSerializer
# Create your views here.
@api_view(['POST'])
def register(request):
    data=request.data
    if len(User.objects.filter(email=data['email']))>0:
        content={
            "message":"User with that ID already exist"
        }
        return Response(content,status=status.HTTP_400_BAD_REQUEST)
    elif data['first_name'] is not None  and  data['last_name'] is not None:
        print(data['password'])
        user=User(email=data['email'],password=make_password(data['password']),first_name=data['first_name'],last_name=data['last_name'])
        user.save()
        serializer=UserSerializerWithToken(user,many=False)
        return Response(serializer.data)
    else:
        content={
            "message":"Please provide all fields"
        }
        return Response(content,status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def login(request):
    email=request.data['email']
    password=request.data['password']
    print(User.objects.filter(email=email)[0].check_password(password))
    if len(User.objects.filter(email=email))==0:
        content={
            "msg":"Invalid Credentials"
        }
        return Response(content,status=status.HTTP_400_BAD_REQUEST)
    elif User.objects.filter(email=email)[0].check_password(password):
        serializer=UserSerializerWithToken(User.objects.filter(email=email)[0],many=False)
        return Response(serializer.data)
    else:
        content={
            "msg":"Invalid Credentials"
        }
        return Response(content,status=status.HTTP_400_BAD_REQUEST)        
#get Profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    profile=User.objects.filter(email=request.user)[0]
    serializer=UserSerializer(profile,many=False)
    return Response(serializer.data)
    
#get Profiles by admin
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getProfilesAdmin(request):
    page=request.GET.get('page')
    profiles=User.objects.all().order_by('id')
    p = Paginator(profiles, 5)
    pages=p.num_pages
    try:
        pageList = p.page(page).object_list
    except PageNotAnInteger:
        pageList = p.page(1).object_list
    except EmptyPage:
        pageList = p.page(p.num_pages).object_list
    serializer=UserSerializer(pageList,many=True)
    return Response({"page":page,"pages":pages,"users":serializer.data})

#get Profiles by admin
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getProfileByIdAdmin(request,pk):
    profile=User.objects.filter(id=pk)
    if len(profile)==0:
        content={
            "msg":"User with that ID does not exist"
        }
        return Response(content,status=status.HTTP_400_BAD_REQUEST)         
    serializer=UserSerializer(profile[0],many=False)
    return Response(serializer.data)
    
#UPDATE profile
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    data=request.data
    print(data)
    profile=User.objects.filter(email=request.user)[0]
    profile.email=data['email']
    profile.first_name=data['first_name']
    profile.last_name=data['last_name']
    if data['password']!='':
        print('PASSWORD SET')
        profile.password=make_password(data['password'])
    print(profile)
    profile.save()
    return Response(UserSerializer(profile,many=False).data)
#UPDATE profile
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProfileAdmin(request,pk):
    data=request.data
    profile=User.objects.filter(id=pk)[0]
    profile.email=data['email']
    profile.first_name=data['first_name']
    profile.last_name=data['last_name']
    if data['is_admin']:
        profile.is_admin=data['is_admin']
    if data['password']!='' or data['password'] is not None :
        profile.password=make_password(data['password'])
    profile.save()
    return Response(UserSerializer(profile,many=False).data)
#DELETE profile BY admin
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProfile(request,pk):
    user=User.objects.filter(id=pk)[0]
    user.delete()
    content={
            "msg":"User deleted successfully"
        }
    return Response(content,status=status.HTTP_200_OK)   
@api_view(['GET'])
@permission_classes([IsAdminUser])     
def userStatistic(request):
    sta=User.objects.all() \
    .annotate(user_to_month=TruncMonth("registered_at")) \
    .values("user_to_month") \
    .annotate(count=Count("id")) \
    .order_by("-user_to_month")
    return Response({"data":list(sta)})
    

