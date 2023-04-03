from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework import status
from base.models import Category,Sub_category
from base.serializer import CategorySerializer
@api_view(['GET'])
def getCategory(request):
    categories=Category.objects.all()
    serializer=CategorySerializer(categories,many=True)
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def addCategory(request):
    category=Category(name=request.data['name'])
    category.save()
    serializer=CategorySerializer(category,many=False)
    return Response(serializer.data)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteCategory(request,pk):
    category=Category(id=pk)
    category.delete()
    content={
            "msg":"Category deleted successfully"
        }
    return Response(content,status=status.HTTP_200_OK) 

@api_view(['POST'])
@permission_classes([IsAdminUser])
def addSubCategory(request):
    category_id=request.data['category_id']
    category=Category.objects.filter(id=category_id)[0]
    sub_category=Sub_category(name=request.data['name'],category_id=category)
    sub_category.save()
    serializer=CategorySerializer(category,many=False)
    return Response(serializer.data) 

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteSubCategory(request,cat_pk,sub_pk):
    Sub_category.objects.filter(id=sub_pk)[0].delete()
    category=Category.objects.filter(id=cat_pk)
    serializer=CategorySerializer(category,many=True)
    return Response(serializer.data)