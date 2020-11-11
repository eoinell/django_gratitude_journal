import os, random
from django import template

register = template.Library()

@register.simple_tag
def bg():
    relpath =  r"static\\logger\\images\\"
    path = os.path.join(os.path.dirname(__file__),'..', relpath)
    choices = os.listdir(path)
    return 'logger//images//' + str(random.choice(choices))