# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
# 
# The contents of this file are subject to the Mozilla Public License
# Version 1.1 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
# 
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
# License for the specific language governing rights and limitations
# under the License.
# 
# The Original Code is Komodo code.
# 
# The Initial Developer of the Original Code is ActiveState Software Inc.
# Portions created by ActiveState Software Inc are Copyright (C) 2000-2007
# ActiveState Software Inc. All Rights Reserved.
# 
# Contributor(s):
#   ActiveState Software Inc
# 
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
# 
# ***** END LICENSE BLOCK *****

# Komodo TemplateToolkit language service.
#
# Generated by 'luddite.py' on Thu Jul  5 12:35:35 2007.
#

import logging
import re
from xpcom import components
from xpcom.server import UnwrapObject
from koXMLLanguageBase import koHTMLLanguageBase


import scimozindent

log = logging.getLogger("koTemplateToolkitLanguage")
#log.setLevel(logging.DEBUG)


def registerLanguage(registry):
    log.debug("Registering language TemplateToolkit")
    registry.registerLanguage(KoTemplateToolkitLanguage())


class KoTemplateToolkitLanguage(koHTMLLanguageBase):
    name = "TemplateToolkit"
    lexresLangName = "TemplateToolkit"
    _reg_desc_ = "%s Language" % name
    _reg_contractid_ = "@activestate.com/koLanguage?language=%s;1" % name
    _reg_clsid_ = "{6072ecd4-525e-11db-82d8-000d935d3368}"
    _reg_categories_ = [("komodo-language", name)]
    defaultExtension = '.ttkt.html'

    lang_from_udl_family = {'CSL': 'JavaScript', 'TPL': 'TemplateToolkit', 'M': 'HTML', 'CSS': 'CSS', 'SSL': 'Perl'}

    sample = """[% INCLUDE header
   title = 'Template Toolkit CGI Test'
%]

<a href="mailto:[% email %]">Email [% me.name %]</a>

<p>This is version [% version %]</p>

<h3>Projects</h3>
<ul>
[% FOREACH project IN worklist(me.id) %]
   <li> <a href="[% project.url %]">[% project.name %]</a>
[% END %]
</ul>

[% INCLUDE footer %]
"""

    def __init__(self):
        koHTMLLanguageBase.__init__(self)
        self.matchingSoftChars["%"] = ("%", self.softchar_accept_bracket_percent)
        
    def softchar_accept_bracket_percent(self, scimoz, pos, style_info, candidate):
        """Look for |<%, both TPL_OPERATOR at start
        """
        return self.softchar_accept_styled_chars(
            scimoz, pos, style_info, candidate,
            {'styled_chars' : [
                    (scimoz.SCE_UDL_TPL_OPERATOR, ord("["))
                ]
            })

    def computeIndent(self, scimoz, indentStyle, continueComments):
        return self._computeIndent(scimoz, indentStyle, continueComments, self._style_info)

    def _computeIndent(self, scimoz, indentStyle, continueComments, style_info):
        res = self._doIndentHere(scimoz, indentStyle, continueComments, style_info)
        if res is None:
            return koHTMLLanguageBase.computeIndent(self, scimoz, indentStyle, continueComments)
        return res

    def _keyPressed(self, ch, scimoz, style_info):
        res = self._doKeyPressHere(ch, scimoz, style_info)
        if res is None:
            return koHTMLLanguageBase._keyPressed(self, ch, scimoz, style_info)
        return res

    _startWords = "IF UNLESS ELSE ELSIF SWITCH FOREACH WHILE TRY CATCH FILTER PERL RAWPERL BLOCK WRAPPER"
    def _doIndentHere(self, scimoz, indentStyle, continueComments, style_info):
        # Returns either None or an indent string
        pos = scimoz.positionBefore(scimoz.currentPos)
        startPos = scimoz.currentPos
        style = scimoz.getStyleAt(pos)
        if style != scimoz.SCE_UDL_TPL_OPERATOR:
            return None
        if scimoz.getWCharAt(pos) != "]":
            return None
        pos -= 1
        style = scimoz.getStyleAt(pos)
        if style != scimoz.SCE_UDL_TPL_OPERATOR:
            return None
        if scimoz.getWCharAt(pos) != "%":
            return None
        pos -= 1
        curLineNo = scimoz.lineFromPosition(pos)
        lineStartPos = scimoz.positionFromLine(curLineNo)
        delta, numTags = self._getTagDiffDelta(scimoz, lineStartPos, startPos)
        if delta < 0 and numTags == 1 and curLineNo > 0:
            didDedent, dedentAmt = self.dedentThisLine(scimoz, curLineNo, startPos)
            if didDedent:
                return dedentAmt
            else:
                return None
        indentWidth = self._getIndentWidthForLine(scimoz, curLineNo)
        indent = scimoz.indent
        newIndentWidth = indentWidth + delta * indent
        if newIndentWidth < 0:
            newIndentWidth = 0
        return scimozindent.makeIndentFromWidth(scimoz, newIndentWidth)

    def _doKeyPressHere(self, ch, scimoz, style_info):
        # Returns either None or an indent string
        pos = scimoz.positionBefore(scimoz.currentPos)
        startPos = scimoz.currentPos
        if startPos < 5:
            return None
        style = scimoz.getStyleAt(pos)
        if style != scimoz.SCE_UDL_TPL_OPERATOR:
            return None
        if scimoz.getWCharAt(pos) != "]":
            return None
        pos -= 1
        style = scimoz.getStyleAt(pos)
        if style != scimoz.SCE_UDL_TPL_OPERATOR:
            return None
        if scimoz.getWCharAt(pos) != "%":
            return None
        pos -= 1
        curLineNo = scimoz.lineFromPosition(pos)
        lineStartPos = scimoz.positionFromLine(curLineNo)
        delta, numTags = self._getTagDiffDelta(scimoz, lineStartPos, startPos)
        if delta < 0 and numTags == 1 and curLineNo > 0:
            didDedent, dedentAmt = self.dedentThisLine(scimoz, curLineNo, startPos)
            if didDedent:
                return dedentAmt
        return None

    def _getTagDiffDelta(self, scimoz, lineStartPos, startPos):
        data = scimoz.getStyledText(lineStartPos, startPos)
        chars = data[0::2]
        styles = [ord(x) for x in data[1::2]]
        lim = len(styles)
        delta = 0
        numTags = 0
        i = 0
        limSub1 = lim - 1
        sawSlash = False
        while i < limSub1:
            if styles[i] == scimoz.SCE_UDL_TPL_OPERATOR and chars[i] == '[':
                i += 1
                if styles[i] != scimoz.SCE_UDL_TPL_OPERATOR or chars[i] != '%':
                    i += 1
                    continue
                i += 1
                if styles[i] == scimoz.SCE_UDL_TPL_OPERATOR and chars[i] == '-':
                    i += 1
                while (i < lim
                       and styles[i] == scimoz.SCE_UDL_TPL_DEFAULT):
                    i += 1
                if styles[i] != scimoz.SCE_UDL_TPL_WORD:
                    continue
                wordStart = i
                while (i < lim
                       and styles[i] == scimoz.SCE_UDL_TPL_WORD):
                    i += 1
                word = chars[wordStart:i]
                if word in self._startWords:
                    numTags += 1
                    delta += 1
                elif word == "END":
                    numTags += 1
                    delta -= 1
            else:
                i += 1
        return delta, numTags

class KoTemplateToolkitLinter(object):
    _com_interfaces_ = [components.interfaces.koILinter]
    _reg_desc_ = "TemplateToolkit Template Linter"
    _reg_clsid_ = "{72b2df05-86c4-428b-b6bd-27a4f6495806}"
    _reg_contractid_ = "@activestate.com/koLinter?language=TemplateToolkit;1"
    _reg_categories_ = [
        ("category-komodo-linter", 'TemplateToolkit'),
    ]


    def __init__(self):
        self._koLintService = components.classes["@activestate.com/koLintService;1"].getService(components.interfaces.koILintService)
        self._perl_linter = None
        self._html_linter = UnwrapObject(self._koLintService.getLinterForLanguage("HTML"))
        
    @property
    def perl_linter(self):
        if self._perl_linter is None:
            self._perl_linter = UnwrapObject(self._koLintService.getLinterForLanguage("Perl"))
        return self._perl_linter
        
    _ttktMatcher = re.compile(r'''(
         (?:\[%\s+PERL\s+%\].*?\[%\s+END\s+%\])
        |[^\[]+ 
        |.)''',                  # Catchall
        re.VERBOSE|re.DOTALL)
    
    _exprTagRE = re.compile(r'(\[%\s*\w+.*%\])', re.DOTALL)
    _perlTagRE = re.compile(r'(\[%\s+PERL\s+%\])(.*?)(\[%\s+END\s+%\])', re.DOTALL)
    def _stripInnerPart(self, m):
        return self._spaceOutNonNewlines(m.group(1))

    def _fixPerlPart(self, text):
        parts = self._ttktMatcher.findall(text)
        if not parts:
            return ""
        i = 0
        lim = len(parts)
        perlTextParts = []
        while i < lim:
            part = parts[i]
            if part.startswith("[") and len(part) > 1:
                m = self._perlTagRE.match(part)
                if m:
                    fixedPart = (self._spaceOutNonNewlines(m.group(1))
                                 + self._exprTagRE.sub(self._stripInnerPart, m.group(2))
                                 + self._spaceOutNonNewlines(m.group(3)))
                else:
                    log.warn("Thought this would match a perl tag, but no")
                    fixedPart = self._spaceOutNonNewlines(part)
            else:
                fixedPart = self._spaceOutNonNewlines(part)
            perlTextParts.append(fixedPart)
            i += 1
        return "".join(perlTextParts)

    _nonNewlineMatcher = re.compile(r'[^\r\n]')
    def _spaceOutNonNewlines(self, markup):
        return self._nonNewlineMatcher.sub(' ', markup)

    _tplPatterns = ("TemplateToolkit", re.compile(r'\[%\s*(?![A-Z])'), re.compile(r'%\]\s*\Z', re.DOTALL))
    def lint(self, request):
        return self._html_linter.lint(request,
                                      udlMapping={"Perl":"TemplateToolkit"},
                                      TPLInfo=self._tplPatterns)

    def lint_with_text(self, request, text):
        perlText = self._fixPerlPart(text)
        if not perlText.strip():
            return
        return self.perl_linter.lint_with_text(request, perlText)
