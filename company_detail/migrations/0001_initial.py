# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 04:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import image_cropping.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answer', models.TextField()),
                ('given_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(default='', max_length=100)),
                ('established_at', models.IntegerField(null=True)),
                ('website', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(default='', max_length=254)),
                ('mobile', models.IntegerField(null=True)),
                ('facebook_link', models.CharField(default='', max_length=100)),
                ('twitter_link', models.CharField(default='', max_length=100)),
                ('instagram_link', models.CharField(default='', max_length=100)),
                ('is_whatsapp', models.BooleanField(default=True)),
                ('registration_no', models.IntegerField(null=True)),
                ('highlights', models.CharField(default='', max_length=100)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('slug', models.SlugField(default='')),
                ('categories', models.ManyToManyField(default='', to='company_detail.CategoryModel')),
                ('dislikes', models.ManyToManyField(related_name='dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('owner', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='EventModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('price', models.IntegerField()),
                ('is_child', models.BooleanField(default=False)),
                ('is_parent', models.BooleanField(default=False)),
                ('is_adult', models.BooleanField(default=False)),
                ('image', models.ImageField(default='package/no-image.png', upload_to='package')),
                ('serves_type', models.CharField(blank=True, choices=[('sub', 'Subscription'), ('sess', 'Session')], max_length=4)),
                ('is_trial', models.BooleanField(default=False)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company_detail.CompanyModel')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='photos/%Y/%m/%d')),
                ('cropping', image_cropping.fields.ImageRatioField('image', '430x360', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping')),
                ('company', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='company_detail.CompanyModel')),
            ],
        ),
        migrations.CreateModel(
            name='PackageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('price', models.IntegerField()),
                ('is_child', models.BooleanField(default=False)),
                ('is_parent', models.BooleanField(default=False)),
                ('is_adult', models.BooleanField(default=False)),
                ('image', models.ImageField(default='package/no-image.png', upload_to='package')),
                ('serves_type', models.CharField(blank=True, choices=[('sub', 'Subscription'), ('sess', 'Session')], max_length=4)),
                ('is_trial', models.BooleanField(default=False)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company_detail.CompanyModel')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ParentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child', models.IntegerField(default='0')),
                ('categories', models.ManyToManyField(default='', to='company_detail.CategoryModel')),
                ('parent', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.IntegerField()),
                ('first_name', models.CharField(blank=True, default='', max_length=100)),
                ('last_name', models.CharField(blank=True, default='', max_length=100)),
                ('email', models.EmailField(default='', max_length=254)),
                ('profile_pic', models.ImageField(default='profile_pics/avatar.jpg', null=True, upload_to='profile_pics')),
                ('is_vendor', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.CharField(max_length=100)),
                ('answers', models.ManyToManyField(blank=True, to='company_detail.AnswerModel')),
                ('asked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('asked_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company_detail.CompanyModel')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReviewModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('image', models.ImageField(default='package/no-image.png', upload_to='review')),
                ('given_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('given_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company_detail.CompanyModel')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SubCategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(default='')),
            ],
        ),
        migrations.AddField(
            model_name='categorymodel',
            name='sub_categories',
            field=models.ManyToManyField(to='company_detail.SubCategoryModel'),
        ),
    ]
