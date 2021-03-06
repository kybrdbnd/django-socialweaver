from django.conf.urls import url
from .views import (home, dashboard, landing_step, package, event,
                    company_profile, calendar, profile_pic, company_detail,
                    question_detail, review_create, wishlist_create,
                    review_like, package_edit, event_edit, review_detail)

urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'landing_step/', landing_step, name="landing_steps"),
    url(r'^dashboard/', dashboard, name="dashboard"),
    url(r'^package/edit/(?P<id>\d+)$', package_edit, name="package_edit"),
    url(r'^package/', package, name="package"),
    url(r'^event/edit/(?P<id>\d+)$', event_edit, name="event_edit"),
    url(r'^event/', event, name="event"),
    url(r'^profile/', company_profile, name="company_profile"),
    url(r'^calendar/', calendar, name="calendar"),
    url(r'^profile_pic/', profile_pic),
    url(r'^question/', question_detail, name="question"),
    url(r'^review/', review_create, name='review_create'),
    url(r'^wishlist/', wishlist_create, name='wishlist_create'),
    url(r'^reviews/', review_detail, name='review'),
    url(r'^review_like/', review_like, name='review_like'),
    url(r'^(?P<slug>[-\w]+)/$', company_detail, name='company_detail'),
]
