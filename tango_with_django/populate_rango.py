__author__ = 'user'


import os
import sys


def populate():
    python_cat = add_cat("Python")

    add_page(cat=python_cat,
             title="Official Django Tutorial",
             url="http://docs.python.org/2/tutorial/",
             views=5)

    add_page(cat=python_cat,
             title="How to Think Like a Computer Scientist",
             url="http://www.greenteapress.com/thinkpython",
             views=10)

    add_page(cat=python_cat,
             title="Learn Python in 10 minutes",
             url="http://korokithakis.net/tutorials/python")

    django_cat = add_cat("Django")

    add_page(cat=django_cat,
             title="Official Django Tutorial",
             url="http://docs.djangoproject.com/en/1.5/intro/tutorial01/",
             views=10)

    add_page(cat=django_cat,
             title="Django Rocks",
             url="http://www.djangorocks.com/")

    add_page(cat=django_cat,
             title="How to Tango with Django",
             url="http://www.tangowithdjango.com/",
             views=20)

    frame_cat = add_cat("Other Frameworks")

    add_page(cat=frame_cat,
             title="Bottle",
             url="http://www.bottlepy.org/docs/dev/")

    add_page(cat=frame_cat,
             title="Flask",
             url="http://flask.pocoo.org/",
             views=15)

    #Print added stuff
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "-{0} -{1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

#Start execution
if __name__ == "__main__":
    print "Starting rango population script"
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django.settings')
    from rango.models import Category, Page
    populate()