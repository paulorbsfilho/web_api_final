from rest_framework import serializers

from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'pk', 'username', 'email']


class EmployerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Employer
        fields = ['url', 'pk', 'user']


class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Candidate
        fields = ['url', 'pk', 'user', 'phone', 'academic_formation', 'bio']


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Company
        fields = ['url', 'pk', 'name', 'owner', 'catchPhrase', 'about']


class JobAdvertisementListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = JobAdvertisement
        fields = ['url', 'pk', 'title', 'payment']


class JobAdvertisementDetailSerializer(serializers.HyperlinkedModelSerializer):
    company = serializers.SlugRelatedField(queryset=Company.objects.all(), slug_field='name')

    class Meta:
        model = JobAdvertisement
        fields = ['url', 'pk', 'title', 'description', 'requirements', 'desirable', 'payment', 'company']
