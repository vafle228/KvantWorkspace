from LoginApp.models import KvantUser
from rest_framework import serializers

from .models import *


class PersonalityDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalityDocument
        exclude = ('id', )


class LivingAdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LivingAdress
        exclude = ('id', )


class StudentParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentParent
        exclude = ('id', )


class StudyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyDocument
        exclude = ('id', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = KvantUser
        fields = ('surname', 'name', 'patronymic', 'email', )


class StudentPersonalInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    adress = LivingAdressSerializer()
    mother = StudentParentSerializer()
    father = StudentParentSerializer()
    document = PersonalityDocumentSerializer()

    class Meta:
        model = StudentPersonalInfo
        exclude = ('id', )


class StaffPersonalInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    adress = LivingAdressSerializer()
    study = StudyDocumentSerializer()
    document = PersonalityDocumentSerializer()

    class Meta:
        model = StaffPersonalInfo
        exclude = ('id', )
