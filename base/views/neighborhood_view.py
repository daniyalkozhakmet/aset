from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework import status
from base.models import Neighborhood
from base.serializer import NeighborhoodSerializer
@api_view(['GET'])
def getNeighborhoods(request):
    neighborhoods=Neighborhood.objects.all()
    serializer=NeighborhoodSerializer(neighborhoods,many=True)
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def addNeighborhood(request):
    neighborhood=Neighborhood(name=request.data['name'])
    neighborhood.save()
    serializer=NeighborhoodSerializer(neighborhood,many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteNeighborhood(request,pk):
    neighborhood=Neighborhood(id=pk)
    neighborhood.delete()
    content={
        "message":"Neighborhood deleted successfully"
    }
    return Response(content,status=status.HTTP_200_OK)