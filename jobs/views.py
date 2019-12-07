from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import ScopedRateThrottle

from jobs.permissions import *
from jobs.serializers import *


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request):
        return Response({
            'users': reverse(UserListView.name, request=request),
            'signup-employer': reverse(EmployerCreateView.name, request=request),
            'employers': reverse(EmployerListView.name, request=request),
            'signup-candidate': reverse(CandidateCreateView.name, request=request),
            'candidates': reverse(CandidateListView.name, request=request),
            'job-advertisements': reverse(JobAdvertisementListView.name, request=request),
            'companies': reverse(CompanyListView.name, request=request),
        })


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'
    permission_classes = [permissions.IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'
    permission_classes = [permissions.IsAdminUser]


class EmployerCreateView(generics.CreateAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    name = 'employer-create'

    def perform_create(self, serializer):
        data = self.request.data
        user = User.objects.create_user(data['username'], data['email'], data['password'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()
        serializer.save(user=user, phone=data['phone'])


class EmployerListView(generics.ListAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    name = 'employer-list'
    permission_classes = [permissions.IsAdminUser]


class EmployerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    name = 'employer-detail'
    permission_classes = [permissions.IsAdminUser, IsSelf]


class CandidateCreateView(generics.CreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    name = 'candidate-create'

    def perform_create(self, serializer):
        data = self.request.data
        user = User.objects.create_user(data['username'], data['email'], data['password'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()
        serializer.save(user=user, phone=data['phone'])


class CandidateListView(generics.ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    name = 'candidate-list'
    permission_classes = [IsEmployer, permissions.IsAdminUser]


class CandidateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    name = 'candidate-detail'
    permission_classes = [permissions.IsAdminUser, IsSelf]


class CompanyListView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    name = 'company-list'
    permission_classes = [permissions.IsAdminUser, IsEmployerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    name = 'company-detail'
    permission_classes = [permissions.IsAdminUser, IsOwner]


class JobAdvertisementCreateView(generics.CreateAPIView):
    queryset = JobAdvertisement.objects.all()
    serializer_class = JobAdvertisementDetailSerializer
    name = 'jobadvertisement-create'
    permission_classes = [permissions.IsAdminUser, IsEmployer]

    def perform_create(self, serializer):
        owner = self.request.user
        company = Company.objects.get(name=self.request.data['company'])
        if company.owner == owner:
            serializer.save(owner=owner, company=company)
        else:
            res = {"\"info\":\"Essa empresa não pertece a você.\""}
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)


class JobAdvertisementListView(generics.ListAPIView):
    queryset = JobAdvertisement.objects.all()
    serializer_class = JobAdvertisementListSerializer
    name = 'jobadvertisement-list'


class JobAdvertisementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobAdvertisement.objects.all()
    serializer_class = JobAdvertisementDetailSerializer
    name = 'jobadvertisement-detail'
    permission_classes = [permissions.IsAdminUser, IsOwnerOrReadyOnly, IsEmployerOrReadOnly]


class CustomAuthTokenView(ObtainAuthToken):
    name = 'auth-token'
    throttle_scope = 'custom-auth-token'
    throttle_classes = [ScopedRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        self.check_throttles(request)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'name': user.username,
            'email': user.email,
        })
