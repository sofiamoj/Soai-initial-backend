from django.shortcuts import render, get_object_or_404
from django.views import View
from django.db.models import Prefetch
from .models import Category, Product, Exercise


class CourseView(View):
    def get(self, request):
        categories = Category.objects.filter(
            is_sub=False,
            products__available=True
        ).prefetch_related(
            Prefetch('products', queryset=Product.objects.filter(available=True))
        ).distinct()
        return render(request, 'course/course.html', {'categories': categories})


class ExerciseView(View):
    def get(self, request, pk):
        exercise = get_object_or_404(Exercise, pk=pk, is_active=True)
        # تمرین قبلی و بعدی
        prev_exercise = Exercise.objects.filter(
            product=exercise.product,
            order__lt=exercise.order,
            is_active=True
        ).order_by('-order').first()

        next_exercise = Exercise.objects.filter(
            product=exercise.product,
            order__gt=exercise.order,
            is_active=True
        ).order_by('order').first()

        return render(request, 'course/exercise.html', {
            'exercise': exercise,
            'prev_exercise': prev_exercise,
            'next_exercise': next_exercise,
        })
