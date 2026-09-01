from django.contrib import admin
from .models import Category, Product, Exercise


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_sub', 'sub_category')
    list_filter = ('is_sub',)
    prepopulated_fields = {'slug': ('name',)}


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1
    fields = ('title', 'order', 'is_active')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'created')
    list_editable = ('price', 'available')
    list_filter = ('available', 'category')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('category',)
    inlines = [ExerciseInline]  # ✅ تمرین‌ها زیر هر دوره


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('product', 'is_active')
    fieldsets = (
        ('Basic Info', {'fields': ('product', 'title', 'description', 'order', 'is_active')}),
        ('Code', {'fields': ('starter_code', 'solution_code', 'expected_output')}),
        ('Help', {'fields': ('hint',)}),
    )
