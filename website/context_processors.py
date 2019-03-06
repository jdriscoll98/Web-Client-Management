from management.models import Company

def get_companies(request):
    member = request.user
    id = request.session.get('company', None)
    if id and member.is_authenticated():
        company = Company.objects.get(pk=id)
        context = {
        'companies': Company.objects.filter(members__in=[member]),
        'company': company
        }
        return context
    return {'companies': None}
