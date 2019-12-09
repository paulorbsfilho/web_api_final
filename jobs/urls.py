from django.urls import path, include

from jobs import views

urlpatterns = [
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
    path('o/', include('oauth2_provider.urls')),

    path('api_auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.CustomAuthTokenView.as_view(), name=views.CustomAuthTokenView.name),

    path('users/', views.UserListView.as_view(), name=views.UserListView.name),
    path('users/<int:pk>', views.UserDetailView.as_view(), name=views.UserDetailView.name),

    path('sign-up-employer/', views.EmployerCreateView.as_view(), name=views.EmployerCreateView.name),
    path('employers/', views.EmployerListView.as_view(), name=views.EmployerListView.name),
    path('employers/<int:pk>', views.EmployerDetailView.as_view(), name=views.EmployerDetailView.name),

    path('sign-up-candidate/', views.CandidateCreateView.as_view(), name=views.CandidateCreateView.name),
    path('candidates/', views.CandidateListView.as_view(), name=views.CandidateListView.name),
    path('users/<int:pk>', views.CandidateDetailView.as_view(), name=views.CandidateDetailView.name),

    path('companies/', views.CompanyListView.as_view(), name=views.CompanyListView.name),
    path('companies/<int:pk>', views.CompanyDetailView.as_view(), name=views.CompanyDetailView.name),

    path('users/', views.UserListView.as_view(), name=views.UserListView.name),
    path('users/<int:pk>', views.UserDetailView.as_view(), name=views.UserDetailView.name),

    path('advertise-job/', views.JobAdvertisementCreateView.as_view(),
         name=views.JobAdvertisementCreateView.name),
    path('jobs-advertisements/', views.JobAdvertisementListView.as_view(),
         name=views.JobAdvertisementListView.name),
    path('jobs-advertisements/<int:pk>', views.JobAdvertisementDetailView.as_view(),
         name=views.JobAdvertisementDetailView.name),
]
