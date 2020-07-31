from django.db import models

# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=50,default="")
    country = models.CharField(max_length=30,default="")
    domain = models.CharField(max_length=20,help_text = "university domain",default="")
    alpha_two_code = models.CharField(max_length=2,help_text = "two letter alpha 2 code",default="")
    web_page = models.CharField(max_length=30,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return (str(self.name))

    def get_model_as_json(self):
        d = dict()
        d['alpha_two_code'] = self.alpha_two_code
        d['country'] = self.country
        d['domain'] = self.domain
        d['name'] = self.name
        d['web_page'] = self.web_page
        d['created_on'] = self.created_on
        return d
