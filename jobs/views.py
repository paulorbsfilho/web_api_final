from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import ScopedRateThrottle
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication

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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAdminUser, TokenHasReadWriteScope]
    required_scopes = ['read:user']


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'
    permission_classes = [permissions.IsAdminUser, TokenHasReadWriteScope]
    required_scopes = ['write:user']


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
        company = Company()
        company.company_name = data['company_name']
        company.catchPhrase = data['catchPhrase']
        company.about = data['about']
        company.owner = user
        company.save()
        serializer.save(user=user, phone=data['phone'])


class EmployerListView(generics.ListAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    name = 'employer-list'
    permission_classes = [permissions.IsAdminUser]
    required_scopes = ['read:employer']


class EmployerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    name = 'employer-detail'
    permission_classes = [permissions.IsAdminUser, IsSelf]
    required_scopes = ['write:employer']


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
    filterset_fields = ['user', 'phone', 'academic_formation', 'bio']
    search_fields = ['^user', 'academic_formation']
    ordering_fields = ['pk', 'user', 'phone', 'academic_formation', 'bio']
    name = 'candidate-list'
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope, IsEmployer]
    required_scopes = ['read:candidate']


class CandidateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    name = 'candidate-detail'
    permission_classes = [permissions.IsAdminUser, IsSelf, TokenHasScope]
    required_scopes = ['write:candidate']


class CompanyListView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    name = 'company-list'
    permission_classes = [permissions.IsAdminUser, IsEmployerOrReadOnly, TokenHasReadWriteScope]
    required_scopes = ['read:company', 'write:company']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    name = 'company-detail'
    permission_classes = [permissions.IsAdminUser, IsOwner, TokenHasScope]
    required_scopes = ['write:company']


class JobAdvertisementCreateView(generics.CreateAPIView):
    queryset = JobAdvertisement.objects.all()
    serializer_class = JobAdvertisementDetailSerializer
    name = 'jobadvertisement-create'
    permission_classes = [IsEmployer]

    def perform_create(self, serializer):
        owner = self.request.user
        company = Company.objects.get(name=self.request.data['company'])
        try:
            if company.owner == owner:
                serializer.save(owner=owner, company=company)
        except:
            print("!A empresa não é sua!\n")
            raise Exception


class JobAdvertisementListView(generics.ListAPIView):
    queryset = JobAdvertisement.objects.all()
    serializer_class = JobAdvertisementListSerializer
    filterset_fields = ['title', 'payment']
    search_fields = ['^title']
    ordering_fields = ['title', 'payment']
    throttle_scope = 'job-view'
    throttle_classes = (ScopedRateThrottle,)
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read:ad']
    name = 'jobadvertisement-list'

    def get_queryset(self):
        return JobAdvertisement.objects.filter(owner=self.request.user)


class JobAdvertisementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobAdvertisement.objects.all()
    serializer_class = JobAdvertisementDetailSerializer
    name = 'jobadvertisement-detail'
    permission_classes = [permissions.IsAdminUser, IsOwnerOrReadyOnly, IsEmployerOrReadOnly]
    required_scopes = ['write:company']


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
