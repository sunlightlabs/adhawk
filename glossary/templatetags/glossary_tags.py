from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
import glossary.helpers
register = template.Library()


@register.tag
def glossarize(parser, token):
    """
    Add hyperlinks to matching glossary terms between
    {% glosserize %} content {% endglossarize %}
    """
    
    nodelist = parser.parse(('endglossarize',))
    parser.delete_first_token()
    
    return GlossarizeNode(nodelist)

class GlossarizeNode(template.Node):
    
    def __init__(self, nodelist):    
        self.nodelist = nodelist
        
    def render(self, context):
        
        raw_output = self.nodelist.render(context)
        
        glossary.helpers.glossarize_in_context(raw_output, context)
        


@register.simple_tag
def glossary_link(format_string):
    """
    If there is a match, add hyperlink to glossary term.
    """
    return glossary.helpers.glossarize(format_string)
