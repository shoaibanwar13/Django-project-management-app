from django.contrib import admin
from .models import team
from .models import contact
from .models import image
class teamAdmi(admin.ModelAdmin):

    list_display = ('image','name','summ')
    readonly_fields = ('image',)
    fields = ('image','name','summ')
    save_as = True
    
admin.site.register(team)
admin.site.register(contact)
admin.site.register(image)

# Register your models here.
