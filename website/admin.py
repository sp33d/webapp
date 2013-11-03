from django.contrib import admin
from website.models import SiteConfiguration

class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        'site_name',
        'site_title',
        'site_contact',
        'site_footer',
        )

admin.site.register(SiteConfiguration, SiteConfigurationAdmin)
