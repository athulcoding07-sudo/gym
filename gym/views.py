from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import (
    Trainer,
    Member,
    MembershipPlan,
    Membership,
    Payment,
    Student
    
)

from .serializers import (
    RegisterSerializer,
    TrainerSerializer,
    MemberSerializer,
    MembershipPlanSerializer,
    MembershipSerializer,
    PaymentSerializer,
    StudentSerializer,
)


# Registration API
class RegisterView(CreateAPIView):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer

    permission_classes = [AllowAny]

    authentication_classes = []


# Trainer API
class TrainerViewSet(viewsets.ModelViewSet):

    queryset = Trainer.objects.all()

    serializer_class = TrainerSerializer

    permission_classes = [IsAuthenticated]


# Member API
class MemberViewSet(viewsets.ModelViewSet):

    queryset = Member.objects.select_related(
        'user',
        'trainer'
    )

    serializer_class = MemberSerializer

    permission_classes = [IsAuthenticated]


# Membership Plan API
class MembershipPlanViewSet(viewsets.ModelViewSet):

    queryset = MembershipPlan.objects.all()

    serializer_class = MembershipPlanSerializer

    permission_classes = [IsAuthenticated]


# Membership API
class MembershipViewSet(viewsets.ModelViewSet):

    queryset = Membership.objects.select_related(
        'member__user',
        'plan'
    )

    serializer_class = MembershipSerializer

    permission_classes = [IsAuthenticated]



class studentViewSet(viewsets.ModelViewSet):

    queryset = Student.objects.all()

    serializer_class = StudentSerializer

    permission_classes = [AllowAny]

    

# Payment API
class PaymentViewSet(viewsets.ModelViewSet):

    queryset = Payment.objects.select_related(
        'membership__member__user',
        'membership__plan'
    )

    serializer_class = PaymentSerializer

    permission_classes = [IsAuthenticated]
       