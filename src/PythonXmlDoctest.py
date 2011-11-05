#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# Copyright 2011 Voom, Inc.
#
# This file is part of the Voom Python XML Doctest Example.
# See http://www.voom.net/test-xml-using-python-doctest/ for documentation.
#
# Python XML Doctest Example is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Python XML Doctest Example is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Python XML Doctest Example.  If not, see <http://www.gnu.org/licenses/>.

"""
Example of testing XML output using Python doctest.
"""

__author__ = "John McGehee, http://www.voom.net/"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2011/11/05 $"
__copyright__ = "Copyright 2011 Voom, Inc."

import datetime
import getpass
from xml.dom.minidom import Document

class PythonXmlDoctest(object):
    '''Example of testing XML output using Python doctest.'''
    
    def __init__(self, contentText):
        ''' Create an ultra-super-mega great document.
        
        If you test this using toxml(), the expected result must appear all on
        one line, which is satisfactory for only for the shortest XML element:
        
        >>> d = PythonXmlDoctest('Somebody stop me!')
        >>> d.doc.toxml()   #doctest: +ELLIPSIS
        '<?xml version="1.0" ?><super><ultra date="..." user="..."><mega>Somebody stop me!</mega></ultra></super>'
        
        Note how I used the doctest ELLIPSIS option. It allows me to
        specify ... for the date and user attribute values so that the test
        will succeed no matter who you are and when you run the test.

        Using toprettyxml() is even worse because the expected result contains \\n
        and \\t, and it's still on one line:
             
        >>> d = PythonXmlDoctest('Somebody stop me!')
        >>> d.doc.toprettyxml()   #doctest: +ELLIPSIS
        '<?xml version="1.0" ?>\\n<super>\\n\\t<ultra date="2011-11-05" user="johnm">\\n\\t\\t<mega>\\n\\t\\t\\tSomebody stop me!\\n\\t\\t</mega>\\n\\t</ultra>\\n</super>\\n'
        
        I got the best result using toprettyxml(indent=' ', newl=' ') together
        with the doctest NORMALIZE_WHITESPACE option:
        
        >>> d = PythonXmlDoctest('Somebody stop me!')
        >>> d.doc.toprettyxml(indent=' ', newl=' ')   #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        '<?xml version="1.0" ?>
        <super>
          <ultra date="..." user="...">
            <mega>
              Somebody stop me!
            </mega>
          </ultra>
        </super> '
        '''

        self._doc = Document()
        super = self._doc.createElement("super")
        self._doc.appendChild(super)
        
        ultra = self._doc.createElement("ultra")
        ultra.setAttribute('date', str(datetime.date.today()))
        ultra.setAttribute('user', getpass.getuser())
        super.appendChild(ultra)
        
        mega = self._doc.createElement("mega")
        ultra.appendChild(mega)
        content = self._doc.createTextNode(contentText)
        mega.appendChild(content)
        
    @property
    def doc(self):
        '''The minidom document.'''
        return self._doc
    
    def toDoctestXml(self):
        '''Return the XML formatted for comparison using doctest.

        >>> d = PythonXmlDoctest('Somebody stop me!')
        >>> d.toDoctestXml()   #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        '<?xml version="1.0" ?>
        <super>
          <ultra date="..." user="...">
            <mega>
              Somebody stop me!
            </mega>
          </ultra>
        </super> '
        '''
        return self._doc.toprettyxml(indent=' ', newl=' ')

if __name__ == "__main__":
    import doctest
    doctest.testmod()
