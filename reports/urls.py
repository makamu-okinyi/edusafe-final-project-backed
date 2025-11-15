# reports/urls.py
# pylint: disable=no-name-in-module
from django.urls import path
from .views import (
    ReportCreateView, 
    ReportStatusView, 
    ReportChatView, 
    DashboardStatsView,
    ForumPostListCreateView,
    ForumPostDetailView,
    ForumReplyCreateView,
    ResourceListView
)

urlpatterns = [
    path('reports/', ReportCreateView.as_view(), name='report-create'),
    path('reports/track/<str:case_id>/', ReportStatusView.as_view(), name='report-status'),
    path('reports/chat/<str:case_id>/', ReportChatView.as_view(), name='report-chat'),
    path('dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('forum/', ForumPostListCreateView.as_view(), name='forum-list-create'),
    path('forum/<int:pk>/', ForumPostDetailView.as_view(), name='forum-post-detail'),
    path('forum/<int:post_pk>/reply/', ForumReplyCreateView.as_view(), name='forum-post-reply'),
    path('resources/', ResourceListView.as_view(), name='resource-list'),
]