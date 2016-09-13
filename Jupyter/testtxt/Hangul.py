# -*- coding: utf-8 -*-
# encoding: utf-8
#
#  Hangul unicode syllabos decoding - encoding
#
#  @ modified becxer
#  @ e-mail becxer87@gmail.com
#

"""
Hangulpy.py
Copyright (C) 2016 Seohyun Back, Ryan Rho, Hyunwoo Cho
Text Decompose & Automata Extention by bluedisk@gmail
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import string,re
################################################################################
# Hangul Unicode Variables
################################################################################

# Code = 0xAC00 + (Chosung_index * NUM_JOONGSUNGS * NUM_JONGSUNGS) + (Joongsung_index * NUM_JONGSUNGS) + (Jongsung_index)
CHOSUNGS = [u'ㄱ',u'ㄲ',u'ㄴ',u'ㄷ',u'ㄸ',u'ㄹ',u'ㅁ',u'ㅂ',u'ㅃ',u'ㅅ',u'ㅆ',u'ㅇ',u'ㅈ',u'ㅉ',u'ㅊ',u'ㅋ',u'ㅌ',u'ㅍ',u'ㅎ']
JOONGSUNGS = [u'ㅏ',u'ㅐ',u'ㅑ',u'ㅒ',u'ㅓ',u'ㅔ',u'ㅕ',u'ㅖ',u'ㅗ',u'ㅘ',u'ㅙ',u'ㅚ',u'ㅛ',u'ㅜ',u'ㅝ',u'ㅞ',u'ㅟ',u'ㅠ',u'ㅡ',u'ㅢ',u'ㅣ']
JONGSUNGS = [u'',u'ㄱ',u'ㄲ',u'ㄳ',u'ㄴ',u'ㄵ',u'ㄶ',u'ㄷ',u'ㄹ',u'ㄺ',u'ㄻ',u'ㄼ',u'ㄽ',u'ㄾ',u'ㄿ',u'ㅀ',u'ㅁ',u'ㅂ',u'ㅄ',u'ㅅ',u'ㅆ',u'ㅇ',u'ㅈ',u'ㅊ',u'ㅋ',u'ㅌ',u'ㅍ',u'ㅎ']

# 코딩 효율과 가독성을 위해서 index대신 unicode사용 by bluedisk
JONG_COMP = {
    u'ㄱ':{
        u'ㄱ': u'ㄲ',
        u'ㅅ': u'ㄳ',
    },
    u'ㄴ':{
        u'ㅈ': u'ㄵ',
        u'ㅎ': u'ㄶ',
    },
    u'ㄹ':{
        u'ㄱ': u'ㄺ',
        u'ㅁ': u'ㄻ',
        u'ㅂ': u'ㄼ',
        u'ㅅ': u'ㄽ',
        u'ㅌ': u'ㄾ',
        u'ㅍ': u'ㄿ',
        u'ㅎ': u'ㅀ',
    }
}

NUM_CHOSUNGS = 19
NUM_JOONGSUNGS = 21
NUM_JONGSUNGS = 28

FIRST_HANGUL_UNICODE = 0xAC00 #'가'
LAST_HANGUL_UNICODE = 0xD7A3 #'힣'

# 한자와 라틴 문자 범위 by bluedisk
FIRST_HANJA_UNICODE = 0x4E00
LAST_HANJA_UNICODE = 0x9FFF

FIRST_HANJA_EXT_A_UNICODE = 0x3400
LAST_HANJA_EXT_A_UNICODE = 0x4DBF

FIRST_LATIN1_UNICODE = 0x0000 # NUL
LAST_LATIN1_UNICODE = 0x00FF # 'ÿ'

# EXT B~E 는 무시

################################################################################
# Hangul Automata functions by bluedisk@gmail.com
################################################################################
COMPOSE_CODE = u'ᴥ'

def decompose_text(text, latin_filter=True):
    result=u""

    for c in list(text):
        if is_hangul(c):

            result = result + "".join(decompose(c)) + COMPOSE_CODE

        else:
            if latin_filter:    # 한글 외엔 Latin1 범위까지만 포함 (한글+영어)
                if is_latin1(c):
                    result = result + c
            else:
                result = result + c

    return result

def compose_text(text):
    res_text = u""
    status="CHO"

    for c in text:

        if status == "CHO":

            if c in CHOSUNGS:
                chosung = c
                status="JOONG"
            else:
                if c != COMPOSE_CODE:

                    res_text = res_text + c

        elif status == "JOONG":

            if c != COMPOSE_CODE and c in JOONGSUNGS:
                joongsung = c
                status="JONG1"
            else:
                res_text = res_text + chosung

                if c in CHOSUNGS:
                    chosung = c
                    status="JOONG"
                else:
                    if c != COMPOSE_CODE:

                        res_text = res_text + c
                    status="CHO"

        elif status == "JONG1":

            if c != COMPOSE_CODE and c in JONGSUNGS:
                jongsung = c

                if c in JONG_COMP:
                    status="JONG2"
                else:
                    res_text = res_text + compose(chosung, joongsung, jongsung)
                    status="CHO"

            else:
                res_text = res_text + compose(chosung, joongsung)

                if c in CHOSUNGS:
                    chosung = c
                    status="JOONG"
                else:
                    if c != COMPOSE_CODE:

                        res_text = res_text + c

                    status="CHO"

        elif status == "JONG2":

            if c != COMPOSE_CODE and c in JONG_COMP[jongsung]:
                jongsung = JONG_COMP[jongsung][c]
                c = COMPOSE_CODE # 종성 재 출력 방지

            res_text = res_text + compose(chosung, joongsung, jongsung)

            if c != COMPOSE_CODE:

                res_text = res_text + c

            status="CHO"


    return res_text

################################################################################
# Boolean Hangul functions
################################################################################

def is_hangul(phrase):
    """Check whether the phrase is Hangul.
    This method ignores white spaces, punctuations, and numbers.
    @param phrase a target string
    @return True if the phrase is Hangul. False otherwise."""

    # If the input is only one character, test whether the character is Hangul.
    if len(phrase) == 1: return is_all_hangul(phrase)

    # Remove all white spaces, punctuations, numbers.
    exclude = set(string.whitespace + string.punctuation + '0123456789')
    phrase = ''.join(ch for ch in phrase if ch not in exclude)

    return is_all_hangul(phrase)

def is_all_hangul(phrase):
    """Check whether the phrase contains all Hangul letters
    @param phrase a target string
    @return True if the phrase only consists of Hangul. False otherwise."""

    for unicode_value in map(lambda letter:ord(letter), phrase):
        if unicode_value < FIRST_HANGUL_UNICODE or unicode_value > LAST_HANGUL_UNICODE:
            # Check whether the letter is chosungs, joongsungs, or jongsungs.
            if unicode_value not in map(lambda v: ord(v), CHOSUNGS + JOONGSUNGS + JONGSUNGS[1:]):
                return False
    return True

def remove_except_words(phrase):
    exclude = set(string.whitespace + string.punctuation + '0123456789')
    phrase = ''.join(ch if ch not in exclude else ' ' for ch in phrase)
    res = ''
    for unicode_value in map(lambda letter:ord(letter), phrase):
        if (unicode_value >= FIRST_HANGUL_UNICODE and unicode_value <= LAST_HANGUL_UNICODE) \
            or (unicode_value >= FIRST_LATIN1_UNICODE and unicode_value <= LAST_LATIN1_UNICODE):
            res += unichr(unicode_value)
    res = re.sub(' +',' ', res)
    return res
            
def is_hanja(phrase):
    for unicode_value in map(lambda letter:ord(letter), phrase):
        if ((unicode_value < FIRST_HANJA_UNICODE or unicode_value > LAST_HANJA_UNICODE) and
            (unicode_value < FIRST_HANJA_EXT_A_UNICODE or unicode_value > LAST_HANJA_EXT_A_UNICODE)):
            return False
    return True

def is_latin1(phrase):
    for unicode_value in map(lambda letter:ord(letter), phrase):
        if unicode_value < FIRST_LATIN1_UNICODE or unicode_value > LAST_LATIN1_UNICODE:
            return False
    return True

################################################################################
# Decomposition & Combination
################################################################################

def compose(chosung, joongsung, jongsung=u''):
    """This function returns a Hangul letter by composing the specified chosung, joongsung, and jongsung.
    @param chosung
    @param joongsung
    @param jongsung the terminal Hangul letter. This is optional if you do not need a jongsung."""

    if jongsung is None: jongsung = u''

    try:
        chosung_index = CHOSUNGS.index(chosung)
        joongsung_index = JOONGSUNGS.index(joongsung)
        jongsung_index = JONGSUNGS.index(jongsung)
    except Exception, e:
        raise NotHangulException('No valid Hangul character can be generated using given combination of chosung, joongsung, and jongsung.')

    return unichr(0xAC00 + chosung_index * NUM_JOONGSUNGS * NUM_JONGSUNGS + joongsung_index * NUM_JONGSUNGS + jongsung_index)

def decompose(hangul_letter):
    """This function returns letters by decomposing the specified Hangul letter."""

    if len(hangul_letter) < 1:
        raise NotLetterException('')
    elif not is_hangul(hangul_letter):
        raise NotHangulException('')

    code = ord(hangul_letter) - FIRST_HANGUL_UNICODE
    jongsung_index = code % NUM_JONGSUNGS
    code /= NUM_JONGSUNGS
    joongsung_index = code % NUM_JOONGSUNGS
    code /= NUM_JOONGSUNGS
    chosung_index = code

    if chosung_index < 0:
        chosung_index = 0

    try:
        return (CHOSUNGS[chosung_index], JOONGSUNGS[joongsung_index], JONGSUNGS[jongsung_index])
    except:
        print "%d / %d  / %d"%(chosung_index, joongsung_index, jongsung_index)
        print "%s / %s " %( (JOONGSUNGS[joongsung_index].encode("utf8"), JONGSUNGS[jongsung_index].encode('utf8')))
        raise Exception()
