from models import Item
from django.template import loader, RequestContext
from django.http import HttpResponse


def list(request):
    items = Item.objects.order_by('term')
    template = loader.get_template("list.html")
    context = RequestContext(request, {'glossary_items': items})
    return HttpResponse(template.render(context))
