from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
# from django.core.mail import send_mail, BadHeaderError
# from django.http import HttpResponse
#
# from Habr.settings import DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL

from django.views.static import serve
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from Face_Analyzer.analize import analize_emotions, analize_landmarks
from . import models
from .forms import SignUpForm, LoginForm

from .models import MediaFile, CustomUser

import logging
import numpy as np


def clean_for_json(obj):
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(i) for i in obj]
    elif isinstance(obj, tuple):
        return list(obj)  # JSON не поддерживает tuple
    elif isinstance(obj, (np.float32, np.float64)):
        return round(float(obj), 2)  # Округляем до двух знаков после запятой
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    else:
        return obj

logger = logging.getLogger('django')
def media(request, path):
    return serve(request, path, document_root=settings.MEDIA_ROOT)

class mainClass(View):
    def get(self, request):
        return render(request,'app/main_template.html')
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = SignUpForm()
    return render(request, 'app/registration/signup.html', {'form': form})

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
    return render(request, 'app/registration/login.html', {'form': form})

class ResetPasswordView(PasswordResetView):
    pass

def analize_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        file_type =''
        if not uploaded_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        content_type = uploaded_file.content_type
        if content_type.startswith('image/'):
            file_type = 'image'
        elif content_type.startswith('video/'):
            file_type = 'video'
        else :
            return JsonResponse({'error': 'Unsupported file type'}, status=400)

        path = default_storage.save(f'uploads/{uploaded_file.name}', ContentFile(uploaded_file.read()))
        filename = path.split('/')[-1]
        logger.info(f'File PATH: { path}')
        user = cast(CustomUser, request.user)
        file = MediaFile.objects.create(start_file=path,file_type=file_type,file_name=filename,user = user)
        try:
            new_file_data = analize_emotions(file)
            new_file=new_file_data['media_path'].split('media/')[-1]
            data = new_file_data['data']
            count = len(data)
            logger.info(f'NewFile PATH: {new_file}')
            file.end_file = new_file
            file.processed = True

            msg=''
            if count ==1:
                msg='найдено лицо'
            else :
                msg='найдены лица'

            landmarks_data = analize_landmarks(file)
            file_landmarks = landmarks_data['media_path'].split('media/')[-1]

            file.landmarks_file = file_landmarks

            file.save()
            clear_data= clean_for_json(data)
            for face in clear_data:
                id = face['Id']
                Face = models.DetectedFace.objects.create(media=file,name=f'face {id}',data=face)
                for emotion_type, val in face['emotion'].items():
                    Emotion = models.Emotion.objects.create(face=Face,type=emotion_type,confidence=val)
            return JsonResponse({'face_data':clear_data,
                                 'message': f'{msg}',
                                 'end_file_path': settings.MEDIA_URL+new_file,
                                 'start_file_path': settings.MEDIA_URL+path,
                                 'count_faces': count,
                                 'file_landmarks': settings.MEDIA_URL+file_landmarks})
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=422)
        except Exception as e:
            logger.error(f"Ошибка обработки: {str(e)}", exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)


class MyResultsListView(LoginRequiredMixin, ListView):
    model = MediaFile
    template_name = 'app/my_results.html'
    context_object_name = 'media_files'

    def get_queryset(self):
        return MediaFile.objects.filter(user=self.request.user).order_by('-uploaded_at')


class MediaDetailView(LoginRequiredMixin, DetailView):
    model = MediaFile
    template_name = 'app/media_detail.html'
    context_object_name = 'media'

    def get_queryset(self):
        return MediaFile.objects.filter(user=self.request.user)
