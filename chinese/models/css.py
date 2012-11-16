# -*- coding: utf-8 -*-
#
# Copyright © 2012 Thomas Tempe <thomas.tempe@alysse.org>
# Copyright © 2012 Roland Sieker <ospalh@gmail.com>

"""
CSS used by the different Chinese models.
"""

style = u'''\
.win .chinese { font-family: "MS Mincho", "ＭＳ 明朝"; }
.mac .chinese { }
.linux .chinese { font-family: "Kochi Mincho", "東風明朝"; }
.mobile .chinese { font-family: "Hiragino Mincho ProN"; }
.question {
background-color: rgb(255, 239, 213);
border-style:dotted;
border-width:1pt;
margin-top:15pt;
margin-bottom:30pt;
padding-top:15px;
padding-bottom:15px;}
.chinese { font-size: 30px }
.tags {color:gray;text-align:right;font-size:10pt;}
.note {color:gray;font-size:12pt;margin-top:20pt;}
.hint {font-size:12pt;}

.tone1 {color: red;}
.tone2 {color: orange;}
.tone3 {color: green;}
.tone4 {color: blue;}
.tone5 {color: gray;}
'''

cloze_style = u'''\
.win .chinese { font-family: "MS Mincho", "ＭＳ 明朝"; }
.mac .chinese { }
.linux .chinese { font-family: "Kochi Mincho", "東風明朝"; }
.mobile .chinese { font-family: "Hiragino Mincho ProN"; }
.question {
background-color: rgb(255, 239, 213);
border-style:dotted;
border-width:1pt;
margin-top:15pt;
margin-bottom:30pt;
padding-top:15px;
padding-bottom:15px;}
.chinese { font-size: 30px }
.tags {color:gray;text-align:right;font-size:10pt;}
.note {color:gray;font-size:12pt;margin-top:20pt;}
.hint {font-size:12pt;}

.tone1 {color: red;}
.tone2 {color: orange;}
.tone3 {color: green;}
.tone4 {color: blue;}
.tone5 {color: gray;}

.cloze {
 font-weight: bold;
 color: blue;
}
'''
