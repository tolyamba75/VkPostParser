from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, ProcessingGroupViewSet, RecipientViewSet


router = DefaultRouter()
router.register(r'account', RecipientViewSet)
router.register(r'task', TaskViewSet)
router.register(r'processing', ProcessingGroupViewSet)

urlpatterns = router.urls
