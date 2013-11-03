from django.db import models

class SiteConfiguration(models.Model):
    site_name   = models.CharField(max_length=32)
    site_title  = models.CharField(max_length=32)
    site_head   = models.CharField(max_length=32, blank=True)
    site_subhead= models.CharField(max_length=128, blank=True)
    site_admin  = models.CharField(max_length=128, blank=True)
    site_favicon= models.ImageField(upload_to='sitefavicon', blank=True) 
    site_logo   = models.ImageField(upload_to='sitelogo', blank=True)
    site_theme  = models.CharField(max_length=15,
                    choices=( ('default','Blue'),
                            ('dark','Gray'),
                            ('orange','Orange')
                            ),
                    default='default'
                  ) 
    site_mission= models.CharField(max_length=512, blank=True)
    site_aboutus= models.CharField(max_length=512, blank=True)
    site_contact= models.CharField(max_length=512, blank=True)
    site_imp_ln = models.CharField(max_length=256, blank=True)
    site_reviews= models.CharField(max_length=256, blank=True)
    site_news   = models.CharField(max_length=256, blank=True)
    site_footer = models.CharField(max_length=128, blank=True)     

    def __unicode__(self):
        return self.site_name

    def links_as_list(self):
        return self.site_imp_ln.split(';')

    def reviews_as_list(self):
        return self.site_reviews.split(';')

    def news_as_list(self):
        return self.site_news.split(';')

    @staticmethod
    def set_and_get_default():
        sc = SiteConfiguration() 
        sc.site_name = 'SITE NAME'
        sc.site_title = 'SITE TITLE'
        sc.site_head = 'SITE HEAD'
        sc.site_subhead = 'SITE SUBHEAD'
        sc.site_admin = 'SITE ADMIN'
        sc.site_mission = 'SITE MISSION'
        sc.site_aboutus = 'ABOUT US'
        sc.site_contact = 'SITE CONTACT'
        sc.site_imp_ln = 'IMPORTANT LINK1; IMPORTANT LINK2'
        sc.site_reviews = 'REVIEW1; REVIEW2'
        sc.site_news = 'UPDATE1; UPDATE2'
        sc.site_footer = 'SITE FOOTER'
        sc.save()
        return sc
