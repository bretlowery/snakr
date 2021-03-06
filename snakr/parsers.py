'''
Parser contains methods to open the resource located at the long URL target and extract metadata such as document title
for return in the JSON data with the short URL.
'''
import urllib2
import bs4
import mimetypes
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from PyOpenGraph import PyOpenGraph
from utilities import Utils
from StringIO import StringIO

class Parsers():

    def __init__(self):
        return

    def _get_pdf_title(self, documenturl):
        title = None
        try:
            pdf = PDFDocument(PDFParser(StringIO(urllib2.urlopen(documenturl).read())))
            title = Utils.remove_nonascii(pdf.info[0]["Title"]).strip()
            if not title:
                title = Utils.remove_nonascii(pdf.info[0]["Subject"]).strip()
            if len(title) < 1:
                title = None
        except:
            pass
        return title

    def get_title(self, documenturl):
        rtn = None
        mime_type = None
        docurl = None
        try:
            docurl = urllib2.urlopen(documenturl)
        except urllib2.HTTPError as e:
            raise Exception('HTTPError %s: %s' % (e.code, e.reason))
        else:
            pass
        if docurl:
            try:
                mime_type = mimetypes.guess_type(documenturl, strict=True)[0]
            except:
                pass
            if mime_type:
                def mt(x):
                    return {
                        'application/pdf': self._get_pdf_title(documenturl),
                        }.get(x, None)
                rtn = mt(mime_type)
            if not mime_type or not rtn:
                doc_supports_og = False
                try:
                    ogdoc = PyOpenGraph.PyOpenGraph(documenturl)
                    doc_supports_og = ogdoc.is_valid()
                except:
                    pass
                if doc_supports_og:
                    rtn = ogdoc.metadata['title']
                if not rtn:
                    doctype = None
                    try:
                        soup = bs4.BeautifulSoup(docurl, "html.parser")
                        items = [item for item in soup if isinstance(item, bs4.Doctype)]
                        doctype = items[0].string if items else None
                    except:
                        pass
                    if doctype:
                        def dt(x):
                            return {
                                u'html': soup.title.string,
                                u'doctype html': soup.title.string,
                                }.get(x, None)
                        rtn = dt(doctype)
        if rtn is None:
            return None
        else:
            return rtn.decode('utf8').strip()

