from django.contrib.auth.models import User

from rest_framework import serializers

from .models import (
    Trainer,
    Member,
    MembershipPlan,
    Membership,
    Payment,
    Student
)


# User Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password'
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  
        

# Trainer Serializer
class TrainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trainer
        fields = '__all__'


# Member Serializer
class MemberSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Member
        fields = '__all__'


# Membership Plan Serializer
class MembershipPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = MembershipPlan
        fields = '__all__'


# Membership Serializer
class MembershipSerializer(serializers.ModelSerializer):

    member_name = serializers.CharField(
        source='member.user.username',
        read_only=True
    )

    plan_name = serializers.CharField(
        source='plan.name',
        read_only=True
    )

    class Meta:
        model = Membership
        fields = '__all__'


# Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):

    member_name = serializers.CharField(
        source='membership.member.user.username',
        read_only=True
    )

    class Meta:
        model = Payment
        fields = '__all__'