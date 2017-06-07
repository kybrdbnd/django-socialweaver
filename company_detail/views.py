from django.shortcuts import render, redirect, get_object_or_404
from .models import (ProfileModel, CompanyModel, CategoryModel,
                     PackageModel, WishlistModel, EventModel, ImageModel, ParentModel,
                     QuestionModel, AnswerModel, ReviewModel)
from .forms import (CompanyForm, CompanyUpdateForm, CompanySocialForm,
                    CompanyImageForm, ProfileForm, CompanyHighlightForm,
                    PackageForm, EventForm, GoogleCalendarEventForm,
                    CustomerLandingForm, QuestionForm, AnswerForm, ReviewForm)
from django.contrib.auth.models import User
from django.contrib import messages
from slugify import slugify
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse


def home(request):
    singapore_best_companies = []
    showcase_companies = CompanyModel.objects.all()[:4]
    upcoming_events = []
    context = {
        'showcase_companies': showcase_companies,
        'singapore_best_companies': singapore_best_companies,
        'upcoming_events': upcoming_events
    }
    return render(request, 'home.html', context)


def landing_step(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = CompanyModel()
            company.name = form.cleaned_data['name']
            company.address = form.cleaned_data['address']
            company.website = form.cleaned_data['website']
            company.email = form.cleaned_data['email']
            categories = form.cleaned_data['categories']
            company.owner = User.objects.get(id=request.user.id)
            company.slug = slugify(company.name)
            company.save()
            for category in categories:
                category = CategoryModel.objects.get(name=category)
                company.categories.add(category)
            messages.success(request, 'Welcome {0}!!!'.format(company.owner))
        return redirect('/company/dashboard')
    else:
        form = CompanyForm()
    return render(request, 'landing_steps.html', {'form': form})


def dashboard(request):
    context = {}
    owner = User.objects.get(id=request.user.id)
    current_user = ProfileModel.objects.get(user=owner)
    if current_user.is_vendor:
        try:
            company = CompanyModel.objects.get(owner=owner)
            context = {
                'company': company
            }
        except CompanyModel.DoesNotExist:
            return redirect('/company/landing_step/')
    else:
        return redirect('/landing_steps/')
    return render(request, 'dashboard.html', context)


def package(request):
    vendor = User.objects.get(id=request.user.id)
    packages = PackageModel.objects.filter(company=vendor.companymodel)
    if request.method == 'POST':
        Packageform = PackageForm(request.POST, request.FILES)
        if Packageform.is_valid():
            instance = Packageform.save(commit=False)
            instance.company = vendor.companymodel
            Packageform.save()
            messages.success(request, 'Package Created Successfully')
            return redirect('/company/package/')
    else:
        Packageform = PackageForm()
    context = {
        'packages': packages,
        'Packageform': Packageform
    }
    return render(request, 'package.html', context)


def package_edit(request, id):
    instance = get_object_or_404(PackageModel, id=id)
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package Updated Successfully')
            return redirect('company:package')
    else:
        form = PackageForm(instance=instance)
    context = {
        'package': instance,
        'form': form
    }
    return render(request, 'package_edit.html', context)


def event(request):
    vendor = User.objects.get(id=request.user.id)
    events = EventModel.objects.filter(company=vendor.companymodel)
    if request.method == 'POST':
        Eventform = EventForm(request.POST, request.FILES)
        if Eventform.is_valid():
            instance = Eventform.save(commit=False)
            instance.company = vendor.companymodel
            Eventform.save()
            messages.success(request, 'Event Created Successfully')
            return redirect('/company/event/')
    else:
        Eventform = EventForm()
    context = {
        'events': events,
        'Eventform': Eventform
    }

    return render(request, 'event.html', context)


def company_profile(request):
    vendor = User.objects.get(id=request.user.id)
    company = CompanyModel.objects.get(owner=vendor)
    profile = ProfileModel.objects.get(user=vendor)
    company_images = ImageModel.objects.filter(company=company)
    if request.method == 'POST':
        CompanyUpdateform = CompanyUpdateForm(request.POST, instance=company)
        CompanySocialform = CompanySocialForm(request.POST, instance=company)
        Profileform = ProfileForm(request.POST, instance=profile
                                  )
        CompanyHighlightform = CompanyHighlightForm(request.POST,
                                                    instance=company)
        CompanyImageform = CompanyImageForm(request.POST, request.FILES)
        if CompanyImageform.is_valid():
            instance = CompanyImageform.save(commit=False)
            instance.company = company
            messages.success(request, 'Business Photos Added')
            CompanyImageform.save()
            return redirect('/company/profile')
        if CompanyHighlightform.is_valid():
            CompanyHighlightform.save()
            messages.success(request, 'Company Highlights Added')
            return redirect('/company/profile/#highlights')
        if CompanySocialform.is_valid():
            CompanySocialform.save()
            messages.success(request, 'Social Links Updated')
            return redirect('/company/profile/#social')
        if CompanyUpdateform.is_valid():
            messages.success(request, 'Profile details updated.')
            CompanyUpdateform.save()
            return redirect('/company/profile')
    else:
        CompanyUpdateform = CompanyUpdateForm(instance=company)
        CompanyImageform = CompanyImageForm()
        Profileform = ProfileForm(instance=profile)
        CompanyHighlightform = CompanyHighlightForm(instance=company)
        CompanySocialform = CompanySocialForm(instance=company)
    context = {
        'CompanyUpdateform': CompanyUpdateform,
        'CompanyImageform': CompanyImageform,
        'company_images': company_images,
        'Profileform': Profileform,
        'CompanyHighlightform': CompanyHighlightform,
        'CompanySocialform': CompanySocialform,
    }
    return render(request, 'company_profile.html', context)


def profile_pic(request):
    vendor = User.objects.get(id=request.user.id)
    profile = ProfileModel.objects.get(user=vendor)
    Profileform = ProfileForm(request.POST,
                              request.FILES,
                              instance=profile
                              )
    if Profileform.is_valid():
        messages.success(request, 'Profile Updated Successfully')
        Profileform.save()
        return redirect('/company/profile#profile')
    return render(request, 'company_profile.html', {})


def calendar(request):
    if request.method == 'POST':
        form = GoogleCalendarEventForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Personal Event Added')
            return redirect('/company/calendar')
    else:
        form = GoogleCalendarEventForm()
    context = {
        'form': form
    }
    return render(request, 'calendar.html', context)


def question_detail(request):
    vendor = User.objects.get(id=request.user.id)
    company = get_object_or_404(CompanyModel, owner=vendor)
    questions = QuestionModel.objects.filter(asked_for=company)
    if request.method == 'POST':
        Answerform = AnswerForm(request.POST)
        if Answerform.is_valid():
            answer = Answerform.cleaned_data.get('answer')
            question_id = Answerform.cleaned_data.get('question_id')
            instance = AnswerModel()
            instance.answer = answer
            instance.given_by = request.user
            instance.save()
            question_instance = QuestionModel.objects.get(id=question_id)
            question_instance.answers.add(instance)
            question_instance.save()
            messages.success(request, "Answer Added Successfully!!!")

    else:
        Answerform = AnswerForm()
    context = {
        'questions': questions,
        'Answerform': Answerform
    }
    return render(request, 'question.html', context)


def customer_landing_step(request):
    user = User.objects.get(id=request.user.id)
    try:
        parent = ParentModel.objects.get(parent=user)
        return redirect('/')
    except ParentModel.DoesNotExist:
        if request.method == 'POST':
            form = CustomerLandingForm(request.POST)
            if form.is_valid():
                categories = form.cleaned_data.get('categories')
                user.username = form.cleaned_data.get('username')
                user.save()
                parent = ParentModel()
                parent.parent = user
                parent.save()
                for category in categories:
                    category = CategoryModel.objects.get(name=category)
                    parent.categories.add(category)
                messages.success(
                    request, "Welcome {0}!!!".format(user.username))
                return redirect('/')
        else:
            form = CustomerLandingForm()
        context = {
            'form': form
        }
    return render(request, 'customer_landing_step.html', context)


def company_detail(request, slug):
    company = get_object_or_404(CompanyModel, slug=slug)
    company_images = ImageModel.objects.filter(company=company)
    packages = PackageModel.objects.filter(company=company)
    question_answers = QuestionModel.objects.filter(asked_for=company)
    reviews = ReviewModel.objects.filter(given_for=company)
    Questionform = QuestionForm()
    Reviewform = ReviewForm()
    context = {
        'company': company,
        'company_images': company_images,
        'packages': packages,
        'question_answers': question_answers,
        'reviews': reviews,
        'Questionform': Questionform,
        'Reviewform': Reviewform

    }
    return render(request, 'company_detail.html', context)


def question_create(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = QuestionForm(request.POST)
            if form.is_valid():
                company_pk = form.cleaned_data.get('company_pk')
                company = CompanyModel.objects.get(pk=company_pk)
                instance = form.save(commit=False)
                instance.asked_for = company
                instance.asked_by = request.user
                messages.success(request, "Question Created Successfully")
                instance.save()
    else:
        messages.info(request, "Login to ask Question")
        return redirect('/accounts/login/')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            company_id = form.cleaned_data.get('company_id')
            company = get_object_or_404(CompanyModel, id=company_id)
            instance = form.save(commit=False)
            instance.given_by = request.user
            instance.given_for = company
            messages.success(request, "Review Created Successfully")
            instance.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


def like(request):
    if request.method == 'POST':
        likes_success = False
        dislikes_success = False
        user_redirect = False
        user = request.user
        company_id = request.POST.get('company_id', None)
        company = get_object_or_404(CompanyModel, id=company_id)
        if user.is_authenticated():
            work = request.POST.get('work')
            if work == 'like':
                if company.likes.filter(id=user.id).exists():
                    company.likes.remove(user)
                else:
                    company.likes.add(user)
                    likes_success = True
                    dislikes_success = False
                    if company.dislikes.filter(id=user.id).exists():
                        company.dislikes.remove(user)
            else:
                if company.dislikes.filter(id=user.id).exists():
                    company.dislikes.remove(user)

                else:
                    company.dislikes.add(user)
                    likes_success = False
                    dislikes_success = True
                    if company.likes.filter(id=user.id).exists():
                        company.likes.remove(user)
        else:
            user_redirect = True
            messages.info(request, "Login to like or dislike")
            # return redirect('/accounts/login/')
    context = {
        'likes_count': company.total_likes(),
        'dislikes_count': company.total_dislikes(),
        'likes_success': likes_success,
        'dislikes_success': dislikes_success,
        'user_redirect': user_redirect
    }
    return HttpResponse(json.dumps(context), content_type='application/json')


def wishlist_create(request):
    user = request.user
    context = {}
    if user.is_authenticated():
        package_id = request.POST.get('package_id', None)
        package = PackageModel.objects.get(id=package_id)
        wishlist_instance = WishlistModel.objects.filter(created_by=user,
                                                         created_for=package)
        if wishlist_instance:
            context['wishlist_removed'] = True
            wishlist_instance.delete()
        else:
            instance = WishlistModel()
            instance.created_for = package
            instance.created_by = user
            instance.save()
            context = {
                'redirect_user': False,
                'wishlist_success': True
            }
    else:
        messages.info(request, "Please Login to Continue!!!")
        context['redirect_user'] = True
    return HttpResponse(json.dumps(context), content_type='application/json')


def review_like(request):
    user = request.user
    context = {}
    if user.is_authenticated():
        review_id = request.POST.get('review_id')
        review = ReviewModel.objects.get(id=review_id)
        if review.likes.filter(id=user.id).exists():
            review.likes.remove(user)
        else:
            context['review_success'] = True
            review.likes.add(user)
    else:
        messages.info(request, "Please Login to Continue!!!")
        context['redirect_user'] = True
    return HttpResponse(json.dumps(context), content_type='application/json')
