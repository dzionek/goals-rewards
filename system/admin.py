from django.contrib import admin

from .models import DirectReward, PointReward, Goal, UserPoint


admin.site.register(DirectReward)
admin.site.register(PointReward)
admin.site.register(Goal)
admin.site.register(UserPoint)
