#!/usr/bin/env python
# encoding: utf-8
"""
Hangulpy.py

Copyright (C) 2012 Ryan Rho, Hyunwoo Cho

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

import string

################################################################################
# Hangul Unicode Variables
################################################################################

# Code = 0xAC00 + (Chosung_index * NUM_JOONGSUNGS * NUM_JONGSUNGS) + (Joongsung_index * NUM_JONGSUNGS) + (Jongsung_index)
CHOSUNGS = [u'ㄱ',u'ㄲ',u'ㄴ',u'ㄷ',u'ㄸ',u'ㄹ',u'ㅁ',u'ㅂ',u'ㅃ',u'ㅅ',u'ㅆ',u'ㅇ',u'ㅈ',u'ㅉ',u'ㅊ',u'ㅋ',u'ㅌ',u'ㅍ',u'ㅎ']
JOONGSUNGS = [u'ㅏ',u'ㅐ',u'ㅑ',u'ㅒ',u'ㅓ',u'ㅔ',u'ㅕ',u'ㅖ',u'ㅗ',u'ㅘ',u'ㅙ',u'ㅚ',u'ㅛ',u'ㅜ',u'ㅝ',u'ㅞ',u'ㅟ',u'ㅠ',u'ㅡ',u'ㅢ',u'ㅣ']
JONGSUNGS = [u'',u'ㄱ',u'ㄲ',u'ㄳ',u'ㄴ',u'ㄵ',u'ㄶ',u'ㄷ',u'ㄹ',u'ㄺ',u'ㄻ',u'ㄼ',u'ㄽ',u'ㄾ',u'ㄿ',u'ㅀ',u'ㅁ',u'ㅂ',u'ㅄ',u'ㅅ',u'ㅆ',u'ㅇ',u'ㅈ',u'ㅊ',u'ㅋ',u'ㅌ',u'ㅍ',u'ㅎ']

NUM_CHOSUNGS = 19
NUM_JOONGSUNGS = 21
NUM_JONGSUNGS = 28

FIRST_HANGUL_UNICODE = 0xAC00 #'가'
LAST_HANGUL_UNICODE = 0xD7A3 #'힣'

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

def has_jongsung(letter):
    """Check whether this letter contains Jongsung"""
    if len(letter) != 1:
        raise Exception('The target string must be one letter.')
    if not is_hangul(letter):
        raise NotHangulException('The target string must be Hangul')

    unicode_value = ord(letter)
    return (unicode_value - FIRST_HANGUL_UNICODE) % NUM_JONGSUNGS > 0

def has_batchim(letter):
    """This method is the same as has_jongsung()"""
    return has_jongsung(letter)
    
def has_approximant(letter):
    """Approximant makes complex vowels, such as ones starting with y or w.
    In Korean there is a unique approximant euㅡ making uiㅢ, but ㅢ does not make many irregularities."""
    if len(letter) != 1:
        raise Exception('The target string must be one letter.')
    if not is_hangul(letter):
        raise NotHangulException('The target string must be Hangul')

    jaso = decompose(letter)
    diphthong = (2, 3, 6, 7, 9, 10, 12, 14, 15, 17)
    # [u'ㅑ',u'ㅒ',',u'ㅕ',u'ㅖ',u'ㅘ',u'ㅙ',u'ㅛ',u'ㅝ',u'ㅞ',u'ㅠ']
    # excluded 'ㅢ' because y- and w-based complex vowels are irregular.
    # vowels with umlauts (ㅐ, ㅔ, ㅚ, ㅟ) are not considered complex vowels.
    return jaso[1] in diphthong

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
    
    return (CHOSUNGS[chosung_index], JOONGSUNGS[joongsung_index], JONGSUNGS[jongsung_index])

################################################################################
# Josa functions
################################################################################

def josa_en(word):
    """add josa either '은' or '는' at the end of this word"""
    word = word.strip()
    if not is_hangul(word): raise NotHangulException('')
    
    last_letter = word[-1]
    josa = u'은' if has_jongsung(last_letter) else u'는'
    return word + josa

def josa_eg(word):
    """add josa either '이' or '가' at the end of this word"""
    word = word.strip()
    if not is_hangul(word): raise NotHangulException('')
    
    last_letter = word[-1]
    josa = u'이' if has_jongsung(last_letter) else u'가'
    return word + josa

def josa_el(word):
    """add josa either '을' or '를' at the end of this word"""
    word = word.strip()
    if not is_hangul(word): raise NotHangulException('')
    
    last_letter = word[-1]
    josa = u'을' if has_jongsung(last_letter) else u'를'
    return word + josa
    
def josa_ro(word):
    """add josa either '으로' or '로' at the end of this word"""
    word = word.strip()
    if not is_hangul(word): raise NotHangulException('')
    
    last_letter = word[-1]
    if not has_jongsung(last_letter):
        josa = u'로'
    elif (ord(last_letter) - FIRST_HANGUL_UNICODE) % NUM_JONGSUNGS == 9: # ㄹ
        josa = u'로'
    else:
        josa = u'으로'

    return word + josa
    
def josa_gwa(word):
    """add josa either '과' or '와' at the end of this word"""
    word = word.strip()
    if not is_hangul(word): raise NotHangulException('')
    
    last_letter = word[-1]
    josa = u'과' if has_jongsung(last_letter) else u'와'
    return word + josa
    
def josa_ida(word):
    """add josa either '이다' or '다' at the end of this word"""
    word = word.strip()
    if not is_hangul(word): raise NotHangulException('')
    
    last_letter = word[-1]
    josa = u'이다' if has_jongsung(last_letter) else u'다'
    return word + josa
    
################################################################################
# Prefixes and suffixes
# Practice area; need more organization
################################################################################

def add_ryul(word):
    """add suffix either '률' or '율' at the end of this word"""
    word = word.strip()
    if not is_hangul(word): raise NotHangulException('')
    
    last_letter = word[-1]
    if not has_jongsung(last_letter):
        ryul = u'율'
    elif (ord(last_letter) - FIRST_HANGUL_UNICODE) % NUM_JONGSUNGS == 4: # ㄴ
        ryul = u'율'
    else:
        ryul = u'률'
        
    return word + ryul
    
################################################################################
# The formatter, or ultimately, a template system
# Practice area; need more organization
################################################################################

def ili(word):
    """convert {가} or {이} to their correct respective particles automagically."""
    word = word.strip()
    if not is_hangul(word): raise NotHangulException('')
    
    last_letter = word[word.find(u'{가}')-1]
    word = word.replace(u'{가}', (u'이' if has_jongsung(last_letter) else u'가'))
    
    last_letter = word[word.find(u'{이}')-1]
    word = word.replace(u'{이}', (u'이' if has_jongsung(last_letter) else u'가'))
    return word

################################################################################
# Exceptions
################################################################################

class NotHangulException(Exception):
    pass

class NotLetterException(Exception):
    pass

class NotWordException(Exception):
    pass
