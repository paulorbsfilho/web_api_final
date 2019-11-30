from rest_framework import generics
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
            'users': reverse(UserList.name, request=request),
            'employers': reverse(EmployerList.name, request=request),
            'candidates': reverse(CandidateList.name, request=request),
            'job-advertisements': reverse(JobAdvertisementList.name, request=request),
        })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'
    permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'
    permission_classes = [permissions.IsAdminUser]


class EmployerList(generics.ListCreateAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    name = 'employer-list'

    def perform_create(self, serializer):
        data = self.request.data
        user = User.objects.create_user(data['username'], data['email'], data['password'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()
        serializer.save(user=user, phone=data['phone'])


class EmployerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    name = 'employer-detail'
    permission_classes = [permissions.IsAdminUser]


class CandidateList(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    name = 'candidate-list'

    def perform_create(self, serializer):
        data = self.request.data
        user = User.objects.create_user(data['username'], data['email'], data['password'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()
        serializer.save(user=user, phone=data['phone'])


class CandidateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    name = 'candidate-detail'
    permission_classes = [permissions.IsAdminUser]


class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    name = 'company-list'


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    name = 'company-detail'


class JobAdvertisementList(generics.ListAPIView):
    queryset = JobAdvertisement.objects.all()
    serializer_class = JobAdvertisementListSerializer
    name = 'jobs-list'


class JobAdvertisementCreate(generics.CreateAPIView):
    queryset = JobAdvertisement.objects.all()
    serializer_class = JobAdvertisementDetailSerializer
    name = 'jobs-create'
    permission_classes = [IsEmployerOrReadyOnly]


class JobAdvertisementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobAdvertisement.objects.all()
    serializer_class = JobAdvertisementDetailSerializer
    name = 'jobs-detail'


class CustomAuthToken(ObtainAuthToken):
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
