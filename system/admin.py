from django.contrib import admin

from .models import DirectReward, PointReward, Goal


admin.site.register(DirectReward)
admin.site.register(PointReward)
admin.site.register(Goal)
