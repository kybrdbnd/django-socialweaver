from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from image_cropping import ImageRatioField
from django.urls import reverse
# Create your models here.


class ProfileModel(models.Model):
    user = models.OneToOneField(User)
    phone_no = models.IntegerField()
    first_name = models.CharField(max_length=100, default='', blank=True)
    last_name = models.CharField(max_length=100, default='', blank=True)
    email = models.EmailField(null=False, default='')
    profile_pic = models.ImageField(upload_to='profile_pics',
                                    default='profile_pics/avatar.jpg',
                                    null=True)
    is_vendor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

    def full_name(self):
        return self.first_name + ' ' + self.last_name


class SubCategoryModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default='')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategoryModel, self).save(*args, **kwargs)


class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default="")
    sub_categories = models.ManyToManyField(SubCategoryModel)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(CategoryModel, self).save(*args, **kwargs)


class CompanyModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100, default="")
    established_at = models.IntegerField(null=True)
    website = models.CharField(max_length=100, default="")
    email = models.EmailField(default="")
    mobile = models.IntegerField(null=True)
    facebook_link = models.CharField(max_length=100, default="")
    twitter_link = models.CharField(max_length=100, default="")
    instagram_link = models.CharField(max_length=100, default="")
    # opening_hours = models.Date
    is_whatsapp = models.BooleanField(default=True)
    registration_no = models.IntegerField(null=True)
    highlights = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(default="")
    owner = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    categories = models.ManyToManyField(CategoryModel, default="")
    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def get_absolute_url(self):
        return reverse('company:company_detail',
                       kwargs={'slug': self.slug})

    def company_categories(self):
        return ",".join([str(c) for c in self.categories.all()])


class ImageModel(models.Model):
    image = models.ImageField(upload_to='photos/%Y/%m/%d', null=True)
    cropping = ImageRatioField('image', '430x360')
    company = models.ForeignKey(CompanyModel, default=None)

    def __str__(self):
        return self.company.name


class PackageModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True)
    price = models.IntegerField()
    is_child = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    is_adult = models.BooleanField(default=False)
    SUBSCRIPTION = 'sub'
    SESSION = 'sess'
    SERVES_TYPE_CHOICES = (
        (SUBSCRIPTION, 'Subscription'),
        (SESSION, 'Session'),
    )
    image = models.ImageField(upload_to='package',
                              default='package/no-image.png')
    serves_type = models.CharField(choices=SERVES_TYPE_CHOICES,
                                   blank=True,
                                   max_length=4)
    is_trial = models.BooleanField(default=False)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    company = models.ForeignKey(CompanyModel)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class EventModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True)
    price = models.IntegerField()
    is_child = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    is_adult = models.BooleanField(default=False)
    SUBSCRIPTION = 'sub'
    SESSION = 'sess'
    SERVES_TYPE_CHOICES = (
        (SUBSCRIPTION, 'Subscription'),
        (SESSION, 'Session'),
    )
    image = models.ImageField(upload_to='package',
                              default='package/no-image.png')
    serves_type = models.CharField(choices=SERVES_TYPE_CHOICES,
                                   blank=True,
                                   max_length=4)
    is_trial = models.BooleanField(default=False)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    company = models.ForeignKey(CompanyModel)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class AnswerModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    answer = models.TextField()
    given_by = models.ForeignKey(User, null=True)

    def __str__(self):
        return self.answer


class QuestionModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    question = models.CharField(max_length=100)
    asked_for = models.ForeignKey(CompanyModel)
    asked_by = models.ForeignKey(User)
    answers = models.ManyToManyField(AnswerModel, blank=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['-created_at']


class ReviewModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='review',
                              default='package/no-image.png')
    given_by = models.ForeignKey(User)
    given_for = models.ForeignKey(CompanyModel)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class ParentModel(models.Model):
    parent = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    categories = models.ManyToManyField(CategoryModel, default="")
    child = models.IntegerField(default='0')

    def __str__(self):
        return self.parent.username
