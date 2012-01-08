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

import unittest

# Code = 0xAC00 + (Chosung_index * 21 * 28) + (Joongsung_index * 28) + (Jongsung_index)
class Hangulpy:
    CHO_SUNGS = [u'ㄱ',u'ㄲ',u'ㄴ',u'ㄷ',u'ㄸ',u'ㄹ',u'ㅁ',u'ㅂ',u'ㅃ',u'ㅅ',u'ㅆ',u'ㅇ',u'ㅈ',u'ㅉ',u'ㅊ',u'ㅋ',u'ㅌ',u'ㅍ',u'ㅎ']
    JOONG_SUNGS = [u'ㅏ',u'ㅐ',u'ㅑ',u'ㅒ',u'ㅓ',u'ㅔ',u'ㅕ',u'ㅖ',u'ㅗ',u'ㅘ',u'ㅙ',u'ㅚ',u'ㅛ',u'ㅜ',u'ㅝ',u'ㅞ',u'ㅟ',u'ㅠ',u'ㅡ',u'ㅢ',u'ㅣ']
    JONG_SUNGS = [u'',u'ㄱ',u'ㄲ',u'ㄳ',u'ㄴ',u'ㄵ',u'ㄶ',u'ㄷ',u'ㄹ',u'ㄺ',u'ㄻ',u'ㄼ',u'ㄽ',u'ㄾ',u'ㄿ',u'ㅀ',u'ㅁ',u'ㅂ',u'ㅄ',u'ㅅ',u'ㅆ',u'ㅇ',u'ㅈ',u'ㅊ',u'ㅋ',u'ㅌ',u'ㅍ',u'ㅎ']
    
    FIRST_HANGUL_CODE = 0xAC00 #'가'
    LAST_HANGUL_CODE = 0xD7A3 #'힣'

    def __init__(self, phrase):
        pass

    @staticmethod
    def is_hangul(letter):
        """
        Check whether the letter is Hangul
        @param letter A letter as a string
        @return True if the letter is Hangul. False otherwise.    
        """
        if len(letter) != 1:
            raise Exception('The target string must be one letter.')

        unicode_value = ord(letter)
        return unicode_value >= Hangulpy.FIRST_HANGUL_CODE and unicode_value <= Hangulpy.LAST_HANGUL_CODE
    
    @staticmethod
    def has_jongsung(letter):
        """Check whether this letter contains JongSung"""
        if len(letter) != 1:
            raise Exception('The target string must be one letter.')
        if not Hangulpy.is_hangul(letter):
            raise NotHangulException('The target string must be Hangul')
        
        unicode_value = ord(letter)
        num_jongsungs = len(Hangulpy.JONG_SUNGS)
        return (unicode_value - Hangulpy.FIRST_HANGUL_CODE) % num_jongsungs > 0
    
    @staticmethod
    def has_batchim(letter):
        return Hangulpy.has_jongsung(letter)

class NotHangulException(Exception):
    pass

if __name__ == '__main__':
    print 'Hangul Module'