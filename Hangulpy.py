#!/usr/bin/env python
# encoding: utf-8
"""
Hangul.py

Copyright (C) 2012 Ryan Rho

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

# Code = 0xAC00 + (Chosung_index * NUM_JOONGSUNGS * NUM_JONGSUNGS) + (Joongsung_index * NUM_JONGSUNGS) + (Jongsung_index)
class Hangulpy:
    CHOSUNGS = [u'ㄱ',u'ㄲ',u'ㄴ',u'ㄷ',u'ㄸ',u'ㄹ',u'ㅁ',u'ㅂ',u'ㅃ',u'ㅅ',u'ㅆ',u'ㅇ',u'ㅈ',u'ㅉ',u'ㅊ',u'ㅋ',u'ㅌ',u'ㅍ',u'ㅎ']
    JOONGSUNGS = [u'ㅏ',u'ㅐ',u'ㅑ',u'ㅒ',u'ㅓ',u'ㅔ',u'ㅕ',u'ㅖ',u'ㅗ',u'ㅘ',u'ㅙ',u'ㅚ',u'ㅛ',u'ㅜ',u'ㅝ',u'ㅞ',u'ㅟ',u'ㅠ',u'ㅡ',u'ㅢ',u'ㅣ']
    JONGSUNGS = [u'',u'ㄱ',u'ㄲ',u'ㄳ',u'ㄴ',u'ㄵ',u'ㄶ',u'ㄷ',u'ㄹ',u'ㄺ',u'ㄻ',u'ㄼ',u'ㄽ',u'ㄾ',u'ㄿ',u'ㅀ',u'ㅁ',u'ㅂ',u'ㅄ',u'ㅅ',u'ㅆ',u'ㅇ',u'ㅈ',u'ㅊ',u'ㅋ',u'ㅌ',u'ㅍ',u'ㅎ']
    
    NUM_CHOSUNGS = 19
    NUM_JOONGSUNGS = 21
    NUM_JONGSUNGS = 28
    
    FIRST_HANGUL_UNICODE = 0xAC00 #'가'
    LAST_HANGUL_UNICODE = 0xD7A3 #'힣'

    def __init__(self, phrase):
        pass

    @staticmethod
    def is_hangul(phrase):
        """Check whether the phrase is Hangul.
        This method ignores white spaces, punctuations, and numbers.
        @param phrase a target string
        @return True if the phrase is Hangul. False otherwise."""
        
        # Remove all white spaces, punctuations, numbers.
        exclude = set(string.whitespace + string.punctuation + '0123456789')
        phrase = ''.join(ch for ch in phrase if ch not in exclude)
        
        for unicode_value in map(lambda letter:ord(letter), phrase):
            if unicode_value < Hangulpy.FIRST_HANGUL_UNICODE or unicode_value > Hangulpy.LAST_HANGUL_UNICODE:
                return False

        return True
    
    @staticmethod
    def has_jongsung(letter):
        """Check whether this letter contains JongSung"""
        if len(letter) != 1:
            raise Exception('The target string must be one letter.')
        if not Hangulpy.is_hangul(letter):
            raise NotHangulException('The target string must be Hangul')

        unicode_value = ord(letter)
        return (unicode_value - Hangulpy.FIRST_HANGUL_UNICODE) % Hangulpy.NUM_JONGSUNGS > 0
    
    @staticmethod
    def has_batchim(letter):
        """This method is the same as has_jongsung()"""
        return Hangulpy.has_jongsung(letter)
    
    @staticmethod
    def josa_en(word):
        """add josa either '은' or '는' at the end of this word"""
        word = word.strip()
        last_letter = word[-1]
        if not Hangulpy.is_hangul: raise NotHangulException('')
        
        josa = u'은' if Hangulpy.has_jongsung(last_letter) else u'는'
        return word + josa
    
    @staticmethod
    def josa_eg(word):
        """add josa either '이' or '가' at the end of this word"""
        word = word.strip()
        last_letter = word[-1]
        if not Hangulpy.is_hangul: raise NotHangulException('')
        
        josa = u'이' if Hangulpy.has_jongsung(last_letter) else u'가'
        return word + josa

    @staticmethod
    def josa_el(word):
        """add josa either '을' or '를' at the end of this word"""
        word = word.strip()
        last_letter = word[-1]
        if not Hangulpy.is_hangul: raise NotHangulException('')
        
        josa = u'을' if Hangulpy.has_jongsung(last_letter) else u'를'
        return word + josa

################################################################################
# Exceptions
################################################################################

class NotHangulException(Exception):
    pass

class NotWordException(Exception):
    pass

################################################################################
# title
################################################################################

if __name__ == '__main__':
    print 'Hangul Module'