# -*- coding: utf-8 -*-
from django.db import models



class NewsItem(models.Model):

    TYPE_CHOICES = (
        ("news", "Новости"),
        ("announce", "Анонс"),
        ("other", "Прочее"),
    )

    title = models.CharField(verbose_name=u"Заголовок", max_length=300, null=False, blank=False)
    intro = models.TextField(verbose_name=u"Вводная часть", help_text=u"Демонстрируется на Главной странице",
                             null=False, blank=False)
    body = models.TextField(verbose_name=u"Тело статьи",
                            null=False, blank=False)
    pub_date = models.DateField(verbose_name=u"Дата публикации", auto_now_add=True)
    type = models.CharField(verbose_name=u"Вид статьи", help_text=u"Определяет в какую вкладку на Главной попадет новость",
                            max_length=8, null=False, blank=False, choices=TYPE_CHOICES, default="other")
    published = models.BooleanField(verbose_name=u"Публиковать", default=False)

    class Meta:
        verbose_name = u"Новостная статья"
        verbose_name_plural = u"Новостные статьи"

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.pub_date)
    
