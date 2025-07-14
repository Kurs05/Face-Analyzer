from django.contrib import admin

from app.models import CustomUser,DetectedFace,Emotion,MediaFile

admin.site.register(CustomUser)
admin.site.register(DetectedFace)
admin.site.register(Emotion)
admin.site.register(MediaFile)


