import re

VOWELS = set('aeiou')

def pluralize(singular):
    ABERRANT_PLURAL_MAP = {
    'appendix': 'appendices',
    'barracks': 'barracks',
    'cactus': 'cacti',
    'child': 'children',
    'criterion': 'criteria',
    'deer': 'deer',
    'echo': 'echoes',
    'elf': 'elves',
    'embargo': 'embargoes',
    'focus': 'foci',
    'fungus': 'fungi',
    'goose': 'geese',
    'hero': 'heroes',
    'hoof': 'hooves',
    'index': 'indices',
    'knife': 'knives',
    'leaf': 'leaves',
    'life': 'lives',
    'man': 'men',
    'mouse': 'mice',
    'nucleus': 'nuclei',
    'person': 'people',
    'phenomenon': 'phenomena',
    'potato': 'potatoes',
    'self': 'selves',
    'syllabus': 'syllabi',
    'tomato': 'tomatoes',
    'torpedo': 'torpedoes',
    'veto': 'vetoes',
    'woman': 'women',
    }
    
    if not singular:
        return ''
    plural = ABERRANT_PLURAL_MAP.get(singular)
    if plural:
        return plural
    root = singular
    try:
        if singular[-1] == 'y' and singular[-2] not in VOWELS:
            root = singular[:-1]
            suffix = 'ies'
        elif singular[-1] == 's':
            if singular[-2] in VOWELS:
                if singular[-3:] == 'ius':
                    root = singular[:-2]
                    suffix = 'i'
                else:
                    root = singular[:-1]
                    suffix = 'ses'
            else:
                suffix = 'es'
        elif singular[-2:] in ('ch', 'sh'):
            suffix = 'es'
        else:
            suffix = 's'
    except IndexError:
        suffix = 's'
    plural = root + suffix
    return plural
    
def first_letter_cap(string):
    out_words = []
    in_words = string.split(' ')
    for word in in_words:
        fl = word[0]
        out_words.append(''.join(['[',fl.upper(),fl.lower(),']',word[1:]]))
    return ' '.join(out_words)

def msub_global(plain,mapping):
    # Not making use of id_list, for now
    map_sort = sorted(mapping,key=lambda x: len(x[0].string),reverse=True)
    found_so_far = []
    for m in map_sort:
        skip = False
        variant,hyperlink,item_id = m
        for s in found_so_far:
            if variant.string.lower() in s:
                skip = True
        if skip:
            continue
        else:
            hyperlink = hyperlink.replace('*',variant.string)
            if variant.is_acronym:
                prog = re.compile(re.escape(variant.string))
            else:
                prog = re.compile(re.escape(variant.string),re.I)
            plain_split = prog.split(plain)
            if len(plain_split) > 1:
                found_so_far.append(variant.string.lower())
            plain = hyperlink.join(plain_split)
    return plain
