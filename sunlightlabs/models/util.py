#import AsciiDammit
import re

map_chars = {u'&deg;': u' degree',
             u'&eacute;': u'e',
             u'&frasl;': u'bkslsh',
             u'&lsquo;': u"'",
             u'&lt;': u" lt ",
             u'&mdash;': u"-",
             u'&Ocirc;': u"O",
             u'&Otilde;': u"O",
             u'&pound;': u"pounds ",
             u'&#8226;': u"",
             u'\xc2\x97': u'-',
             u'\xc2\x91': u"'",
             u'\xc2\x92': u"'",
             u'\xc2\x93': u'"',
             u'\xc2\x94': u'"',
             u'\xe2\x80\x98': u"'",
             u'\xe2\x80\x99': u"'",
             u'\xe2\x80\x9a': u"'",
             u'\xe2\x80\x9b': u"'",
             u'\xe2\x80\x9c': u'"',
             u'\xe2\x80\x9d': u'"',
             u'\xe2\x80\x9f': u'"',
             u'\xe2\x80\x9e': u'"',
             u'\x60\x60': u'"',
             u'/': u'',
             u'<': u'',
             #u'\u2028': u' ',
             #u'\u2026': u' ',
             #u'\u2014': u' ',
             #u'\u2122': u' trademark ',
             #u'\u2022': u'-',
             u'\xa0': u' ',
             #u'\xfc': u'u',
             #u'\xf3': u'o',
             #u'\xe1': u'a',
             #u'\xe0': u'a',
             #u'\xe9': u'e',
             #u'\xef': u'i',
             #u'\xb5': u' ',
             #u'\xb6': u' ',
             #u'\xb7': u' dividedby ',
             #u'\xa7': u' ',
             #u'\xa9': u' copyright ',
             #u'\u0cb5': u' copyright ',
             #u'\u2018': "'",
             #u'\u2010': "-",
             #u'\u2014': '-',
             #u'\u2013': '-',
             u'\u00A0': u' ',
             u'\u201c': u'"',
             u'\u201d': u'"',
             u'\u2019': u"'",
             u'\t': u' '}


def clean_text(text):
    for s, r in map_chars.iteritems():
        _text = text.replace(s, r)
    _text = re.sub(r'(https?|ftp):\/\/[^\s]+', ' ', _text)
    _text = re.sub(r'(&[A-Za-z0-9#]+;)+|\s\s+', ' ', _text)
    #return AsciiDammit.asciiDammit(text)
    return _text
