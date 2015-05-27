"""
Author: Willians Costa da Silva
Email: willianscsilva@gmail.com
License: GNU General Public License version 2.0 (GPLv2) - http://www.gnu.org/licenses/gpl-2.0.html
Created: 2013-03-23
Credits & Source:
- http://python.org/
Note: Copy, distribute, modify freely, but keep the credits, please.
"""
import re,sys

class pfp_regex:
    
    def preg_match(self,pattern,_str):
        try:
            result = False
            pattern_compile = re.compile(pattern)
            result = re.search(pattern_compile,_str)
            return result
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        
    
    def preg_match_all(self,pattern,_str):
        try:
            result = False
            pattern_compile = re.compile(pattern)
            result = re.findall(pattern_compile,_str)
            return result
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
            
    def preg_replace(self,pattern_search,replacement,_str):
        try:
            type_search = type(pattern_search)
            type_replace = type(replacement)
            
            if type_search == list and type_replace == list:
                    if len(pattern_search) == len(replacement):
                            i=0
                            for values in pattern_search:
                                    pattern = re.compile(values)                                    
                                    _str = pattern.sub(replacement[i],_str)
                                    i+=1
                    else:
                        print "Length Error: pattern_search and replacement must have the same size"
            elif type_search == list and type_replace == str:
                    for values in pattern_search:
                            pattern = re.compile(values)
                            _str = pattern.sub(replacement,_str)
            else:                
                pattern = re.compile(pattern_search)
                _str = pattern.sub(replacement,_str)
            return _str
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise    
