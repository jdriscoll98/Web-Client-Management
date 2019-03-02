from django.views.generic.edit import DeleteView
from django.http import JsonResponse

class DeleteViewAjax(DeleteView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.render_to_response()

    def render_to_response(self, **response_kwargs):
        return JsonResponse({'deleted': True}, safe=False, **response_kwargs)
