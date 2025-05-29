from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver


User = get_user_model()


class Property(models.Model):
    PROPERTY_TYPES = (
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('office', 'Офис'),
        ('land', 'Земля'),
    )

    title = models.CharField('Название', max_length=255)
    property_type = models.CharField('Тип недвижимости', max_length=50, choices=PROPERTY_TYPES)
    address = models.TextField('Адрес')
    price = models.DecimalField('Цена', max_digits=12, decimal_places=2)
    area = models.FloatField('Площадь м²')
    description = models.TextField('Описание', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    is_available = models.BooleanField('Доступен для продажи', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ✅ Новое поле: агент, ответственный за этот объект
    agent = models.ForeignKey(
        'Agent',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_properties'
    )

    def __str__(self):
        return self.title


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField('Телефон', max_length=17)
    passport = models.CharField('Паспорт', max_length=20)
    address = models.TextField('Адрес регистрации')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Buyer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='buyer_profile'
    )
    phone = models.CharField('Телефон', max_length=17)
    budget = models.DecimalField('Бюджет', max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.user.email


class Agent(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='agent_profile'
    )
    phone = models.CharField('Телефон', max_length=17)
    department = models.CharField('Отдел', max_length=100)
    experience_years = models.PositiveIntegerField('Стаж, лет')
    bio = models.TextField('Описание', blank=True, null=True)
    is_active = models.BooleanField('Активный', default=True)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Sale(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True, blank=True)
    sale_date = models.DateField(auto_now_add=True)
    contract_number = models.CharField(max_length=100, unique=True)
    price_with_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    agent = models.ForeignKey(
        'Agent',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    def __str__(self):
        buyer_info = f"{self.buyer.user.full_name}" if self.buyer and hasattr(self.buyer, 'user') else "Без покупателя"
        return f"{self.property.title} → {buyer_info}"
    

class CompanyInfo(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    description = models.TextField('Описание')
    logo = models.ImageField('Логотип', upload_to='company/', null=True, blank=True)
    video_url = models.URLField('Видео', blank=True, null=True)
    history = models.TextField('История по годам', blank=True, null=True)
    address = models.TextField('Адрес', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    email = models.EmailField('Email', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Инфо о компании'
        verbose_name_plural = 'Инфо о компании'


class FAQ(models.Model):
    question = models.CharField('Вопрос', max_length=255)
    answer = models.TextField('Ответ')
    added_at = models.DateTimeField('Дата добавления', default=timezone.now)
    
    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Часто задаваемые вопросы'
        ordering = ['-added_at']


@receiver(post_delete, sender=User)
def handle_user_deletion(sender, instance, **kwargs):
    # Можно просто помечать сделки как "без покупателя", а не удалять
    from .models import Sale
    Sale.objects.filter(buyer__user=instance).update(buyer=None)


class Vacancy(models.Model):
    title = models.CharField('Название вакансии', max_length=255)
    description = models.TextField('Описание')
    salary = models.DecimalField('Зарплата', max_digits=10, decimal_places=2, blank=True, null=True)
    published_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-published_at']



class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_reviews'
    )
    rating = models.PositiveSmallIntegerField('Оценка', default=5)
    text = models.TextField('Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.user.email} ({self.rating}/5)"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']


class PromoCode(models.Model):
    code = models.CharField('Промокод', max_length=50, unique=True)
    discount_percent = models.DecimalField('Процент скидки', max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField('Действует с', null=True, blank=True)
    valid_to = models.DateTimeField('Действует до', null=True, blank=True)
    uses = models.PositiveIntegerField('Максимальное число использований', default=1)
    used_count = models.PositiveIntegerField('Число использований', default=0)
    is_active = models.BooleanField('Активен', default=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)" 

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def can_use(self):
        from django.utils import timezone

        now = timezone.now()
        if not self.is_active:
            return False
        if self.valid_from and now < self.valid_from:
            return False
        if self.valid_to and now > self.valid_to:
            return False
        if self.used_count >= self.uses and self.uses > 0:
            return False
        return True