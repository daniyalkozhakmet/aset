from ast import Pass
import enum
from unicodedata import category
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from django.db.models.functions import TruncMonth
from rest_framework import status
import datetime
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from base.models import Complaint,User,Sub_category,Neighborhood,Contact
from base.serializer import ComplaintSerializer
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createComplaint(request):
    users_id=User.objects.filter(email=request.user)[0]
    description=request.data['description']
    topic=request.data['topic']
    contact=request.data['contact']
    category_id=request.data['category_id']
    neighborhood_id=request.data['neighborhood_id']
    if description=='' or topic=='' or category_id=='' or neighborhood_id=='':
        content={
            "msg":"Please fill in all fields"
        } 
        return Response(content,status=status.HTTP_400_BAD_REQUEST)
    if contact['email']=='' or contact['phone']=='':
        complaint=Complaint(topic=topic,description=description,category_id=Sub_category.objects.filter(id=category_id)[0],neighborhood_id=Neighborhood.objects.filter(id=neighborhood_id)[0],users_id=users_id)
        complaint.save()
        serializer=ComplaintSerializer(complaint,many=False)
        return Response(serializer.data)
    else:
        contact=Contact(phone=contact['phone'],email=contact['email'])
        contact.save()
        complaint=Complaint(topic=topic,description=description,category_id=Sub_category.objects.filter(id=category_id)[0],neighborhood_id=Neighborhood.objects.filter(id=neighborhood_id)[0],users_id=users_id,contact_id=contact)
        complaint.save()
        serializer=ComplaintSerializer(complaint,many=False)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getComplaints(request):
    page=request.GET.get('page')
    complaints=Complaint.objects.filter(users_id=User.objects.filter(email=request.user)[0]).order_by('id')
    p = Paginator(complaints, 5)
    pages=p.num_pages
    try:
        pageList = p.page(page).object_list
    except PageNotAnInteger:
        pageList = p.page(1).object_list
    except EmptyPage:
        pageList = p.page(p.num_pages).object_list
    serializer=ComplaintSerializer(pageList,many=True)
    return Response({"page":page,"pages":pages,"complaints":serializer.data})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getComplaintByID(request,pk):
    complaint=Complaint.objects.filter(users_id=User.objects.filter(email=request.user)[0]).filter(id=pk)[0]
    serializer=ComplaintSerializer(complaint,many=False)
    return Response(serializer.data)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteComplaint(request,pk):
    complaint=Complaint.objects.filter(users_id=User.objects.filter(email=request.user)[0]).filter(id=pk)[0]
    if complaint:
        complaint.delete()
    content={
        "msg":"Complaint is deleted successfully"
    }
    return Response(content,status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getComplaintsByAdmin(request):
    page=request.GET.get('page')
    complaints=Complaint.objects.all().order_by('id')
    p = Paginator(complaints, 5)
    pages=p.num_pages
    try:
        pageList = p.page(page).object_list
    except PageNotAnInteger:
        pageList = p.page(1).object_list
    except EmptyPage:
        pageList = p.page(p.num_pages).object_list
    serializer=ComplaintSerializer(pageList,many=True)
    return Response({"page":page,"pages":pages,"complaints":serializer.data})
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getComplaintByIDAdmin(request,pk):
    complaint=Complaint.objects.filter(id=pk)[0]
    serializer=ComplaintSerializer(complaint,many=False)
    return Response(serializer.data)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateComplaint(request,pk):
    description=request.data['description']
    topic=request.data['topic']
    contact=request.data['contact']
    category_id=request.data['category_id']
    neighborhood_id=request.data['neighborhood_id']
    if description=='' or topic=='' or category_id=='' or neighborhood_id=='':
        content={
            "msg":"Please fill in all fields"
        } 
        return Response(content,status=status.HTTP_400_BAD_REQUEST)
    complaint=Complaint.objects.filter(id=pk)[0]
    category=Sub_category.objects.filter(id=category_id)[0]
    neighborhood=Neighborhood.objects.filter(id=neighborhood_id)[0]
    if contact['email']!='' or contact['phone']!='':
        contact=Contact(email=contact['email'],phone=contact['phone'])
        contact.save()
        complaint.description=description
        complaint.topic=topic
        complaint.category_id=category
        complaint.neighborhood_id=neighborhood
        complaint.contact_id=contact
        complaint.save()
        serializer=ComplaintSerializer(complaint,many=False)
        return Response(serializer.data)
    else:
        complaint.description=description
        complaint.topic=topic
        complaint.category_id=category
        complaint.neighborhood_id=neighborhood
        complaint.save()
        serializer=ComplaintSerializer(complaint,many=False)
        return Response(serializer.data)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateComplaintByAdmin(request,pk):
    complaint=Complaint.objects.filter(id=pk)[0]
    data=request.data
    if data['response']!='':
        complaint.response=data['response']
        complaint.is_replied=True
        complaint.replied_at=datetime.datetime.now()
        complaint.save()
    serializer=ComplaintSerializer(complaint,many=False)
    return Response(serializer.data)
@api_view(['POST'])
def uploadImage(request,pk):
    complaint = Complaint.objects.filter(id=pk)[0]
    complaint.img = request.FILES.get('image')
    complaint.save()
    return Response("Image is uploaded")
@api_view(['GET'])
@permission_classes([IsAdminUser])     
def complaintStatistic(request):
    compliant=Complaint.objects.all()
    category=[c.category_id.category_id.name for c in compliant]
    data=[]
    for i in set(category):
        duplicateFrequencies = {}
        duplicateFrequencies['name'] = i
        duplicateFrequencies['count'] = category.count(i)
        data.append(duplicateFrequencies)
    return Response(data)