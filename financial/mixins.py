from django.views.generic.edit import DeleteView

class DeleteViewAjax(DeleteView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        return JSONResponse({'deleted': True}, safe=False, **response_kwargs)
