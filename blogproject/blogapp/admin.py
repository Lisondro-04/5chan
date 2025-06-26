from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Blog, Review, Comment, Tag

admin.site.register(Blog, SimpleHistoryAdmin)
admin.site.register(Review, SimpleHistoryAdmin)
admin.site.register(Comment, SimpleHistoryAdmin)
admin.site.register(Tag, SimpleHistoryAdmin)
