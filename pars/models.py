from django.db import models


class AccessToken(models.Model):
    """
    Таблица ключей пользователей
    """
    objects = None

    token = models.CharField('Токен пользователя', max_length=100)


class Task(models.Model):
    """
    Таблица задач
    """

    objects = None

    name = models.CharField(verbose_name='Имя задачи', max_length=100)
    group_id = models.PositiveIntegerField('Группа владельца')
    status = models.BooleanField('Статус задачи', default=False)

    frequency = models.PositiveIntegerField('Частота запуска', default=60)
    last_run = models.PositiveIntegerField('Последний запуск', default=0)

    def __str__(self):
        return str(self.name)


class ProcessingGroup(models.Model):
    """
    Таблица обработки постов
    """

    objects = None

    task = models.ForeignKey(Task, verbose_name='Задача', on_delete=models.CASCADE, related_name='processing')

    group_id = models.PositiveIntegerField('Группа для задачи')
    status = models.BooleanField('Статус задачи', default=False)

    launch_num = models.PositiveIntegerField('Количество выполнений', default=0)
    processed_post = models.PositiveIntegerField('Количество обработанных постов', default=0)
    last_post_id = models.PositiveIntegerField('Последний пост', default=0)

    class Meta:
        unique_together = [["group_id", "task"]]

    def __str__(self):
        return str(self.task) + " " + str(self.group_id)


class Recipient(models.Model):
    """
    Таблица получателя постов
    """

    objects = None

    admin_id = models.PositiveIntegerField("Получатель")
    task = models.ForeignKey(Task, verbose_name='Задача', on_delete=models.CASCADE, related_name='receiver')

    class Meta:
        unique_together = [["admin_id", "task"]]

    def __str__(self):
        return str(self.task)
