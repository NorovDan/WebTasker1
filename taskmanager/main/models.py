from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField("Название", max_length=60)
    task = models.TextField("Описание",max_length=130)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name ="Задача"
        verbose_name_plural = "Задачи"

