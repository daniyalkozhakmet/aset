from django.urls import path
from .views.user_view import register,login,getProfile,getProfilesAdmin,getProfileByIdAdmin,updateProfile,deleteProfile,updateProfileAdmin,userStatistic
from .views.neighborhood_view import getNeighborhoods,addNeighborhood,deleteNeighborhood
from .views.category_view import getCategory,addCategory,deleteCategory,addSubCategory,deleteSubCategory
from .views.complaint_view import createComplaint,getComplaints,getComplaintByID,deleteComplaint,getComplaintsByAdmin,getComplaintByIDAdmin,updateComplaint,updateComplaintByAdmin,uploadImage,complaintStatistic
urlpatterns = [
    path('user/register',register),
    path('user/login',login),
    path('user/profile',getProfile),
    path('user/profile/update',updateProfile),
    path('user/admin/profiles',getProfilesAdmin),
    path('user/admin/statistics',userStatistic),
    path('user/admin/profile/<str:pk>',getProfileByIdAdmin),
    path('user/admin/profile/delete/<str:pk>',deleteProfile),
    path('user/admin/profile/update/<str:pk>',updateProfileAdmin),
]
urlpatterns+=[
    path('neighborhood/',getNeighborhoods),
    path('neighborhood/add',addNeighborhood),
    path('neighborhood/delete/<str:pk>',deleteNeighborhood),
]
urlpatterns+=[
    path('category/',getCategory),
    path('category/statistics',complaintStatistic),
    path('category/add',addCategory),
    path('category/delete/<str:pk>',deleteCategory),
    path('category/sub/add',addSubCategory),
    path('category/sub/delete/<str:cat_pk>/<str:sub_pk>',deleteSubCategory),
]
urlpatterns+=[
    path('complaint/add',createComplaint),
    path('complaint/get',getComplaints),
    path('complaint/get/admin',getComplaintsByAdmin),
    path('complaint/get/<str:pk>',getComplaintByID),
    path('complaint/get/admin/<str:pk>',getComplaintByIDAdmin),
    path('complaint/delete/<str:pk>',deleteComplaint),
    path('complaint/update/<str:pk>',updateComplaint),
    path('complaint/update/admin/<str:pk>',updateComplaintByAdmin),
    path('upload/<str:pk>',uploadImage),

]