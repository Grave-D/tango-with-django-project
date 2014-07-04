from compiler.visitor import ASTVisitor
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, request
from django.http.response import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from rango.bing_search import run_query
from rango.models import Category, Page, User, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm


def encode_url(category_name):
    # Returns category_name_url
    return category_name.replace(' ', '_')


def decode_category_name(category_name_url):
    # Returns category name
    return category_name_url.replace('_', ' ')


def get_category_list(max_results=0, starts_with=''):
    category_list = []
    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)
    else:
        category_list = Category.objects.all()

    if max_results > 0:
        if len(category_list) > max_results:
            category_list = category_list[:max_results]

    for category in category_list:
        category.url = encode_url(category.name)
    return category_list


def index(request):
    # Obtain the context from the HTTP request
    context = RequestContext(request)
    # Query the database for categories
    # and order it by likes in descending oder
    category_list = get_category_list()
    pages = Page.objects.all().order_by("views")[:5].reverse()

    context_dict = {'categories': category_list, 'pages': pages, }
    # Create a URL attribute for every category found
    # by replacing spaces to underscores
    """ Aaaand all that was for nothing because we're doing it session way.
        This piece of code is for cookie training only I guess
    # Get response earlier to work with cookies
    response = render_to_response("rango/index.html", context_dict, context)
    visits = int(request.COOKIES.get('visits', '0'))
    # Check if the cookie exists, get last_visit time
    if request.COOKIES.has_key('last_visit'):
        last_visit = request.COOKIES['last_visit']
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        # Check if you should add a visit and update last_visit_time
        if (datetime.now() - last_visit_time).seconds > 5:
            response.set_cookie('visits', visits+1)
            response.set_cookie('last_visit', datetime.now())
    # If 'last_visit' cookie doesn't exist - create it
    else:
        response.set_cookie('last_visit', datetime.now())
    # Return the response with cookies
    return response
    """
    # Now let's get to sessions. Lookup comments to cookies if needed
    if request.session.get('last_visit'):
        last_visit = request.session.get('last_visit')
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        visits = request.session.get('visits', 0)
        if (datetime.now() - last_visit_time).days > 0:
            request.session['visits'] = visits+1
            request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
    return render_to_response('rango/index.html', context_dict, context)


def about(request):
    context = RequestContext(request)
    if request.session.get('visits'):
        visit_count = request.session.get('visits')
        last_visit_time = datetime.strptime(request.session.get('last_visit')[:-7], "%Y-%m-%d %H:%M:%S")
    else:
        visit_count = 0
        last_visit_time = datetime.now()
    category_list = get_category_list()
    context_dict = {'about_message': 'This is about page', 'visits': visit_count,
                    'last_visit_time': last_visit_time, 'categories': category_list,}
    return render_to_response("rango/about.html", context_dict, context)


def category(request, category_name_url):
    context = RequestContext(request)
    # Replace undrescores in ulr to spaces
    category_name = decode_category_name(category_name_url)
    category_list = get_category_list()
    context_dict = {'category_name': category_name, 'categories': category_list,}
    if request.method == "POST":
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
            context_dict['result_list'] = result_list


    try:
        category = Category.objects.get(name=category_name)
        # return pages associated to the category
        pages = Page.objects.filter(category=category)
        # Add category to context dictionary to verify category exists
        context_dict['category'] = category
        context_dict['pages'] = pages
        context_dict['category_name_url'] = category_name_url

    except Category.DoesNotExist:
        # Template will display "Does not exist" message
        pass

    return render_to_response('rango/category.html', context_dict, context)


@login_required
def profile(request):
    context = RequestContext(request)
    try:
        basic_user = User.objects.get(request.user)
        user_profile = UserProfile.objects.get(user=basic_user)
        category_list = get_category_list()
        context_dict = {"user_profile": user_profile, "basic_user": basic_user, "categories": category_list}
    except User.DoesNotExist:
        #Template to deal with non-existant user
        pass
    return render_to_response('rango/profile.html', context_dict, context)


@login_required
def add_category(request):
    # Get the context from request
    context = RequestContext(request)

    # HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Save category to database
            form.save(commit=True)
            # Return to index page
            return index(request)
        else:
            # If form is invalid - print error message
            print(form.errors)
    else:
        # If the form.method isn't POST, display form to enter details
        form = CategoryForm()
        # If the form is bad, render the form with error message
        category_list = get_category_list()
        context_dict = {'form': form, 'categories': category_list,}
    return render_to_response('rango/add_category.html', context_dict, context)


@login_required
def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_category_name(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            # This time we can't commit right away
            # We need to fill associated category manually.
            page = form.save(commit=False)
            # Retrieving Category object so we can add it
            cat = Category.objects.get(name=category_name)
            page.category = cat
            # Also we need to add the default number of views
            page.views = 0
            page.save()

            return category(request, category_name_url)
        else:
            print(form.errors)
    else:
        form = PageForm()
    category_list = get_category_list()
    context_dict = {'category_name_url': category_name_url, 'category_name': category_name,
                    'form': form, 'categories': category_list,}
    return render_to_response('rango/add_page.html', context_dict, context)


def register(request):
    # Getting context
    context = RequestContext(request)

    #  A boolean value which shows if a registration was successful.
    #  Initially set to False
    registered = False

    # If request.method is HHTP Post then process form data
    if request.method == 'POST':
        # Attempt to grab data from form information
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If two forms are valid, process data:
        if user_form.is_valid() and profile_form.is_valid():
            # Saving user data in the database...
            user = user_form.save()
            # We need to hash user password before saving user
            user.set_password(user.password)
            user.save()
            # Saving user_profile data
            # Since we need to set user attributes ourselves, we set commit=False
            # This delays saving the model until it's ready
            profile = profile_form.save(commit=False)
            profile.user = user
            # If the user provided a profile picture we should get it from the input
            # and put in the UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                # Now we can save our user
            profile.save()
            registered = True

        # If either form is invalid, show errors
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, then render blank forms using two ModelForm instances
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Finally render the template depending on content
    category_list = get_category_list()
    context_dict = {'user_form': user_form, 'profile_form': profile_form,
                    'registered': registered, 'categories': category_list,}
    return render_to_response('rango/register.html', context_dict, context)


def user_login(request):
    # Get context from request
    context = RequestContext(request)
    # If the request is a POST, try to get data
    if request.method == 'POST':
        # Get the username and password provided by user
        username = request.POST['username']
        password = request.POST['password']

        # This line uses Django's machinery to check
        # if username and password are valid. If it is - user object is returned
        user = authenticate(username=username, password=password)

        # If we haven't got a user object(username or password are not valid),
        # Django returns None as user object
        if user is not None:
            # Check if user account is active
            if user.is_active:
                # Login user if account is active
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # Account is not active - no login
                return HttpResponse('Your account is disabled.')
        else:
            # Bad username or password was provided. No login.
            print 'Invalid login information: {0}, {1}'.format(username, password)
            return HttpResponse('Incorrect username or password.')

    else:
        # Request is not a POST request, so show login form
        return render_to_response('rango/login.html', {}, context)


@login_required
def restricted(request):
    category_list = get_category_list()
    context_dict = {'categories': category_list,}
    return render_to_response('rango/restricted.html', context_dict)


# Use the login_required decorator to ensure only logged in users can access this view
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')


def search(request):
    context = RequestContext(request)
    result_list = []

    if request.method == "POST":
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)

    return render_to_response('rango/search.html', {'result_list': result_list}, context)


def track_url(request, page_id):
    url = '/rango/'
    try:
        page = Page.objects.get(id=page_id)
        page.views += 1
        page.save()
        url = page.url
    except Page.DoesNotExist:
        # For future development
        pass
    return redirect(url)


@login_required
def like_category(request):
    context = RequestContext(request)
    likes = 0
    cat_id = None
    if request.method == "GET":
        cat_id = request.GET["category_id"]
    if cat_id:
        category = Category.objects.get(id=cat_id)
        if category:
            likes = category.likes + 1
            category.likes = likes
            category.save()
    return HttpResponse(likes)


def suggest_category(request):
    context = RequestContext(request)
    starts_with = ''
    cat_list = []
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_category_list(8, starts_with)
    return render_to_response('rango/category_list.html', {'categories' : cat_list}, context)


@login_required
def auto_add_page(request):
    context = RequestContext(request)
    cat_id = None
    url = None
    title = None
    category = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        title = request.GET['title']
        url = request.GET['url']
    if cat_id:
        category = Category.objects.get(id=int(cat_id))
        p = Page.objects.get_or_create(category=category, title=title, url=url)
        pages = Page.objects.filter(category=category).order_by('-views')
    context_dict = {'pages': pages}
    return render_to_response('rango/page_list.html', context_dict, context)