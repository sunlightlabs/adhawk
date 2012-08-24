from models import Item
from django.core.urlresolvers import reverse
from utils.msub import msub_first
from utils.msub import msub_global
from utils.pluralize import pluralize

def glossarize_in_context(raw_output, context, sector=None):
    
    if context.has_key('glossarize'):
        id_list = context['glossarize']
    else:
        id_list = {}
        
    processed_output, id_list = glossarize(raw_output, id_list, sector)
    
    context['glossarize'] = id_list 
    
    return processed_output



def glossarize(plain, id_list=None, sector=None):
    """
    Converts a string into a hyperlinked string.

    Notes:
    * Only the first occurence for each term is replaced.
    * It looks at one glossary item at a time.
    * Longer glossary items match first.
    """
    
    if not id_list: 
        id_list = {} 

    base_url = reverse("glossary")

    # Do initial sort
    if sector:
        items = Item.objects.filter(sectors=sector)
    else:
        items = Item.objects.all()
            


    def link(item):
        # Note that the asterisk (*) has special meaning for msub_first and
        # msub_global.
        return """<a href="%s#%s">*</a>""" % (base_url, item.slug)

    mapping = []
    for item in items.order_by('-term_length'):
        
        hyperlink = link(item)
        variations = []
        
        if item.term != '':
            variations.append(item.term)
            variations.append(pluralize(item.term))
        
        if item.acronym != '':
            variations.append(item.acronym)
            
        if item.synonym != '':
            variations.append(item.synonym)
            variations.append(pluralize(item.synonym))
            
        for variant in variations:
            if variant:
                mapping.append((r"\b%s\b" % variant, hyperlink, item.id))

    text, id_list = msub_first(plain, mapping, id_list)
    return text, id_list
