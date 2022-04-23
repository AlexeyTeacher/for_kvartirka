from .models import Comment


def post_serializer(post):
    if Comment.objects.filter(post=post.pk):
        comment_serializer_data = []

        for comment in Comment.objects.filter(post=post.pk, reply=None):
            reply_serializer_level_2 = []

            for level_2 in Comment.objects.filter(reply=comment.pk):
                reply_serializer_level_3 = []
                for level_3 in Comment.objects.filter(reply=level_2.pk):
                    reply_serializer_level_3.append({
                        'text': level_3.text,
                        'author': str(level_3.author),
                    })

                if reply_serializer_level_3:
                    reply_serializer_level_2.append({
                        'text': level_2.text,
                        'author': str(level_2.author),
                        'reply': reply_serializer_level_3,
                    })
                else:
                    reply_serializer_level_2.append({
                        'text': level_2.text,
                        'author': str(level_2.author),
                    })

            comment_serializer = {
                'text': comment.text,
                'author': str(comment.author),
                'reply': reply_serializer_level_2
            }

            comment_serializer_data.append(comment_serializer)

        return {
            'content': post.content,
            'author': str(post.author),
            'comments': comment_serializer_data
        }
    else:
        return {
            'content': post.content,
            'author': str(post.author),
        }