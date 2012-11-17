# -*- coding: utf-8 -*-
# 
# Copyright © 2012 Thomas Tempe <thomas.tempe@alysse.org>
# Copyright © 2012 Roland Sieker <ospalh@gmail.com>
#
# Original: Damien Elmes <anki@ichi2.net> (as japanese/model.py)
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

import anki.stdmodels
from anki.consts import MODEL_CLOZE
from css import cloze_style

# List of fields
######################################################################

fields_list = ["Text", "Pinyin", "Definition", "Extra", "Stroke Order Links"]

# Card templates
######################################################################

card_front = u'''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>
<div class=question>
<span class=chinese>{{cloze:Text}}</span>
</div>
'''

card_back = u'''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>
<div class=question>
<span class=chinese>{{cloze:Text}}</span><br/>
{{Pinyin}}<br/>
<div class=meaning>{{Definition}}</div><br/>
<div class=note>{{Extra}}</div><br/>
<div class=chinese>{{Stroke Order Links}}</div>
</div>

'''


# Add model for chinese word to Anki
######################################################################

def add_model_chinese_cloze(col):
    mm = col.models
    m = mm.new("Chinese Cloze")
    m['type'] = MODEL_CLOZE
    # Add fields
    for f in fields_list:
        fm = mm.newField(f)
        mm.addField(m, fm)
    t = mm.newTemplate(u"Cloze")
    t['qfmt'] = card_front
    t['afmt'] = card_back
    mm.addTemplate(m, t)

    m['css'] += cloze_style
    m['addon'] = 'Chinese Cloze'
    mm.add(m)

    return m

anki.stdmodels.models.append(("Chinese Cloze", add_model_chinese_cloze))
