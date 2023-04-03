from dataclasses import field, fields
from statistics import mode
from rest_framework import serializers
from .models import Neighborhood, User,Sub_category,Category,Complaint,Contact
from rest_framework_simplejwt.tokens import RefreshToken
class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField('get_token')
    def get_token(self,obj):
        return str(RefreshToken.for_user(obj).access_token)
    class Meta:
        model=User
        fields=['id','first_name','last_name','email','registered_at','is_admin','token']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','first_name','last_name','email','registered_at','is_admin']
class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Neighborhood
        fields='__all__'
class CategorySerializer(serializers.ModelSerializer):
    sub_categories=serializers.SerializerMethodField('get_sub')
    category=serializers.SerializerMethodField('get_cat')
    def get_cat(self,obj):
        return obj.name
    def get_sub(self,obj):
        data=SubCategorySerializer(obj.sub_category_set.all(),many=True)
        return data.data
    class Meta:
        model=Category
        fields=['id','category','sub_categories']      
class SubCategorySerializer(serializers.ModelSerializer):
    sub_category=serializers.SerializerMethodField('get_sub')
    name=serializers.SerializerMethodField('get_name')
    category=serializers.SerializerMethodField('get_category')
    def get_sub(self,obj):
        return obj.name
    def get_name(self,obj):
        return obj.name
    def get_category(self,obj):
        return obj.category_id.name
    class Meta:
        model=Sub_category
        fields=['id','sub_category','name','category']
class ComplaintSerializer(serializers.ModelSerializer):
    contact=serializers.SerializerMethodField('get_contact')
    sub_category=serializers.SerializerMethodField('get_sub')
    neighborhood=serializers.SerializerMethodField('get_neigh')
    user=serializers.SerializerMethodField('get_user')
    def get_contact(self,obj):
        contact=obj.contact_id
        return ContactSerializer(contact,many=False).data
    def get_sub(self,obj):
        sub_cat=obj.category_id
        return SubCategorySerializer(sub_cat,many=False).data
    def get_neigh(self,obj):
        neigh=obj.neighborhood_id
        return NeighborhoodSerializer(neigh,many=False).data
    def get_user(self,obj):
        user=obj.users_id
        return UserSerializer(user,many=False).data
    class Meta:
        model=Complaint
        fields=['id','description','topic','neighborhood','user','sub_category','img','created_at','contact','replied_at','is_replied','response']
    
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields='__all__'