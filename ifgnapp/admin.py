from django.contrib import admin
from . models import staff, post, in_link, contact_us, my_image, error_log, course, course_code, g_image
# Register your models here.


class img_Admin(admin.ModelAdmin):
    search_fields = ['name']

class postAdmin(admin.ModelAdmin):
    search_fields = ['title']
    prepopulated_fields = {'slug_name': ('name',)}


admin.site.register(in_link)
admin.site.register(post, postAdmin)
admin.site.register(my_image, img_Admin)
admin.site.register(staff)
admin.site.register(contact_us)
admin.site.register(course)
admin.site.register(course_code)
admin.site.register(g_image)
admin.site.register(error_log)


admin.site.site_header = 'IFGN INSTITUTE ADMIN'  
admin.site.index_title = 'IFGN INSTITUTE ADMIN DATA' 
admin.site.site_title = 'IFGN INSTITUTE ADMINISTRATIONS'

