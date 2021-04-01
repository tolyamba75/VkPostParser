from .models import Task, AccessToken   # Import the model classes we just wrote.
from .vkdo import VkParserPost

from django.db.models import F
from django.conf import settings
from django.utils import timezone

from celery import task

from random import randrange
import vk_api


def filter_post(wall, num_last_post):
    ready_post = []
    num_posts = []

    for post in wall:
        if post['media_id'] > num_last_post:
            num_posts.append(post['media_id'])
            ready_post.append(post)

    try:
        num_last_post = max(num_posts)
    finally:
        return ready_post, num_last_post


def send(module_vk, lst_post, recipient):
    """
    Отправка сообщений

    :param module_vk: модуль вк
    :param lst_post: список постов
    :param recipient: id получателя писем

    """

    for msg in lst_post:
        # в привязке к API_ID и ID отправителя
        # дата поста + id группы поста + id поста ('id user',
        #           которому отправляем или 'id группы заказчика' (позже))
        random_id = str(msg['date']) + \
                    str(((msg['owner_id']) ** 2) ** (1 / 2)) + \
                    str(msg['media_id'])
        module_vk.send_msg(recipient, msg, random_id)


def get_token_user():
    count = randrange(AccessToken.objects.count())
    access_token = AccessToken.objects.all()[count]
    return access_token


@task()
def parser_vk():
    now_time = int(timezone.now().timestamp())   # unix time

    list_tasks = Task.objects.prefetch_related("processing").prefetch_related("receiver")\
        .filter(status=True, last_run__lte=now_time - F('frequency'))

    for t in list_tasks:
        list_group = t.processing.filter(task=t.id, status=True)
        recipient = t.receiver.get(task=t.id).admin_id

        for group in list_group:
            access_token = get_token_user()

            module_vk = VkParserPost(settings.VK_GROUP_TOKEN, access_token.token)
            try:
                wall, num_post = filter_post(module_vk.wall_group(group.group_id),
                                             group.last_post_id)
            except vk_api.exceptions.ApiError as e:
                if e.error['error_code'] == 5:
                    AccessToken.objects.filter(id=access_token.id).delete()
                continue

            else:
                send(module_vk, wall, recipient)

                group.last_run = now_time
                group.last_post_id = num_post
                group.processed_post += len(wall)
                group.launch_num += 1
                group.save()

        t.last_run = now_time
        t.save()
    return 'ok'
