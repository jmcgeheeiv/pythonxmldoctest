# Test XML Output Using Python doctest

Python doctest combines unit testing with documentation.  With doctest, you put your
unit tests in the Python docstring, and documentation generators like
[Sphinx](http://sphinx-doc.org/) render your tests as usage examples.  It’s easy to
compare a method’s output to an XML string using doctest.  It’s not so easy when you
want the XML string pretty-printed for the sake of readable documentation.  Here is a
simple solution.

## Background: doctest wants the XML on a single line

Consider this sample that creates an XML document. If you use doctest to test against the
result of `toxml()` in the docstring, the expected result must appear all on one line,
which is satisfactory for only the shortest XML element:

    import datetime
    import getpass
    from xml.dom.minidom import Document

    class PythonXmlDoctest(object):
        '''Example of testing XML output using Python doctest.'''

        def __init__(self, contentText):
            ''' Create an ultra-super-mega great document.

            >>> d = PythonXmlDoctest('Somebody stop me!')
            >>> d.doc.toxml()   #doctest: +ELLIPSIS
            '<?xml version="1.0" ?><super><ultra date="..." user="..."><mega>Somebody stop me!</mega></ultra></super>'
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

    if __name__ == "__main__":
        import doctest
        doctest.testmod()

The doctest `ELLIPSIS` option allows me to specify `...` for the `date` and `user` attribute values so
that the test will succeed any time for any user.

## Solution: pretty print with spaces and normalize white space

I get the best result using `toprettyxml(indent=' ', newl=' ')` together with the doctest `NORMALIZE_WHITESPACE`
option. The key to understanding `NORMALIZE_WHITESPACE` is that it causes all sequences of one or more
(but not zero) white space characters to be considered equivalent:

    def __init__(self, contentText):
        ''' Create an ultra-super-mega great document.
        
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
        # Code for __init() continues...

The expected result in the above docstring is easily readable, and the test passes.  Moreover, when rendered as documentation using [Sphinx](http://sphinx-doc.org/), the XML expected result appears as a nicely formatted usage example.

## If your XML package has no pretty print

If you are using another Python XML package like [ElementTree](http://docs.python.org/library/xml.etree.elementtree.html) that cannot pretty print, just [read the XML into minidom and output it again pretty printed](http://www.doughellmann.com/PyMOTW/xml/etree/ElementTree/create.html):

    from xml.etree import ElementTree
    from xml.dom import minidom
    def prettify(elem):
        """Return a pretty-printed XML string for the Element."""
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent=' ', newl=' ')

## Use a raw docstring if you have lots of backslashes

When your docstring is an ordinary string, you must use a double backslash even in raw strings within your test.
This is particularly tiresome with Windows file paths:

     def test_backslash1():
    '''Two backslashes needed in the docstring tests:

    >>> r’\\windows\\filename.txt’ == test_backslash1()
    True
    '''
    return r’\windows\filename.txt’

If you make the docstring itself a raw sting by starting it with `r'''`, you can use a single backslash:

    def test_backslash2():
    r'''Two backslashes not required because this docstring is itself a raw string:

    >>> r’\windows\filename.txt’ == test_backslash2()
    True
    '''
    return r’\windows\filename.txt’
