from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Client, Cost

# client views
class AddClient(LoginRequiredMixin, CreateView):
    model = Client
    fields = '__all__'

class DeleteClient(LoginRequiredMixin, DeleteView):
    model = Client

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        return JSONResponse({'deleted': True}, safe=False, **response_kwargs)

class UpdateClient(LoginRequiredMixin, UpdateView):
    model = Client
    fields = '__all__'

# cost views
class AddCost(LoginRequiredMixin, CreateView):
    model = Cost
    fields = '__all__'

class UpdateCost(LoginRequiredMixin, UpdateView):
    model = Cost
    fields = '__all__'

class DeleteCost(LoginRequiredMixin, DeleteView):
    model = Cost
