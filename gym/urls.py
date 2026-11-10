from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    TrainerViewSet,
    MemberViewSet,
    MembershipPlanViewSet,
    MembershipViewSet,
    PaymentViewSet,
    studentViewSet,
)


router = DefaultRouter()

router.register('trainers', TrainerViewSet, basename='trainer')

router.register('members', MemberViewSet, basename='member')

router.register('plans', MembershipPlanViewSet, basename='plan')

router.register('memberships', MembershipViewSet, basename='membership')

router.register('payments', PaymentViewSet, basename='payment')

router.register('students', studentViewSet, basename='student')


urlpatterns = [

    path('register/', RegisterView.as_view()),

    path('', include(router.urls)),

]