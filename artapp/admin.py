from django.contrib import admin
from artapp.models import Art
from artapp.models import Artist

admin.site.register(Artist)

class ArtAdmin(admin.ModelAdmin):
		prepopulated_fields = {'slug': ('title',)}
		list_display = ('title', 'created_at') #will have 'artist' when that is written 
		search_fields = ['title']
admin.site.register(Art, ArtAdmin)