from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from rest_framework.authtoken.models import Token


class ApiKeyGeneratorView(LoginRequiredMixin, View):
    def get(self, request):
        qs__token = Token.objects.filter(user=request.user)
        if qs__token.exists():
            template_data = {'token': qs__token.get()}
            return render(request, 'api/api_guide.html', template_data)

        return render(request, 'api/api_guide.html', {})

    def post(self, request):
        token, _ = Token.objects.get_or_create(user=request.user)
        return render(request, 'api/api_guide.html', {'token': token})
