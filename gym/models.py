from django.db import models
from django.contrib.auth.models import User


# 1. Trainer Model
class Trainer(models.Model):

    full_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    specialization = models.CharField(max_length=100)

    experience = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


# 2. Member Model
class Member(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='gym_profile'
    )

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )

    phone = models.CharField(max_length=15)

    age = models.PositiveIntegerField()

    joined_date = models.DateField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


# 3. Membership Plan Model
class MembershipPlan(models.Model):

    PLAN_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]

    name = models.CharField(max_length=100)

    plan_type = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES
    )

    duration_days = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 4. Membership Model
class Membership(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='memberships'
    )

    plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.PROTECT,
        related_name='memberships'
    )

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.plan}"

    

class Student(models.Model):
    name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    age = models.PositiveIntegerField()

    enrolled_date = models.DateField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


    

# 5. Payment Model
class Payment(models.Model):

    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('online', 'Online'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    membership = models.ForeignKey(
        Membership,
        on_delete=models.PROTECT,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.membership.member} - {self.amount}"

