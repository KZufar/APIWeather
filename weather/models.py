from django.db import models


class APIRequestLog(models.Model):
    remote_addr = models.GenericIPAddressField(
        verbose_name='IP адрес',
        max_length=100,
    )
    request_datetime = models.DateTimeField(
        verbose_name='Дата поступления запроса',
        auto_now_add=True,
    )
    response_datetime = models.DateTimeField(
        verbose_name='Дата получения ответа',
        null=True,
        blank=True,
    )
    path = models.CharField(
        verbose_name='URL адрес',
        max_length=250,
    )
    query_params = models.TextField(
        verbose_name='Параметры запроса',
        null=True,
        blank=True,
    )
    request_method = models.CharField(
        verbose_name='Метод запроса',
        max_length=10,
    )
    response = models.TextField(
        verbose_name='Ответ',
        null=True,
        blank=True,
    )
    status_code = models.IntegerField(
        verbose_name='Код ответа',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'API запрос'
        verbose_name_plural = 'Журнал запросов к API'


class BotUser(models.Model):
    user_id = models.PositiveIntegerField(
        verbose_name='ID пользователя',
        unique=True,
    )
    name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=255,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь (Телеграм бот)'
        verbose_name_plural = 'Пользователи (Телеграм бот)'


class Message(models.Model):
    bot_user = models.ForeignKey(
        to=BotUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        )
    request_msg = models.TextField(
        verbose_name='Сообщение от пользователя',
    )
    response_msg = models.TextField(
        verbose_name='Ответное сообщение',
    )
    created_at = models.DateTimeField(
        verbose_name='Время получения',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Сообщение (Телеграм бот)'
        verbose_name_plural = 'Сообщения (Телеграм бот)'
