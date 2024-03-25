from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

User = get_user_model()


class Book(models.Model):
    title = models.CharField(
        'Название',
        max_length=30
    )
    year = models.PositiveSmallIntegerField(
        'Год издания',
        validators=[
            MinValueValidator(10),
            MaxValueValidator(2024)],
    )
    author = models.CharField(
        'Автор',
        max_length=30
    )
    is_taken = models.BooleanField(
        default=False,
        verbose_name='Взята'
    )

    class Meta:
        verbose_name_plural = 'Книги'
        verbose_name = 'книга'

    def __str__(self):
        return self.title


class Status(models.Model):
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        related_name='status',
        verbose_name='Книга'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='books_taken',
        verbose_name='Пользователь'
    )
    taken_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата взятия'
    )
    returned_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата возврата'
    )

    class Meta:
        verbose_name_plural = 'Статусы'
        verbose_name = 'статус'

    def __str__(self):
        status = 'Взята' if (self.taken_at
                             and not self.returned_at) else 'Доступна'
        return f'{self.book.title} - {status}'


class HistoryMove(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name='Название книги'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь, взявший книгу'
    )
    action = models.CharField(
        max_length=50,
        verbose_name='Действие'
    )
    action_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата действия'
    )

    class Meta:
        verbose_name_plural = 'Истории передач'
        verbose_name = 'история передачи'

    def __str__(self):
        return f"{self.book.title} - {self.action} - {self.action_date}"


@receiver(post_save, sender=Status)
def update_book_status(sender, instance, **kwargs):
    book = instance.book
    book.is_taken = True if (instance.taken_at
                             and not instance.returned_at) else False
    book.save(update_fields=['is_taken'])
    action = 'Взята' if (instance.taken_at
                         and not instance.returned_at) else 'Возвращена'
    HistoryMove.objects.create(
        book=book,
        user=instance.user,
        action=action
    )


@receiver(pre_delete, sender=Status)
def handle_book_return(sender, instance, **kwargs):
    book = instance.book
    book.is_taken = False
    book.save(update_fields=['is_taken'])
    HistoryMove.objects.create(
        book=book,
        user=instance.user,
        action='Возвращена'
    )
