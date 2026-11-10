from django.contrib import admin

from .models import (
    Trainer,
    Member,
    MembershipPlan,
    Membership,
    Payment
)

admin.site.register(Trainer)
admin.site.register(Member)
admin.site.register(MembershipPlan)
admin.site.register(Membership)
admin.site.register(Payment)