from django.views.generic.edit import DeleteView
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy

class DeleteViewAjax(DeleteView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object() # Bruh why????
        self.object.delete()
        return self.render_to_response()

    def render_to_response(self, **response_kwargs):
        if self.request.is_ajax():
            return JsonResponse({'deleted': True}, safe=False, **response_kwargs)
        # else: # no need for else...
        return HttpResponseRedirect(reverse_lazy('website:homepage_view'))
