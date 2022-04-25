from django.urls import path

from .views import *

urlpatterns = [
    path('api/post/', PostView.as_view()),
    path('api/post/<int:post_id>/', PostReadUpdateDeleteView.as_view()),
    path('api/comment/', CommentCreateView.as_view()),
    path('api/comment/<int:comment_id>/', CommentReadUpdateDeleteView.as_view()),
    path('api/comment_all/<int:comment_id>/', CommentReadAllReplyView.as_view()),

]