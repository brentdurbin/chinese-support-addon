# -*- coding: utf-8 -*-
#
# Copyright © 2012 Thomas TEMPÉ, <thomas.tempe@alysse.org>
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#COPYRIGHT AND PERMISSION NOTICE

#Copyright © 1991-2012 Unicode, Inc. All rights reserved. Distributed under the Terms of Use in http://www.unicode.org/copyright.html.

#Permission is hereby granted, free of charge, to any person obtaining a copy of the Unicode data files and any associated documentation (the "Data Files") or Unicode software and any associated documentation (the "Software") to deal in the Data Files or Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, and/or sell copies of the Data Files or Software, and to permit persons to whom the Data Files or Software are furnished to do so, provided that (a) the above copyright notice(s) and this permission notice appear with all copies of the Data Files or Software, (b) both the above copyright notice(s) and this permission notice appear in associated documentation, and (c) there is clear notice in each modified Data File or in the Software as well as in the documentation associated with the Data File(s) or Software that the data or software has been modified.

#THE DATA FILES AND SOFTWARE ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THE DATA FILES OR SOFTWARE.

#Except as contained in this notice, the name of a copyright holder shall not be used in advertising or otherwise to promote the sale, use or other dealings in these Data Files or Software without prior written authorization of the copyright holder.


import re

from aqt import mw, utils
from aqt.editor import Editor
from anki.hooks import addHook, wrap

from chinese.config import chinese_support_config

import Chinese_support
import edit_behavior
import edit_functions
import translate

# Focus lost hook
##########################################################################

def on_focus_lost(flag, fields_data, focus_field):
    field_names = mw.col.models.fieldNames(fields_data.model())
    updated_field = field_names[focus_field]
    efields = dict(fields_data) #user-edited fields
    try:
        model_type = fields_data.model()['addon']
    except:
        model_type = ""
    model_name = fields_data.model()['name']

    edit_behavior.update_fields(efields, updated_field, model_name, model_type)

    for k in field_names:
        if efields[k] <> fields_data[k]:
            fields_data[k] = efields[k]
            flag = True
    
#    if flag:
#        print "Left field ", updated_field, "(polluted)" 
#    else:
#        print "Left field ", updated_field, "(clean)" 
    return flag

def on_chinese_cloze(self):
    highest = 0
    for name, val in self.note.items():
        m = re.findall("\{\{c(\d+)::", val)
        if m:
            highest = max(highest, sorted([int(x) for x in m])[-1])
    
    highest += 1
    # must start at 1
    highest = max(1, highest)

    temp_text = ""
    for name, val in self.note.items():
        temp_text += "name: " + name + " val: " + val + "\n"
    sel = self.web.selectedText()
    temp_text += "selectedText: " + sel + "\n"

    added_pinyin = ""
    if chinese_support_config.options["cloze_options"] == "Add Pinyin":
        added_pinyin = "::" + edit_functions.transcribe(sel)

    trans = translate.cloze_translate_cjklib(sel)
    if "Definition" in self.note:
        self.note["Definition"] += sel + ": " + trans
    if "Stroke Order Links" in self.note:
        self.note["Stroke Order Links"] += edit_functions.get_stroke_order_links(sel)

    temp_text += "trans: " + trans + "\n"

    self.web.eval("wrap('{{c%(high)d::', '%(pinyin)s}}');" %  \
        {"high": highest, "pinyin": added_pinyin})

    # Hack to update the GUI - should probalby replace w/something more appropriate.
    self.setNote(self.note)

    #utils.showInfo(temp_text)

def my_setup_buttons(self):
    but = self._addButton("cloze", lambda s=self: on_chinese_cloze(self), _("Ctrl+Shift+G"), _("Chinese Cloze Deletion + Definition (Ctrl+Shift+G)"), text=u"[Pīnyīn]+Def")
    but.setFixedWidth(66)

Editor.setupButtons = wrap(Editor.setupButtons, my_setup_buttons)

addHook('editFocusLost', on_focus_lost)
