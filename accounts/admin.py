from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'shipping_address', 'phone')
    search_fields = ('user__username', 'address', 'phone')  # Searching through related user's username and profile fields
    list_filter = ('user__is_active',)  # Filter by whether the user account is active

admin.site.register(Profile, ProfileAdmin)
