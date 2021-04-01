import vk_api
import json


class VkParserPost:
    """
    Работа с ВК

    :param token: ключ группы
    :type token: str

    :param access_token: ключ пользователя
    :type access_token: str
    """

    def __init__(self, token, access_token):
        vk_session_group = vk_api.VkApi(token=token)
        self.vk_group = vk_session_group.get_api()
        vk_session = vk_api.VkApi(token=access_token)
        self.vk = vk_session.get_api()
        self.keyboard = {"inline": True,
                         "buttons": [
                             [
                                 {
                                     "action": {
                                         "type": "open_link",
                                         "link": "http://example.com/",
                                         "label": "Разместить запись"
                                     }
                                 }
                             ]
                         ]
                         }

    def wall_group(self, group_id, num=50):
        """
        "Прогулка" по стене

        :param group_id: положительное id группы
        :param num: количество просматриваемых постов(max=100)

        :return: [{date, owner_id, media_id}]
        """

        resp = self.vk.wall.get(owner_id=-group_id, count=num, filter='owner')['items']

        now_post = []

        for post in resp:
            dct = {'date': post['date'],
                   'owner_id': post['owner_id'],
                   'media_id': post['id']}
            now_post.append(dct)

        return now_post

    def send_msg(self, user_id, now_post, rnd_num):
        """
        Отправка сообщения с кнопкой

        :param user_id: id пользователя, которому отпраляем

        :param now_post: пост
        :type now_post: dict

        :param rnd_num: число сообщения

        :return: число сообщения
        """

        return self.vk_group.messages.send(user_id=user_id, random_id=rnd_num, peer_id=user_id,
                                           attachment='wall{owner_id}_{media_id}'.format(owner_id=now_post['owner_id'],
                                                                                         media_id=now_post['media_id']),
                                           keyboard=json.dumps(self.keyboard))
