from .models import Comment


def post_serializer(post):
    if Comment.objects.filter(post=post.pk).order_by('pk'):
        comment_serializer_data = []

        for comment in Comment.objects.filter(post=post.pk, reply=None).order_by('pk'):
            comment_serializer_data.append(comment_serializer(comment.pk))

        return {
            'id': post.pk,
            'content': post.content,
            'author': str(post.author),
            'comments': comment_serializer_data
        }
    else:
        return {
            'id': post.pk,
            'content': post.content,
            'author': str(post.author),
        }


def comment_serializer(comment_id):
    comment = Comment.objects.get(pk=comment_id)
    reply_serializer_level_2 = []

    for level_2 in Comment.objects.filter(reply=comment.pk).order_by('pk'):
        reply_serializer_level_3 = []

        for level_3 in Comment.objects.filter(reply=level_2.pk).order_by('pk'):
            reply_serializer_level_3.append({
                'id': level_3.pk,
                'post': level_3.post.pk,
                'text': level_3.text,
                'author': str(level_3.author),
            })

        reply_serializer_level_2_data = {
            'id': level_2.pk,
            'post': level_2.post.pk,
            'text': level_2.text,
            'author': str(level_2.author),
        }

        if reply_serializer_level_3:
            reply_serializer_level_2_data['reply'] = reply_serializer_level_3

        reply_serializer_level_2.append(reply_serializer_level_2_data)

    comment_serializer_data = {
        'id': comment.pk,
        'post': comment.post.pk,
        'text': comment.text,
        'author': str(comment.author),
    }
    if reply_serializer_level_2:
        comment_serializer_data['reply'] = reply_serializer_level_2

    return comment_serializer_data


def comment_all_reply_serializer(comment_id):
    comment = Comment.objects.get(pk=comment_id)
    reply_serializer_level_2 = []
    for level_2 in Comment.objects.filter(reply=comment.pk).order_by('pk'):
        reply_serializer_level_3 = []
        for level_3 in Comment.objects.filter(reply=level_2.pk).order_by('pk'):
            if level_3.reply:
                reply_serializer_level_3.append(comment_all_reply_serializer(level_3.pk))
            else:
                reply_serializer_level_3.append({
                    'id': level_3.pk,
                    'post': level_3.post.pk,
                    'text': level_3.text,
                    'author': str(level_3.author),
                })
        reply_serializer_level_2_data = {
                'id': level_2.pk,
                'post': level_2.post.pk,
                'text': level_2.text,
                'author': str(level_2.author),
            }
        if reply_serializer_level_3:
            reply_serializer_level_2_data['reply'] = reply_serializer_level_3
        reply_serializer_level_2.append(reply_serializer_level_2_data)

    comment_serializer_data = {
        'id': comment.pk,
        'post': comment.post.pk,
        'text': comment.text,
        'author': str(comment.author),
    }
    if reply_serializer_level_2:
        comment_serializer_data['reply'] = reply_serializer_level_2

    return comment_serializer_data

