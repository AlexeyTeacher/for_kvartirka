import json

from django.http import JsonResponse, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .serializers import post_serializer


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
        print(request)
        try:
            post_body = json.loads(request.body)
            if request.user.is_authenticated:
                post_data = {
                    'content': post_body.get('content'),
                    'author': post_body.get('username')
                }
            else:
                post_data = {
                    'content': post_body.get('content'),
                    'author': None
                }
            post_obj = Post.objects.create(**post_data)
            data = {
                'message': f'Добавлена новая статья под номером: {post_obj.pk}'
            }
            status = 201
        except Exception as ex:
            data = {
                'message': f'Произошла ошибка. Статья НЕ добавлена!',
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
                'message': f'Произошла ошибка. Статья под номером: {post_id} НЕ изменена',
                'Error': str(ex)
            }
            status = 500
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, status=status)


