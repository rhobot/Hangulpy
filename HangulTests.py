#!/usr/bin/env python
# encoding: utf-8
"""
HangulTests.py

Created by Ryan Rho on 2012-01-07.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import unittest
from Hangulpy import *

class HangulTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_is_hangul(self):
        hangul_letters = u'가나다라힣뷁'
        other_letters = u'@%漢字かんじhán tự'
        non_unicode_letters = 'abcdez$%^&* '
        
        for letter in hangul_letters:
            self.assertTrue(Hangulpy.is_hangul(letter))
        
        for letter in other_letters:
            self.assertFalse(Hangulpy.is_hangul(letter))
        
        for letter in non_unicode_letters:
            self.assertFalse(Hangulpy.is_hangul(letter))
    
    def test_has_jongsung(self):
        jongsung_letters = u'강줽뷁'
        non_jongsung_letters = u'가너댜봬쉐'
        
        for letter in jongsung_letters:
            self.assertTrue(Hangulpy.has_jongsung(letter))
        
        for letter in non_jongsung_letters:
            self.assertFalse(Hangulpy.has_jongsung(letter))
    

    
if __name__ == '__main__':
    unittest.main()