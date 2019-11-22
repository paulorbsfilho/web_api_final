from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),

    path('api_auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name=views.CustomAuthToken.name),

    path('sign-up/', views.UserCreate.as_view(), name=views.UserCreate.name),
    path('users/', views.UserList.as_view(), name=views.UserList.name),
    path('users/<int:pk>', views.UserDetail.as_view(), name=views.UserDetail.name),

    path('employers/', views.EmployerList.as_view(), name=views.EmployerList.name),
    path('employers/<int:pk>', views.EmployerDetail.as_view(), name=views.EmployerDetail.name),

    path('candidates/', views.CandidateList.as_view(), name=views.CandidateList.name),
    path('users/<int:pk>', views.CandidateDetail.as_view(), name=views.CandidateDetail.name),

    path('companies/', views.CompanyList.as_view(), name=views.CompanyList.name),
    path('companies/<int:pk>', views.CompanyDetail.as_view(), name=views.CompanyDetail.name),

    path('users/', views.UserList.as_view(), name=views.UserList.name),
    path('users/<int:pk>', views.UserDetail.as_view(), name=views.UserDetail.name),

    path('jobs-advertisements/', views.JobAdvertisementList.as_view(),
         name=views.JobAdvertisementList.name),
    path('jobs-advertisements/<int:pk>', views.JobAdvertisementDetail.as_view(),
         name=views.JobAdvertisementDetail.name),
]
