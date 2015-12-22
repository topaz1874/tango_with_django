from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>[-\w]+)/$',
        views.category, name='category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^add_page/(?P<category_name_slug>[-\w]+)/$',
        views.add_page, name='add_page'),
    # url(r'^register/$', views.register, name='register'),
    # url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    # url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^search/$', views.search,
        name='search'),
    url(r'^goto/$', views.track_url,
        name='goto'),
    url(r'^add_profile/$', views.register_profile,
        name='add_profile'),
    url(r'^profile/$', views.profile,
        name='profile'),
    url(r'^edit_profile/(?P<id>\d+)/$', views.edit_profile,
        name='edit_profile'),
    url(r'^like_category/$', views.like_category,
        name='like_category'),
    url(r'^suggest_category/$', views.suggest_category,
        name='suggest_category'),
    url(r'^auto_add_page/$', views.auto_add_page,
        name='auto_add_page'),
    url(r'^wiki/$', views.wiki_article_index,
        name='wiki_article_index'),
    url(r'^article/(?P<slug>[-\w]+)/$',views.wiki_article_detail,
        name='wiki_article_detail'),
    url(r'^history/(?P<slug>[-\w]+)/$', views.wiki_article_history,
        name='wiki_article_history'),
    url(r'^add/article$', views.wiki_add_article,
        name='wiki_add_article'),
    url(r'^edit/article(?P<slug>[-\w]+)/$', views.wiki_edit_article,
        name='wiki_edit_article')


)
