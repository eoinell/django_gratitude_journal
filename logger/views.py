from datetime import datetime, timedelta

from django.utils import timezone

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib import messages

from .models import Word
from django import forms

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import urllib, base64

def plot_to_uri(figure):
    buf = io.BytesIO()
    figure.savefig(buf, format='png', dpi=1_500)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return urllib.parse.quote(string)

class GratForm(forms.Form):
    log_field = forms.CharField(label='', max_length=200)

def index(request, error=False):
    form = GratForm()
    return render(request, 'logger/index.html', {'form': form, 'error': error})

def log(request):
    if request.user.is_authenticated:

        form = GratForm(request.POST)
        if form.is_valid():
            
            text = form.cleaned_data['log_field']
            word_kwargs = {'user': request.user,
                            'sub_date': timezone.now()}
            for group in text.split(','):
                w = Word(text=group.strip(), **word_kwargs)
                w.save()
            return HttpResponseRedirect(reverse('logger:submitted'))
        return HttpResponseRedirect(reverse('logger:index', args=(True)))
    else:
        messages.info(request, 'Please login first to save your gratitudes!')
        return HttpResponseRedirect(reverse('login'))

def submitted(request):
    
    words = map(lambda x: x.text, Word.objects.filter(
                                                    sub_date__date=datetime.today().date(),
                                                    sub_date__gte=datetime.now() - timedelta(weeks=1) 
                                                ).order_by('-sub_date')
                )
    seen = set()
    recent_words = [w for w in words if not (w in seen or seen.add(w))]
    
    words = Word.objects.all()
    text = ' '.join([w.text for w in words])
    if text:
        wc = WordCloud(background_color="white")
        
        wc.generate(text)
        fig, ax = plt.subplots()
        ax.imshow(wc, interpolation='bilinear', cmap=plt.cm.gray)
        ax.axis('off')
    else:
        fig, ax = plt.subplots()
        ax.annotate('You need to log some words first!', (0.5, 0.5), fontsize='xx-large')
        ax.axis('off')
    uri = plot_to_uri(fig)
        

    return render(request, 'logger/breakdown.html', {"recent_words": recent_words,
                                                     "plot": uri})

    