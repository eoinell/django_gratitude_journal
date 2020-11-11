from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Word(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    text = models.CharField(max_length=100)
    sub_date = models.DateTimeField('submission_date')
    
    def streak(self): # -> days
        streak = 0
        prev_date = datetime.now()
        for word in self.objects.order_by('-sub_date'):
            if (prev_date - word.sub_date).hours < 48:
                prev_date = word.sub_date
                streak += 1
        return streak
    
    def __str__(self):
        return self.text


# default = Word(User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword').id,
#                                         'Yoko',
#                                         datetime.now())

