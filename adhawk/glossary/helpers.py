from models import Item
from django.core.urlresolvers import reverse
## These were imported, but i don't have them so I wrote them. -Bob
#from utils.msub import msub_first
#from utils.msub import msub_global
#from utils.pluralize import pluralize
#from utils.msub import msub_global
from glossary.utils import pluralize,msub_global

class Variation(object):
    def __init__(self,string,is_acronym=False):
        self.string = string
        self.is_acronym = is_acronym

    def __unicode__(self):
        return self.string

def glossarize_in_context(raw_output, context, sector=None):
    
    #if context.has_key('glossarize'):
    #    id_list = context['glossarize']
    #else:
    #    id_list = {}
        
    processed_output = glossarize(raw_output)
    
    #context['glossarize'] = id_list 
    
    return processed_output

def glossarize(plain):
    """
    Converts a string into a hyperlinked string.

    Notes:
    * Only the first occurence for each term is replaced.
    * It looks at one glossary item at a time.
    * Longer glossary items match first.
    """
    
    #if not id_list: 
    #    id_list = {} 


    # Do initial sort
    #if sector:
    #    items = Item.objects.filter(sectors=sector)
    #else:
    items = Item.objects.all()
            
    def link(item):
        # Note that the asterisk (*) has special meaning for msub_first and
        # msub_global.
        return """<a class="openModal" definition="%s">*</a>""" % (item.slug,)

    mapping = []
    for item in items.order_by('-term_length'):
        
        hyperlink = link(item)
        variations = []
        
        if item.term != '':
            variations.append(Variation(item.term))
            variations.append(Variation(pluralize(item.term)))
        
        if item.acronym != '':
            variations.append(Variation(item.acronym,is_acronym=True))
            
        if item.synonym != '':
            variations.append(Variation(item.synonym))
            variations.append(Variation(pluralize(item.synonym)))
            
        for variant in variations:
            if variant:
                mapping.append((variant, hyperlink, item.id))
    #print variations            

    text = msub_global(plain, mapping)
    return text
