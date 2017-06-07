from django import forms
from django.forms import FileInput, Textarea
from .models import (ProfileModel, CategoryModel,
                     CompanyModel, ImageModel, PackageModel, EventModel,
                     ParentModel, QuestionModel, ReviewModel)
import re


class UserForm(forms.ModelForm):
    user_type = forms.BooleanField(required=False)

    class Meta:
        model = ProfileModel
        fields = ('first_name', 'last_name', 'email', 'phone_no',)

    def signup(self, request, user):
        profile = ProfileModel()
        profile.user = user
        profile.first_name = self.cleaned_data['first_name']
        profile.last_name = self.cleaned_data['last_name']
        profile.email = self.cleaned_data['email']
        profile.phone_no = self.cleaned_data['phone_no']
        is_vendor = self.cleaned_data['user_type']
        if is_vendor:
            profile.is_vendor = is_vendor
        profile.save()

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        pattern_name = re.compile("^[a-zA-Z]*$")

        if not pattern_name.match(first_name):
            msg = "Only Characters are required"
            self.add_error('first_name', msg)
        if not pattern_name.match(last_name):
            msg = "Only Characters are required"
            self.add_error('last_name', msg)


class PackageForm(forms.ModelForm):
    class Meta:
        model = PackageModel
        fields = ('name', 'description', 'price', 'serves_type',
                  'is_child', 'is_parent', 'is_adult', 'image')
    SUBSCRIPTION = 'sub'
    SESSION = 'sess'
    SERVES_TYPE_CHOICES = (
        (SUBSCRIPTION, 'Subscription'),
        (SESSION, 'Session'),
    )
    serves_type = forms.ChoiceField(choices=SERVES_TYPE_CHOICES,
                                    widget=forms.RadioSelect())


class EventForm(forms.ModelForm):
    class Meta:
        model = EventModel
        fields = ('name', 'description', 'price', 'serves_type',
                  'is_child', 'is_parent', 'is_adult', 'image')
    SUBSCRIPTION = 'sub'
    SESSION = 'sess'
    SERVES_TYPE_CHOICES = (
        (SUBSCRIPTION, 'Subscription'),
        (SESSION, 'Session'),
    )
    serves_type = forms.ChoiceField(choices=SERVES_TYPE_CHOICES,
                                    widget=forms.RadioSelect())


class CompanyForm(forms.ModelForm):
    name = forms.CharField(label="Name of the Company",
                           max_length=100, required=True)
    address = forms.CharField(label="Address of the Company:",
                              max_length=100)
    website = forms.CharField(label="Website of the Company", max_length=100)
    email = forms.EmailField(label="Email ID of the Company")
    categories = forms.ModelMultipleChoiceField(label="Categories",
                                                queryset=CategoryModel.objects.all())

    class Meta:
        model = CompanyModel
        fields = ('name', 'address', 'website', 'email')


class CompanyUpdateForm(forms.ModelForm):

    class Meta:
        model = CompanyModel
        fields = ('name', 'address', 'description', 'established_at',
                  'website', 'mobile', 'is_whatsapp', 'registration_no',
                  'email')

    def clean(self):
        cleaned_data = super(CompanyUpdateForm, self).clean()
        name = cleaned_data.get("name")
        mobile = cleaned_data.get('mobile')
        pattern_name = re.compile("^[a-zA-Z]*$")

        if not pattern_name.match(name):
            msg = "Only Characters are required"
            self.add_error('name', msg)

        if not len(str(mobile)) == 10:
            msg = "Only 10 digits Allowed"
            self.add_error('mobile', msg)


class CompanyImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ('image',)
        widgets = {
            'image': FileInput(attrs={'multiple': True,
                                      'onchange': 'Imagethumb(this)'}),
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = ProfileModel
        fields = ('first_name', 'last_name', 'phone_no', 'profile_pic')
        widgets = {
            'profile_pic': FileInput()
        }


class CompanyHighlightForm(forms.ModelForm):
    class Meta:
        model = CompanyModel
        fields = ('highlights',)


class CompanySocialForm(forms.ModelForm):
    class Meta:
        model = CompanyModel
        fields = ('facebook_link', 'twitter_link', 'instagram_link')


class GoogleCalendarEventForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    organiser = forms.CharField(max_length=100)
    start_date = forms.DateField(
        widget=forms.DateInput(attrs=({'class': 'datepicker'})))
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs=({'class': 'timepicker'})))
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs=({'class': 'timepicker'})))


class CustomerLandingForm(forms.ModelForm):
    username = forms.CharField(label="Enter Username", max_length=100)
    child = forms.IntegerField(label="Enter No.Of Children")
    categories = forms.ModelMultipleChoiceField(label="Categories",
                                                queryset=CategoryModel.objects.all())

    class Meta:
        model = ParentModel
        fields = ('child',)


class QuestionForm(forms.ModelForm):
    company_pk = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = QuestionModel
        fields = ('question',)


class AnswerForm(forms.Form):
    answer = forms.CharField(max_length=100, label="Enter Your Answer")
    question_id = forms.CharField(widget=forms.HiddenInput())


class ReviewForm(forms.ModelForm):
    company_id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = ReviewModel
        fields = ('title', 'content', 'image')
        widgets = {
            'content': Textarea(attrs={'class': 'materialize-textarea'})
        }
