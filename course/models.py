from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='category', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:category_filter', args=[self.slug,])


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/images/')
    video = models.FileField(upload_to='products/videos/', validators=[FileExtensionValidator(allowed_extensions=['mp4'])], null=True, blank=True)
    rar_file = models.FileField(upload_to='products/rar/', validators=[FileExtensionValidator(allowed_extensions=['rar'])], null=True, blank=True)
    description = models.TextField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course:course_detail', args=[self.slug,])


# ✅ Exercise model - جدید
class Exercise(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=200)
    description = models.TextField(help_text='Explain the exercise. HTML is supported.')
    starter_code = models.TextField(default='# Write your code here\n', help_text='Initial code shown to user')
    solution_code = models.TextField(help_text='Correct solution (only visible in admin)')
    expected_output = models.TextField(help_text='Expected output to verify the solution')
    hint = models.TextField(blank=True, help_text='Optional hint for the user')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Exercise'
        verbose_name_plural = 'Exercises'

    def __str__(self):
        return f'{self.product.name} — {self.title}'

    def get_absolute_url(self):
        return reverse('course:exercise', args=[self.pk])
