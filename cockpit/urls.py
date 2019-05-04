from django.urls import path, include
from . import views
from rest_framework import routers


# If we have /api/ in URL then do this according to DJango rest framework
router = routers.DefaultRouter()
router.register('feedback', views.feedbackView)
router.register('analyzedfeedback', views.analyzedfeedbackView)
router.register('wish', views.wishView)
router.register('democratic', views.demoView)
router.register('account', views.accountView)
router.register('related', views.relatedFeedbacksView)
router.register('game', views.gameView)


urlpatterns = [
    path('', views.index),
    path('postfeedback', views.postFeedback),  # POST feedback custom API
    path('getrelated', views.getRelated),  # Get Relations Custom API
    path('postissue', views.postIssue),  # POST issues custom API
    path('authenticate', views.logincheck),  # Login authentication
    path('api/', include(router.urls)),
]
