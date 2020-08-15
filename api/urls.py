from rest_framework import routers

from . import views


router = routers.SimpleRouter()

# Admin
router.register(
    r'admin/users', views.AdminUserViewSet
)
router.register(
    r'admin/goals', views.AdminGoalViewSet
)
router.register(
    r'admin/direct-rewards', views.AdminDirectRewardViewSet
)
router.register(
    r'admin/point-rewards', views.AdminPointRewardViewSet
)

# User-specific
router.register(
    r'goals', views.GoalViewSet, basename='GoalView'
)
router.register(
    r'direct-rewards', views.DirectRewardViewSet, basename='DirectRewardView'
)
router.register(
    r'point-rewards', views.PointRewardViewSet, basename='PointRewardView'
)

urlpatterns = router.urls
