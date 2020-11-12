import os, random
from django import template
from django.contrib.staticfiles import finders


register = template.Library()

@register.simple_tag
def bg():
    p = finders.find('logger/images')
    choices = os.listdir(p)
    # return '/images/' +  str(random.choice(choices))
    return 'images/' + "nathan-dumlao-EwaV3HjwmUo-unsplash.jpg"