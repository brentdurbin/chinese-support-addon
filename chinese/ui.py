# -*- coding: utf-8 -*-
#
# Copyright © 2012 Thomas TEMPÉ, <thomas.tempe@alysse.org>
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#COPYRIGHT AND PERMISSION NOTICE

#Copyright © 1991-2012 Unicode, Inc. All rights reserved. Distributed under the Terms of Use in http://www.unicode.org/copyright.html.

#Permission is hereby granted, free of charge, to any person obtaining a copy of the Unicode data files and any associated documentation (the "Data Files") or Unicode software and any associated documentation (the "Software") to deal in the Data Files or Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, and/or sell copies of the Data Files or Software, and to permit persons to whom the Data Files or Software are furnished to do so, provided that (a) the above copyright notice(s) and this permission notice appear with all copies of the Data Files or Software, (b) both the above copyright notice(s) and this permission notice appear in associated documentation, and (c) there is clear notice in each modified Data File or in the Software as well as in the documentation associated with the Data File(s) or Software that the data or software has been modified.

#THE DATA FILES AND SOFTWARE ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THE DATA FILES OR SOFTWARE.

#Except as contained in this notice, the name of a copyright holder shall not be used in advertising or otherwise to promote the sale, use or other dealings in these Data Files or Software without prior written authorization of the copyright holder.


from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, openLink, askUser
import aqt.addons 
from anki.hooks import wrap

from config import chinese_support_config
import __init__
import translate
import Chinese_support
import edit_behavior

ui_actions = {}
dictionaries = [ "None", "CEDICT", "HanDeDict", "CFDICT"]
transcriptions = [
    "Pinyin", "WadeGiles", "CantoneseYale", "Jyutping", "Bopomofo"]
speech_options = [ "None", "Google TTS Mandarin"]
cloze_options = ["Add Pinyin", "Do Not Add Pinyin"]

def display_next_tip():
    (tip, link) = chinese_support_config.get_next_tip()
    if tip:
        if link:
            if askUser(tip):
                openLink(link)
        else:
            showInfo(tip)


def setup_plugin():
    openLink("https://github.com/ttempe/chinese-support-addon/wiki/Setup-Instructions")

def help_plugin():
    openLink("https://github.com/ttempe/chinese-support-addon/wiki")

def about_plugin():
    showInfo(u"Chinese support plugin v. " + __init__.__version__ + u"<br>Copyright © 2012 Thomas TEMP&Eacute; and many others.<br><br>Please see source code for additional info.")

def set_dict_constructor(dict):
    def set_dict():
        update_dict_action_checkboxes()
        translate.set_dict(dict)
    return set_dict

def set_option_constructor(option, value):
    def set_option():
        chinese_support_config.set_option(option, value)
        update_dict_action_checkboxes()
    return set_option


edit_window = None

def edit_logic_ok():
    open(Chinese_support.edit_behavior_filename, "w").write(edit_window.text.toPlainText().encode("utf8"))
    reload(edit_behavior)

def edit_logic():
    d = QDialog(mw)
    global edit_window
    edit_window = aqt.forms.editaddon.Ui_Dialog()
    edit_window.setupUi(d)
    d.setWindowTitle(_("Configure behavior of note edit dialog box"))
    edit_window.text.setPlainText(unicode(open(Chinese_support.edit_behavior_filename).read(), "utf8"))
    d.connect(edit_window.buttonBox, SIGNAL("accepted()"), edit_logic_ok)
    d.exec_()

def add_action(title, to, funct, checkable=False):
    action = QAction(_(title), mw)
    if checkable:
        action.setCheckable(True)
    mw.connect(action, SIGNAL("triggered()"), funct)
    to.addAction(action)
    return action

def update_dict_action_checkboxes():
    global ui_actions
    for d in dictionaries:
        ui_actions["dict_"+d].setChecked(d==chinese_support_config.options["dictionary"])
    for t in transcriptions:
        ui_actions["transcription_"+t].setChecked(t==chinese_support_config.options["transcription"])
    for t in speech_options:
        ui_actions["speech_"+t].setChecked(t==chinese_support_config.options["speech"])
    for c in cloze_options:
        ui_actions[c].setChecked(c==chinese_support_config.options["cloze_options"])


def myRebuildAddonsMenu(self):
    global ui_actions
    for m in self._menus:
        if "Chinese_support"==m.title():
            sm=m.addMenu(_("Set dictionary"))
            for i in dictionaries:
                ui_actions["dict_"+i]=add_action(i, sm, set_dict_constructor(i),True)
            sm=m.addMenu(_("Set transcription"))
            for i in transcriptions:
                ui_actions["transcription_"+i]=add_action(i, sm, set_option_constructor("transcription", i), True)
            sm=m.addMenu(_("Set speech language"))
            for i in speech_options:
                ui_actions["speech_"+i]=add_action(i, sm, set_option_constructor("speech", i), True)
            sm=m.addMenu(_("Chinese Cloze Behavior"))
            ui_actions["Add Pinyin"]=add_action("Add Pinyin to Cloze", sm, set_cloze_add_pinyin, True)
            ui_actions["Do Not Add Pinyin"]=add_action("Do Not Add Pinyin to Cloze", sm, set_cloze_no_add_pinyin, True)

            add_action(_("Editor Behavior"), m, edit_logic)
            add_action(_("Setup instructions"), m, setup_plugin)
            add_action(_("Help"), m, help_plugin)
            add_action(_("About..."), m, about_plugin)
            m.setTitle(_("Chinese support"))
            update_dict_action_checkboxes()
            break

aqt.addons.AddonManager.rebuildAddonsMenu = wrap(aqt.addons.AddonManager.rebuildAddonsMenu, myRebuildAddonsMenu)

display_next_tip()
