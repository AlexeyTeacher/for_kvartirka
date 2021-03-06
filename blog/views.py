import json

from django.http import JsonResponse, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .serializers import post_serializer, comment_serializer, comment_all_reply_serializer


@method_decorator(csrf_exempt, name='dispatch')
class PostView(View):
    def get(self, request):
        post_count = Post.objects.count()
        posts = Post.objects.all()
        posts_serializer_data = []
        for post in posts:
            posts_serializer_data.append(post_serializer(post))

        data = {
            'posts': posts_serializer_data,
            'count': post_count
        }
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        try:
            post_body = json.loads(request.body)
            post_data = {
                'content': post_body.get('content'),
            }
            if request.user.is_authenticated:
                post_data['author'] = post_body.get('username')
            post_obj = Post.objects.create(**post_data)
            data = {
                'message': f'Добавлена новая статья под номером: {post_obj.pk}'
            }
            status = 201
        except Exception as ex:
            data = {
                'message': f'Произошла ошибка. Статья не добавлена!',
                'Error': str(ex)
            }
            status = 500
        return JsonResponse(data, status=status, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class PostReadUpdateDeleteView(View):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            return JsonResponse(post_serializer(post), json_dumps_params={'ensure_ascii': False})
        except:
            return HttpResponseNotFound('Страница не найдена')

    def put(self, request, post_id):
        put_body = json.loads(request.body)
        try:
            post = Post.objects.get(pk=post_id)
            post.content = put_body.get('content')
            post.save()
            data = {
                'message': f'Статья под номером: {post_id} успешно изменена',
                'post': post_serializer(post)
            }
            status = 201
        except Exception as ex:
            data = {
                'message': f'Произошла ошибка. Статья под номером: {post_id} НЕ изменена',
                'Error': str(ex)
            }
            status = 500
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, status=status)

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            post.delete()
            data = {
                'message': f'Статья под номером: {post_id} успешно удалена',
            }
            status = 200
        except Exception as ex:
            data = {
                'message': f'Произошла ошибка. Статья под номером: {post_id} не изменена',
                'Error': str(ex)
            }
            status = 500
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, status=status)


@method_decorator(csrf_exempt, name='dispatch')
class CommentCreateView(View):
    def post(self, request):
        try:
            comment_body = json.loads(request.body)
            comment_data = {
                'text': comment_body.get('text'),
            }
            if request.user.is_authenticated:
                comment_data["author"] = comment_body.get('username')
            if 'reply' in comment_body:
                comment_data['reply_id'] = comment_body.get('reply')
            if 'post' in comment_body:
                comment_data['post_id'] = comment_body.get('post')
            comment_obj = Comment.objects.create(**comment_data)
            data = {
                'message': f'Добавлен новый комментарий(id{comment_obj.pk}) к статье № {comment_obj.post.pk}.'
            }
            status = 201
        except Exception as ex:
            data = {
                'message': f'Произошла ошибка. Комментарий не добавлен!',
                'Error': str(ex)
            }
            status = 500
        return JsonResponse(data, status=status, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class CommentReadUpdateDeleteView(View):
    def get(self, request, comment_id):
        try:
            return JsonResponse(comment_serializer(comment_id), json_dumps_params={'ensure_ascii': False})
        except Exception as ex:
            return HttpResponseNotFound(f'Страница не найдена')

    def put(self, request, comment_id):
        put_body = json.loads(request.body)
        try:
            comment = Comment.objects.get(pk=comment_id)
            comment.text = put_body.get('text')
            if request.user.is_authenticated:
                comment.author = put_body.get('username')
            if 'reply' in put_body:
                comment.reply_id = put_body.get('reply')
            comment.save()
            data = {
                'message': f'Комментарий id{comment_id} успешно изменен',
                'post': comment_serializer(comment_id)
            }
            status = 201
        except Exception as ex:
            data = {
                'message': f'Произошла ошибка. Комментарий id{comment_id} не изменен!',
                'Error': str(ex)
            }
            status = 500
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, status=status)

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
            comment.delete()
            data = {
                'message': f'Комментарий id{comment_id} успешно удален',
            }
            status = 200
        except Exception as ex:
            data = {
                'message': f'Произошла ошибка. Комментарий id{comment_id} не получилось удалить!',
                'Error': str(ex)
            }
            status = 500
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, status=status)


@method_decorator(csrf_exempt, name='dispatch')
class CommentReadAllReplyView(View):
    def get(self, request, comment_id):
        try:
            return JsonResponse(comment_all_reply_serializer(comment_id), json_dumps_params={'ensure_ascii': False})
        except Exception as ex:
            return HttpResponseNotFound(f'Страница не найдена')