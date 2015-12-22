from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from .models import Category, Page, UserProfile, Article, Edit
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm, ArticleForm, EditForm
from .bing_search import requests_query

# def index(request):
# return HttpResponse("Rango says hey there world!")
# construct a dictionary to pass to the template engine as ites context.
# Note the Key blodmessage is the same as {{ blodmessage }} in the template.
#     context_dict = {'boldmessage': 'I am blod font from the context'}

# return a rendered response to send to the client.
# we make use of the shortcut function to make our lives easier.
# Note that the first parameter is the template we wish to use.
#     return render(request, 'rango/index.html', context_dict)


def index_with_client_side_cookies(request):
    # Query the database for a list of all categories currently stored.
    # Order the cateogries by no. like in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to
    # the template engine.
    page_list = Page.objects.order_by('-views')[:5]
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list,
                    'pages': page_list}

    # get the number of visits to the site.
    # we use the COOKIES.get() func to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, we default to zero and cast that.
    visits = int(request.COOKIES.get('visits', '1'))
    reset_last_visit_time = False
    response = render(request, 'rango/index.html', context_dict)
    # Does the cookie last_vist exists?
    if 'last_vist' in request.COOKIES:
        # yes it does, get the cookie's value
        last_vist = request.COOKIES.get('last_vist')
        # cast the value to a python date/time object
        last_vist_time = datetime.strptime(last_vist[:-7], "%Y-%m-%d %H:%M:%S")

        # If it's been more than a day since the last vist...
        if (datetime.now() - last_vist_time).days > 0:
            visits += 1
            # ... and flag that the cookie last visit needs to be updated
            reset_last_visit_time = True
    else:
        # Cookie last_vist doesn't exist, so flag that itshould be set.
        reset_last_visit_time = True
        context_dict['visits'] = visits
        response = render(request, 'rango/index.html', context_dict)

    if reset_last_visit_time:
        response.set_cookie('last_vist', datetime.now())
        response.set_cookie('visits', visits)
    return response


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list,
                    'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_vist_time = datetime.strptime(
            last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_vist_time).days > 0:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context_dict['visits'] = visits

    return render(request, 'rango/index.html', context_dict)


def about(request):
    # return HttpResponse("Rango says here is the about page.")
    count = request.session.get('visits')
    if not count:
        count = 0

    return render(request, 'rango/about.html', {'visits': count})


def category(request, category_name_slug):

    context_dict = {}

    try:
        # can we find a category name slug with the given name?
        # if we can't, the .get() method raises a DoesNotExist exception.
        # so the .get() method returns one model instance or raises an
        # exception.
        category = Category.objects.get(slug=category_name_slug)
        category.views += 1
        category.save()
        context_dict['category_name'] = category.name
        context_dict['views'] = category.views
        # retrieve all of the associated pages.
        # note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category).order_by('-views')

        # add our results list ot the template context under name pages
        context_dict['pages'] = pages
        # we also add the category object from the database to the context dic.
        # we'll use this in the template to veryfy that the category exists.
        context_dict['category'] = category

        context_dict['category_name_slug'] = category_name_slug

    except Category.DoesNotExist:
        # we get here if we didn't finde the special category.
        # Don't do anything - the template displays the "no category" message
        # for us.
        pass

    result_list = []
    if request.method == 'POST':
        query = request.POST.get('query', False)
        if query:
            result_list = requests_query(query.strip())
    context_dict['result_list'] = result_list

    return render(request, "rango/category.html", context_dict)


@login_required
def add_category(request):
    if request.method == 'POST':
        # print 'POST:',request.POST
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            # print 'form:',form
            # print cat, cat.slug
            # return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form,
                    'category': cat,
                    'category_name_slug': category_name_slug, }

    return render(request, 'rango/add_page.html', context_dict)


def register(request):

    # a boolean value for telling the template whether the registration
    # was successful.
    # set to False initially code change value to  True when reigstration
    # succeeds.
    registered = False

    # If it's a Http Post, we're interested in processing form data.
    if request.method == 'POST':
        # attempt ot grad info from the raw form info.
        # note that we make use of both userform userprofileform
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # if the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # now we hash the password with the set_password method.
            # once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # now sort out the userprofile instance.
            # since we need to set the user attribute ourselves,
            # we set commit=False.
            # this delays saving the model until we're ready to avoid integrity
            # problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        # invalid form or forms mistakes or something else?
        # print problems to the terminal
        # they'll also be shown to the user.
        else:
            print 'user_form errors:', user_form.errors, profile_form.errors

    # not a http post, so we render our form using two modelform instances.
    # these forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):

    # if the request is a HTTP POST, try to pull out the relevant info.
    if request.method == 'POST':
        # gather username and password provided by the user.
        # this info is obtained from the login form.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # use django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if itis.
        user = authenticate(username=username, password=password)

        # if we have a User object, the details are correct.
        # if None , no user with matching redentials was found.
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your rango account is disabled.")
        else:
            print "Invalid login details: {0},{1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    # return HttpResponse("Since you're logged in, you can see this text!")
    return render(request, 'rango/restricted.html', {'info': "Since you're logged in, you can see this text!"})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')


def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = requests_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})


def track_url(request):
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            page = Page.objects.get(id=page_id)
            page.views += 1
            page.save()
            return redirect(page.url)
    return redirect('/rango/')


@login_required
def register_profile(request):

    if request.method == 'POST':
        form = UserProfileForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            if 'picture' in request.FILES:
                form.picture = request.FILES['picture']
            form.save()
            return redirect('/rango/')
        else:
            print form.errors
    else:
        form = UserProfileForm()

    return render(request, 'rango/profile_registration.html', {'form': form})

@login_required
def edit_profile(request, id):
    instance = UserProfile.objects.get(user_id=id)
    form = UserProfileForm(request.POST or None, instance=instance)
    if request.method == 'POST':
            if form.is_valid():
                print request.FILES
                form.save(commit=False)
                if 'picture' in request.FILES:
                    form.picture = request.FILES['picture']
                form.save()    
                return redirect('/rango/profile/')
    return render(request, 'registration/registration_form.html', {'form': form})


@login_required
def profile(request):
    context_dict = {}
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    context_dict['profile'] = profile

    return render(request, 'rango/profile.html', context_dict)


@login_required
def like_category(request):

    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    # users = request.session.get('users')
    # if not users:
    #     request.session['users'] = []
    #     users = request.session['users']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    print cat_list
    return cat_list


def suggest_category(request):

    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion123']

    cat_list = get_category_list(8, starts_with)
    return render(request, 'rango/cats.html', {'cats': cat_list})

@login_required
def auto_add_page(request):
    title = None
    url = None
    cat = None
    context_dict = {}

    if request.method == 'GET':
        title = request.GET['title']
        url = request.GET['url']
        cat_id = request.GET['category_id']
        if cat_id:
            cat = Category.objects.get(id=int(cat_id))
            page = Page.objects.get_or_create(
                category=cat,
                url=url,
                title=title)
            pages = Page.objects.filter(category=cat).order_by('-views')

            context_dict['pages'] = pages

        return render(request, 'rango/page_list.html', context_dict)

def wiki_article_index(request):
    return render(request, 'rango/wiki_index.html', {
        'articles': Article.published.all()
        })

def wiki_article_detail(request, slug):
    return render(request, 'rango/wiki_article_detail.html', {
        'article': Article.objects.get(slug=slug)
        })

# class ArticleDetailView(DetailView):
#     model = Article
#     template_name = "wiki_article_detail"
#     queryset = Article.objects.all()
@login_required
def wiki_add_article(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        msg = "Article saved successfully"
        messages.success(request, msg, fail_silently=True)
        return redirect(article) # call .get_absolute_url() func
    return render(request, 'rango/wiki_article_form.html',
        {'form': form })

@login_required
def wiki_edit_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    form = ArticleForm(request.POST or None, instance=article)
    edit_form = EditForm(request.POST or None)
    if form.is_valid():
        article = form.save()
        if edit_form.is_valid():
            edit = edit_form.save(commit=False)
            edit.article = article
            edit.editor = request.user
            edit.save()
            msg = "Article updated successfully"
            messages.success(request, msg, fail_silently=True)
            return redirect(article)
    return render(request, 'rango/wiki_article_form.html',
        {'form':form,
         'edit_form': edit_form,
         'article': article,})


def wiki_article_history(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article_history = Edit.objects.filter(article__slug=article.slug)
    return render(request, 'rango/wiki_article_history.html',
        {'article': article,
        'article_history': article_history})

# class ArticleListView(ListView):
#     model = Article
#     template_name = "wiki_article_history"









