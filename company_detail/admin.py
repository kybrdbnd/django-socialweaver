from django.contrib import admin
from .models import (CompanyModel, CategoryModel, SubCategoryModel,
                     ProfileModel, PackageModel, WishlistModel,
                     EventModel, ImageModel,
                     QuestionModel, AnswerModel, ReviewModel, ParentModel)
from image_cropping import ImageCroppingMixin
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_no', 'email', 'is_vendor')
    list_display_links = ('full_name',)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'company_categories', 'created_at')
    list_display_links = ('name', 'owner')
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_sub_categories')
    prepopulated_fields = {"slug": ("name",)}

    def get_sub_categories(self, obj):
        return ', '.join([sub_category.name for sub_category in obj.sub_categories.all()])


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'company',
                    'serves_type', 'serves_to')

    def serves_to(self, obj):
        serves_to = []
        if obj.is_child:
            serves_to.append('Child')
        if obj.is_parent:
            serves_to.append('Parent')
        if obj.is_adult:
            serves_to.append('Adult')
        return (', ').join(serves_to)


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'company',
                    'serves_type', 'serves_to')

    def serves_to(self, obj):
        serves_to = []
        if obj.is_child:
            serves_to.append('Child')
        if obj.is_parent:
            serves_to.append('Parent')
        if obj.is_adult:
            serves_to.append('Adult')
        return (', ').join(serves_to)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'given_by',
                    'created_at', 'updated_at')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('get_package', 'get_user', 'created_at')

    def get_package(self, obj):
        return obj.created_for.name

    def get_user(self, obj):
        return obj.created_by.get_full_name()


class ImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('image', 'company')


admin.site.register(ParentModel)
admin.site.register(QuestionModel)
admin.site.register(AnswerModel, AnswerAdmin)
admin.site.register(ReviewModel, ReviewAdmin)
admin.site.register(ProfileModel, ProfileAdmin)
admin.site.register(CompanyModel, CompanyAdmin)
admin.site.register(SubCategoryModel, SubCategoryAdmin)
admin.site.register(CategoryModel, CategoryAdmin)
admin.site.register(PackageModel, PackageAdmin)
admin.site.register(WishlistModel, WishlistAdmin)
admin.site.register(EventModel, EventAdmin)
admin.site.register(ImageModel, ImageAdmin)
