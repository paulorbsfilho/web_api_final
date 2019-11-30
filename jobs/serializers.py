from rest_framework import serializers

from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'pk', 'username', 'email']


class UserCreateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'pk', 'username', 'email', 'password']


class EmployerSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Employer
        fields = ['url', 'pk', ]

    # def create(self, validated_data):
    #     username = validated_data['username']
    #     email = validated_data['email']
    #     password = validated_data['password']
    #     user = User.objects.create_user(username=username, email=email, password=password)
    #     user.first_name = validated_data['first_name']
    #     user.last_name = validated_data['last_name']
    #     user.save()
    #     employer = Employer()
    #     employer.phone = validated_data['phone']
    #     employer.user = user
    #     employer.save()
    #     return employer
    #
    # def update(self, instance, validated_data):
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.save()
    #     return instance


class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Candidate
        fields = ['url', 'pk', 'user', 'phone', 'academic_formation']

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        phone = validated_data['phone']
        academic_formation = validated_data['academic_formation']
        institution = validated_data['institution']
        knowledge = validated_data['knowledge']
        bio = validated_data['bio']
        return Candidate.objects.create(user=user,
                                        phone=phone,
                                        academic_formation=academic_formation,
                                        institution=institution,
                                        knowledge=knowledge,
                                        bio=bio,
                                        **validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.academic_formation = validated_data.get('academic_formation', instance.academic_formation)
        instance.institution = validated_data.get('institution', instance.institution)
        instance.knowledge = validated_data.get('knowledge', instance.knowledge)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance


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

    class Meta:
        model = JobAdvertisement
        fields = ['url', 'pk', 'title', 'description', 'requirements', 'desirable', 'payment', 'company']
