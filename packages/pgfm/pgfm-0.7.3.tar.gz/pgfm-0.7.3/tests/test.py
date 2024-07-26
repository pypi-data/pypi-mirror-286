
import unittest

import pgfm

import datetime
import io
import json
import urllib
import lxml
import lxml.etree

# ============================================================================

class TestApi(unittest.TestCase):

    class Lay:
        def __init__(self, *args):
            self.args = args
        def recset(self, data):
            return "rset", data

    class LayDesc:
        def __init__(self):
            self.slots = {}
        def laySlot(self, cls):
            try:
                res = self.slots[cls]
            except KeyError:
                res = self.slots[cls] = TestApi.LaySlot()
            return res

    class LaySlot:
        def __init__(self):
            self.key = None
            self.lay = None

    class Api(pgfm.Api):
        @classmethod
        def layKey(cls, data):
            return "layKey", data
        @staticmethod
        def layCls():
            return TestApi.Lay
            
    # layInf: without LayDesc, new.
    def testLay(self):
        with ReplLays() as repl:
            data = object()
            layInf = self.Api.layInf(data, None)
            self.assertIsInstance(layInf, self.Lay)
        self.assertIs(repl.lays["layKey", data], layInf)
            
    # layInf: without LayDesc, repeat, same data.
    def testLayRep(self):
        with ReplLays() as repl:
            data = object()
            lay1 = self.Api.layInf(data, None)
            lay2 = self.Api.layInf(data, None)
            self.assertIs(lay1, lay2)
        self.assertEqual(len(repl.lays), 1)

    # layInf: without LayDesc, repeat, diff data.
    def testLayRepDiff(self):
        with ReplLays() as repl:
            data1 = object()
            data2 = object()
            lay1 = self.Api.layInf(data1, None)
            lay2 = self.Api.layInf(data2, None)
            self.assertIsNot(lay1, lay2)
        self.assertEqual(len(repl.lays), 2)

    # layInf: with LayDesc, new.
    def testLayDesc(self):
        with ReplLays() as repl:
            data = object()
            layDesc = self.LayDesc()
            lay = self.Api.layInf(data, layDesc)
            self.assertIsInstance(lay, self.Lay)
            laySlot = layDesc.laySlot(self.Lay)
            self.assertIs(laySlot.lay, lay)
            self.assertEqual(laySlot.key, ("layKey", data))
        self.assertEqual(len(repl.lays), 0)
            
    # layInf: with LayDesc, repeat, same data.
    def testLayDescRep(self):
        with ReplLays() as repl:
            data = object()
            layDesc = self.LayDesc()
            lay1 = self.Api.layInf(data, layDesc)
            lay2 = self.Api.layInf(data, layDesc)
            self.assertIs(lay1, lay2)
        self.assertEqual(len(repl.lays), 0)

    # layInf: with LayDesc, repeat, diff data.
    def testLayDescRepDiff(self):
        with ReplLays() as repl:
            data1 = object()
            data2 = object()
            layDesc = self.LayDesc()
            lay1 = self.Api.layInf(data1, layDesc)
            lay2 = self.Api.layInf(data2, layDesc)
            self.assertIsNot(lay1, lay2)
            laySlot = layDesc.laySlot(self.Lay)
            self.assertIs(laySlot.lay, lay2)
            self.assertEqual(laySlot.key, ("layKey", data2))

    # recset
    def testRecset(self):
        with ReplLays() as repl:
            data = object()
            rset = self.Api.recset(data, None)
            self.assertEqual(rset, ("rset", data))

# ============================================================================

class TestApiData(unittest.TestCase):

    # red
    def testData(self):
        res = pgfm.ApiData.read(b'{"abc":"def"}')
        self.assertEqual(res, {"abc":"def"})

# ============================================================================

class TestApiData1(unittest.TestCase):

    # Ver
    def testVer(self):
        self.assertEqual(pgfm.ApiData1.Ver, "v1")

# ============================================================================

class TestApiData2(unittest.TestCase):

    # Ver
    def testVer(self):
        self.assertEqual(pgfm.ApiData2.Ver, "v2")

# ============================================================================

class TestApiDataLatest(unittest.TestCase):

    # Ver
    def testVer(self):
        self.assertEqual(pgfm.ApiDataLatest.Ver, "vLatest")

# ============================================================================

class TestApiXml(unittest.TestCase):
    
    # Xp
    def testXp(self):
        xp = pgfm.ApiXml.Xp("abc/def")
        self.assertIsInstance(xp, lxml.etree.XPath)

    # Jc: F
    def testJc(self):
        jc = pgfm.ApiXml.Jc("F", "TEST")
        self.assertIsInstance(jc, str)
        self.assertEqual(jc, "{http://www.filemaker.com/fmpxmlresult}TEST")

    # Jc: L
    def testJc(self):
        jc = pgfm.ApiXml.Jc("L", "TEST")
        self.assertIsInstance(jc, str)
        self.assertEqual(jc, "{http://www.filemaker.com/fmpxmllayout}TEST")

    # Jc: f
    def testJc(self):
        jc = pgfm.ApiXml.Jc("f", "test")
        self.assertIsInstance(jc, str)
        self.assertEqual(jc, "{http://www.filemaker.com/xml/fmresultset}test")

    # read
    def testRead(self):
        data = b"<abc/>"
        res = pgfm.ApiXml.read(data)
        self.assertIsInstance(res, lxml.etree._Element)

    class ApiXmlSub(pgfm.ApiXml):
        @classmethod
        def XpError(cls, data):
            return [123] # with XPath we get a list.

    # error
    def testError(self):
        data = object()
        res = self.ApiXmlSub.error(data)
        self.assertEqual(res, (123, None))

# ============================================================================

class TestApiXmlLay(unittest.TestCase):

    # Ver
    def testVer(self):
        self.assertEqual(pgfm.ApiXmlLay.Ver, "FMPXMLLAYOUT")

    # Tag
    def testTg(self):
        self.assertEqual(pgfm.ApiXmlLay.Tag, 
                "{http://www.filemaker.com/fmpxmllayout}FMPXMLLAYOUT")

    XmlXpError = lxml.etree.fromstring(b"""
      <FMPXMLLAYOUT xmlns="http://www.filemaker.com/fmpxmllayout">
        <ERRORCODE>0</ERRORCODE>
      </FMPXMLLAYOUT>""")

    # XpError
    def testXpError(self):
        res, = pgfm.ApiXmlLay.XpError(self.XmlXpError)
        self.assertEqual(res, "0")

    # rtyp
    def testRtyp(self):
        data = object()
        res = pgfm.ApiXmlLay.rtyp(data)
        self.assertEqual(res, "layFmt")

    # layFmt
    # TODO

# ============================================================================

class TestApiXmlNew(unittest.TestCase):
    
    # Ver
    def testVer(self):
        self.assertEqual(pgfm.ApiXmlNew.Ver, "fmresultset")

    # Tag
    def testTag(self):
        self.assertEqual(pgfm.ApiXmlNew.Tag, 
                "{http://www.filemaker.com/xml/fmresultset}fmresultset")

    XmlXpError = lxml.etree.fromstring(b"""
      <fmresultset xmlns="http://www.filemaker.com/xml/fmresultset">
        <error code="0"/>
      </fmresultset>""")

    # XpError
    def testXpError(self):
        res, = pgfm.ApiXmlNew.XpError(self.XmlXpError)
        self.assertEqual(res, "0")

    XmlXpLayName = lxml.etree.fromstring(b"""
      <fmresultset xmlns="http://www.filemaker.com/xml/fmresultset">
        <datasource layout="Lay"/>
      </fmresultset>""")

    # XpLayName
    def testXpLayName(self):
        res, = pgfm.ApiXmlNew.XpLayName(self.XmlXpLayName)
        self.assertEqual(res, "Lay")

    XmlXpFnams = lxml.etree.fromstring(b"""
      <fmresultset xmlns="http://www.filemaker.com/xml/fmresultset">
        <metadata>
          <field-definition name="A" />
          <field-definition name="B" />
        </metadata>
      </fmresultset>""")

    # XpFnams
    def testXpFnams(self):
        res = pgfm.ApiXmlNew.XpFnams(self.XmlXpFnams)
        self.assertEqual(res, ["A", "B"])

    XmlXpNumRecs = lxml.etree.fromstring(b"""
      <fmresultset xmlns="http://www.filemaker.com/xml/fmresultset">
        <resultset fetch-size="2" />
      </fmresultset>""")

    # XpNumRecs
    def testXpNumRecs(self):
        res = pgfm.ApiXmlNew.XpNumRecs(self.XmlXpNumRecs)
        self.assertEqual(res, 2)

    XmlXpLayKey = lxml.etree.fromstring(b"""
      <fmresultset xmlns="http://www.filemaker.com/xml/fmresultset">
        <metadata />
      </fmresultset>""")

    # XpLayKey
    def testXpLayKey(self):
        res, = pgfm.ApiXmlNew.XpLayKey(self.XmlXpLayKey)
        self.assertEqual(res.tag, 
                "{http://www.filemaker.com/xml/fmresultset}metadata")

    XmlXpNames = lxml.etree.fromstring(b"""
      <fmresultset xmlns="http://www.filemaker.com/xml/fmresultset">
        <resultset>
          <record>
            <field>
              <data>A</data>
            </field>
          </record>
          <record>
            <field>
              <data>B</data>
            </field>
          </record>
          <record>
            <field>
              <data></data>
            </field>
          </record>
        </resultset>
      </fmresultset>""")

    # XpNames
    def testXpNames(self):
        res = pgfm.ApiXmlNew.XpNames(self.XmlXpNames)
        self.assertEqual(res, ["A", "B"])

    # layCls
    def testLayCls(self):
        self.assertIs(pgfm.ApiXmlNew.layCls(), pgfm.LaySpecXapiNew)

# ============================================================================

class TestApiXmlOld(unittest.TestCase):
    
    # Ver
    def testVer(self):
        self.assertEqual(pgfm.ApiXmlOld.Ver, "FMPXMLRESULT")

    # Tag
    def testTag(self):
        self.assertEqual(pgfm.ApiXmlOld.Tag, 
                "{http://www.filemaker.com/fmpxmlresult}FMPXMLRESULT")

    XmlXpError = lxml.etree.fromstring(b"""
      <FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
        <ERRORCODE>0</ERRORCODE>
      </FMPXMLRESULT>""")

    # XpError
    def testXpError(self):
        res, = pgfm.ApiXmlOld.XpError(self.XmlXpError)
        self.assertEqual(res, "0")

    XmlXpLayName = lxml.etree.fromstring(b"""
      <FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
        <DATABASE LAYOUT="Lay" />
      </FMPXMLRESULT>""")

    # XpLayName
    def testXpLayName(self):
        res, = pgfm.ApiXmlOld.XpLayName(self.XmlXpLayName)
        self.assertEqual(res, "Lay")

    XmlXpFnams = lxml.etree.fromstring(b"""
      <FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
        <METADATA>
          <FIELD NAME="A" />
          <FIELD NAME="B" />
        </METADATA>
      </FMPXMLRESULT>""")

    # XpFnams
    def testXpFnams(self):
        res = pgfm.ApiXmlOld.XpFnams(self.XmlXpFnams)
        self.assertEqual(res, ["A", "B"])

    XmlXpNumRecs = lxml.etree.fromstring(b"""
      <FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
        <RESULTSET>
          <ROW />
          <ROW />
        </RESULTSET>
      </FMPXMLRESULT>""")

    # XpNumRecs
    def testXpNumRecs(self):
        res = pgfm.ApiXmlOld.XpNumRecs(self.XmlXpNumRecs)
        self.assertEqual(res, 2)

    XmlXpLayKey = lxml.etree.fromstring(b"""
      <FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
        <METADATA />
      </FMPXMLRESULT>""")

    # XpLayKey
    def testXpLayKey(self):
        res, = pgfm.ApiXmlOld.XpLayKey(self.XmlXpLayKey)
        self.assertEqual(res.tag, 
                "{http://www.filemaker.com/fmpxmlresult}METADATA")

    XmlXpNames = lxml.etree.fromstring(b"""
      <FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
        <RESULTSET>
          <ROW>
            <COL>
              <DATA>A</DATA>
            </COL>
          </ROW>
          <ROW>
            <COL>
              <DATA>B</DATA>
            </COL>
          </ROW>
          <ROW>
            <COL>
              <DATA></DATA>
            </COL>
          </ROW>
        </RESULTSET>
      </FMPXMLRESULT>""")

    # XpNames
    def testXpNames(self):
        res = pgfm.ApiXmlOld.XpNames(self.XmlXpNames)
        self.assertEqual(res, ["A", "B"])

    # layCls
    def testLayCls(self):
        self.assertIs(pgfm.ApiXmlOld.layCls(), pgfm.LaySpecXapiOld)

# ============================================================================

class TestApiXmlRset(unittest.TestCase):
    
    # When guessing result type from data the code inspects the received XML.
    # It only checks specific attributes and thus we could create trimmed down 
    # samples that only have those bits, but why to do that when we already 
    # have representative samples of all result types? So we use those samples
    # instead.

    class ApiXmlRsetSub1(pgfm.ApiXmlRset):
        @classmethod
        def XpLayName(cls, xml):
            return xml.xpath("@l")
        @classmethod
        def XpNumRecs(cls, xml):
            return xml.xpath("number(@n)")
        @classmethod
        def XpFnams(cls, xml):
            return xml.xpath("f/@n")
    
    # rtyp: srvDbs
    def testRtypSrvDbs(self):
        dat = b"<r l=''><f n='DATABASE_NAME'/></r>"
        xml = lxml.etree.fromstring(dat)
        rtyp = self.ApiXmlRsetSub1.rtyp(xml)
        self.assertEqual(rtyp, "srvDbs")
        
    # rtyp: dbLays
    def testRtypDbLays(self):
        dat = b"<r l=''><f n='LAYOUT_NAME'/></r>"
        xml = lxml.etree.fromstring(dat)
        rtyp = self.ApiXmlRsetSub1.rtyp(xml)
        self.assertEqual(rtyp, "dbLays")

    # rtyp: dbScrs
    def testRtypDbScrs(self):
        dat = b"<r l=''><f n='SCRIPT_NAME'/></r>"
        xml = lxml.etree.fromstring(dat)
        rtyp = self.ApiXmlRsetSub1.rtyp(xml)
        self.assertEqual(rtyp, "dbScrs")

    # rtyp: wrong number of fields
    def testRtypErrFields(self):
        dat = b"<r l=''><f n='a'/><f n='b'/></r>"
        xml = lxml.etree.fromstring(dat)
        with self.assertRaises(pgfm.ErrApiXmlRsetRtypFields) as c:
            self.ApiXmlRsetSub1.rtyp(xml)
        str(c.exception)

    # rtyp: wrong field name
    def testRtypErrFieldName(self):
        dat = b"<r l=''><f n='OTHER_NAME'/></r>"
        xml = lxml.etree.fromstring(dat)
        with self.assertRaises(pgfm.ErrApiXmlRsetRtypFieldName) as c:
            self.ApiXmlRsetSub1.rtyp(xml)
        str(c.exception)

    # rtyp: lay
    def testRtypLay(self):
        dat = b"<r l='Lay' n='0'/>"
        xml = lxml.etree.fromstring(dat)
        rtyp = self.ApiXmlRsetSub1.rtyp(xml)
        self.assertEqual(rtyp, "layInf")

    # rtyp: rset
    def testRtypRset(self):
        dat = b"<r l='Lay' n='1'/>"
        xml = lxml.etree.fromstring(dat)
        rtyp = self.ApiXmlRsetSub1.rtyp(xml)
        self.assertEqual(rtyp, "recset")

    class ApiXmlRsetSub(pgfm.ApiXmlRset):
        XpLayKey = pgfm.ApiXml.Xp("/*/*[1]")

    # layKey
    def testLayKey(self):
        xml = lxml.etree.fromstring(b"<abc><def/><ghi/></abc>")
        key = self.ApiXmlRsetSub.layKey(xml)
        self.assertEqual(key, b"<def/>")

    class ApiXmlRsetSub2(pgfm.ApiXmlRset):
        @classmethod
        def XpNames(cls, xml):
            return "abc", "def", "ghi"

    # srvDbs
    def testSrvDbs(self):    
        res = self.ApiXmlRsetSub2.srvDbs(None)
        self.assertEqual(res, ("ABC", "DEF", "GHI"))

    # dbLays
    
    # dbScrs
        
        
# ============================================================================

class TestColName(unittest.TestCase):

    # __new__: create from a string.
    def testNewStr(self):
        colName1 = pgfm.ColName("field")
        self.assertIsInstance(colName1, pgfm.ColName)
        self.assertEqual(colName1, "FIELD") # ignore case
        colName2 = pgfm.ColName("table::field")
        self.assertIsInstance(colName2, pgfm.ColName)
        self.assertEqual(colName2, "TABLE::FIELD") # ignore case.

    # __new__: create from ColName.
    def testNewColName(self):
        colName1 = pgfm.ColName("field")
        colName2 = pgfm.ColName(colName1)
        self.assertIs(colName1, colName2)

    # __new__: create with a default table without its own.
    def testNewNoTableDflt(self):
        colName = pgfm.ColName("field", "defaultTable")
        self.assertEqual(colName, "DEFAULTTABLE::FIELD") # ignore case

    # __new__: create with a default table with its own.
    def testNewTableDflt(self):
        colName = pgfm.ColName("table::field", "defaultTable")
        self.assertEqual(colName, "TABLE::FIELD") # ignore case

    # tbl: read a non-empty table part.
    def testTbl(self):
        colName = pgfm.ColName("table::field")
        self.assertIsInstance(colName.tbl, pgfm.Name)
        self.assertEqual(colName.tbl, "TABLE") # ignore case

    # tbl: read an empty table part.
    def testTblEmpty(self):
        colName = pgfm.ColName("field")
        self.assertIsInstance(colName.tbl, pgfm.Name)
        self.assertIs(colName.tbl, pgfm.emptyName)

# ============================================================================

class TestContainer(unittest.TestCase):

    # For now only empty string and None.

    # FromStr: empty
    def testFromStrEmpty(self):
        val = pgfm.Container.FromStr("")
        self.assertIs(val, pgfm.emptyVal)

    # __new__: str, empty
    def testNewEmpty(self):
        val = pgfm.Container("")
        self.assertIs(val, pgfm.emptyVal)

    # __new__: None
    def testNewNone(self):
        val = pgfm.Container(None)
        self.assertIs(val, pgfm.emptyVal)

    # __new__: unsuitable object.
    def testNewErr(self):
        try:
            pgfm.Container(object())
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrContainerNew)
            self.assertIsInstance(str(e), str)

# ============================================================================

class TestCmp(unittest.TestCase):

    # 'Cmp' is a mixin that provides Python-specific comparison for classes
    # with 'cmp' method. These are 'Name' and 'Val', plus their subclasses.
    # We test all comparsion functions in one method. To test 'Name' we use
    # 'Name' itself. To test 'Val' we use 'Text'. We do not test other
    # subclasses, because we only need to see that Python methods correctly
    # map to 'cmp', not the logic of 'cmp' itself. (That is tested in the
    # corresponding tests for those subclasses.)

    # Implemented in 'Name'.
    def testName(self):
        name = pgfm.Name("B")
        self.assertNotEqual(name, "a")
        self.assertGreater(name, "a")
        self.assertGreaterEqual(name, "a")
        self.assertGreaterEqual(name, "b")
        self.assertEqual(name, "b")
        self.assertLessEqual(name, "b")
        self.assertLessEqual(name, "c")
        self.assertLess(name, "c")
        self.assertNotEqual(name, "c")

    # Implemented in 'Text'.
    def testText(self):
        text = pgfm.Text("B")
        self.assertNotEqual(text, "a")
        self.assertGreater(text, "a")
        self.assertGreaterEqual(text, "a")
        self.assertGreaterEqual(text, "b")
        self.assertEqual(text, "b")
        self.assertLessEqual(text, "b")
        self.assertLessEqual(text, "c")
        self.assertLess(text, "c")
        self.assertNotEqual(text, "c")

# ============================================================================

class TestColSpec(unittest.TestCase):


    # __init__
    def testInit(self):
        relSpec = object()
        res = pgfm.ColSpec("a", "text", 1, relSpec)
        self.assertIsInstance(res, pgfm.ColSpec)
        self.assertEqual(res.name, "A")
        self.assertIs(res.type, pgfm.Text)
        self.assertEqual(res.reps, 1)
        self.assertIs(res.relSpec, relSpec)

    # __init__ with every type
    def testInitType(self):
        for tstr, type in (
                ("text"     , pgfm.Text     ), 
                ("number"   , pgfm.Number   ),
                ("date"     , pgfm.Date     ),
                ("time"     , pgfm.Time     ),
                ("timestamp", pgfm.Timestamp),
                ("container", pgfm.Container)):
            with self.subTest(tstr):
                res = pgfm.ColSpec("a", tstr, 1, None)
                self.assertIs(res.type, type)

    # col: one repetition.
    def testColOne(self):
        colSpec = pgfm.ColSpec("a", "text", 1, None)
        vs = [1, 2, 3, 4]
        res = colSpec.col(vs, 1)
        self.assertEqual(res, 2)

    # col: more than one repetition.
    def testColMany(self):
        colSpec = pgfm.ColSpec("a", "text", 2, None)
        vs = [1, 2, 3, 4]
        res = colSpec.col(vs, 1)
        self.assertEqual(res, [2, 3])

# ============================================================================

class TestColSpecOld(unittest.TestCase):

    # __init__
    def testInit(self):
        laySpec = object()
        relSpec = pgfm.RelSpecOld(laySpec, "Rel")
        res = pgfm.ColSpecOld("a", "text", 1, relSpec, 2)
        self.assertIsInstance(res, pgfm.ColSpecOld)
        self.assertEqual(res.name, "A")
        self.assertIs(res.type, pgfm.Text)
        self.assertEqual(res.reps, 1)
        self.assertIs(res.relSpec, relSpec)
        self.assertEqual(res.moff, 2)
        self.assertIs(relSpec.col, res)

    # __init__ with every type.
    def testNew(self):
        for tstr, tcls in (
                ("TEXT"     , pgfm.Text     ),
                ("NUMBER"   , pgfm.Number   ),
                ("DATE"     , pgfm.Date     ),
                ("TIME"     , pgfm.Time     ),
                ("TIMESTAMP", pgfm.Timestamp),
                ("CONTAINER", pgfm.Container)):
            with self.subTest(tstr):
                # Imitation of internal parameters.
                res = pgfm.ColSpecOld("a", tstr, 1, None, 1)
                self.assertIs(res.type, tcls)

    VS = [ 1, 2,                                   # metadata
          "a",                                     # field 1
          "b[1]", "b[2]",                          # field 2
          "c.1", "c.2",                            # field 3
          "d[1].1", "d[2].1", "d[1].2", "d[2].2" ] # field 4
    MS = [0, 2, 3, 5, 7, 11]

    class MockRec:
        def __init__(self, ms, vs, mi):
            self.data = ms, vs, mi

    class MockRow:
        def __init__(self, ms, vs, mi, ri):
            self.data = ms, vs, mi, ri

    # recCol: layout, one rep.
    def testRecColLayOne(self):
        rec = self.MockRec(self.MS, self.VS, 0)
        colSpec = pgfm.ColSpecOld("a", "text", 1, None, 1)
        res = colSpec.recCol(rec)
        self.assertEqual(res, "a")

    # recCol: layout, many reps.
    def testRecColLayMany(self):
        rec = self.MockRec(self.MS, self.VS, 0)
        colSpec = pgfm.ColSpecOld("a", "text", 2, None, 2)
        res = colSpec.recCol(rec)
        self.assertEqual(res, ["b[1]", "b[2]"])

    # recCol: portal, one rep.
    def testRecColRelOne(self):
        rec = self.MockRec(self.MS, self.VS, 0)
        colSpec = pgfm.ColSpecOld("a", "text", 1, None, 3)
        res = colSpec.recCol(rec)
        self.assertEqual(res, "c.1")

    # recCol: portal, many rep.
    def testRecColRelMany(self):
        rec = self.MockRec(self.MS, self.VS, 0)
        colSpec = pgfm.ColSpecOld("a", "text", 2, None, 4)
        res = colSpec.recCol(rec)
        self.assertEqual(res, ["d[1].1", "d[2].1"])

    # rowCol: one rep.
    def testRowColOne(self):
        colSpec = pgfm.ColSpecOld("a", "text", 1, None, 3)

        row1 = self.MockRow(self.MS, self.VS, 0, 0)
        res1 = colSpec.rowCol(row1)
        self.assertEqual(res1, "c.1")

        row2 = self.MockRow(self.MS, self.VS, 0, 1)
        res1 = colSpec.rowCol(row2)
        self.assertEqual(res1, "c.2")

    # rowCol: many reps.
    def testRowColMany(self):
        colSpec = pgfm.ColSpecOld("a", "text", 2, None, 4)

        row1 = self.MockRow(self.MS, self.VS, 0, 0)
        res1 = colSpec.rowCol(row1)
        self.assertEqual(res1, ["d[1].1", "d[2].1"])

        row2 = self.MockRow(self.MS, self.VS, 0, 1)
        res1 = colSpec.rowCol(row2)
        self.assertEqual(res1, ["d[1].2", "d[2].2"])

# ============================================================================

class TestColSpecNew(unittest.TestCase):

    # __init__
    def testInit(self):
        relSpec = object()
        res = pgfm.ColSpecNew("a", "text", 1, relSpec, 2)
        self.assertIsInstance(res, pgfm.ColSpecNew)
        self.assertEqual(res.name, "A")
        self.assertIs(res.type, pgfm.Text)
        self.assertEqual(res.reps, 1)
        self.assertIs(res.relSpec, relSpec)
        self.assertEqual(res.voff, 2)

    # __init__ with every type
    def testInitType(self):
        for tstr, tcls in (
                ("text"     , pgfm.Text     ),
                ("number"   , pgfm.Number   ),
                ("date"     , pgfm.Date     ),
                ("time"     , pgfm.Time     ),
                ("timestamp", pgfm.Timestamp),
                ("container", pgfm.Container)):
            with self.subTest(tstr):
                res = pgfm.ColSpecNew("a", tstr, 1, None, 1)
                self.assertIs(res.type, tcls)

    VS = [
        2, 1, "a", "b[1]", "b[2]",       # record
        4, 3, "c.1", "d[1].1", "d[2].1", # portal, row 1
        6, 5, "c.2", "d[1].2", "d[2].2", # portal, row 2
    ]
    MS = [ 0, 5, 15 ]

    class MockRec:
        def __init__(self, *data):
            self.data = data

    class MockRow:
        def __init__(self, *data):
            self.data = data

    # recCol: layout, one rep.
    def testRecColLayOne(self):
        colSpec = pgfm.ColSpecNew("a", "text", 1, None, 2)
        rec = self.MockRec(self.MS, 0, self.VS, 0)
        res = colSpec.recCol(rec)
        self.assertEqual(res, "a")

    # recCol: layout, many reps.
    def testRecColLayMany(self):
        colSpec = pgfm.ColSpecNew("a", "text", 2, None, 3)
        rec = self.MockRec(self.MS, 0, self.VS, 0)
        res = colSpec.recCol(rec)
        self.assertEqual(res, ["b[1]", "b[2]"])

    # recCol: portal, one rep.
    def testRecColRelOne(self):
        relSpec = pgfm.RelSpecNew(None, "a", 1)
        colSpec = pgfm.ColSpecNew("a", "text", 1, relSpec, 2)
        rec = self.MockRec(self.MS, 0, self.VS, 0)
        res = colSpec.recCol(rec)
        self.assertEqual(res, "c.1")

    # recCol: portal, many reps.
    def testRecColRelMany(self):
        relSpec = pgfm.RelSpecNew(None, "a", 1)
        colSpec = pgfm.ColSpecNew("a", "text", 2, relSpec, 3)
        rec = self.MockRec(self.MS, 0, self.VS, 0)
        res = colSpec.recCol(rec)
        self.assertEqual(res, ["d[1].1", "d[2].1"])

    # rowCol: one rep.
    def testRowColOne(self):
        relSpec = pgfm.RelSpecNew(None, "a", 1)
        colSpec = pgfm.ColSpecNew("a", "text", 1, relSpec, 2)

        row1 = self.MockRow(self.VS, 5)
        res1 = colSpec.rowCol(row1)
        self.assertEqual(res1, "c.1")

        row2 = self.MockRow(self.VS, 10)
        res2 = colSpec.rowCol(row2)
        self.assertEqual(res2, "c.2")

    # rowCol: many reps.
    def testRowColMany(self):
        relSpec = pgfm.RelSpecNew(None, "a", 1)
        colSpec = pgfm.ColSpecNew("a", "text", 2, relSpec, 3)

        row1 = self.MockRow(self.VS, 5)
        res1 = colSpec.rowCol(row1)
        self.assertEqual(res1, ["d[1].1", "d[2].1"])

        row2 = self.MockRow(self.VS, 10)
        res2 = colSpec.rowCol(row2)
        self.assertEqual(res2, ["d[1].2", "d[2].2"])    

# ============================================================================

class TestColSpecSrc(unittest.TestCase):

    # This class is a mixin for LaySpec and RelSpec that provides common
    # methods to get field specifications (ColSpec). The subclass must define
    # the '_colSpec' and '_valsByColSpecs' methods. To test its functionality
    # I use a mock class that inherits 'ColSpecSrc' and defines the necessary
    # methods. The '_colSpec' method accepts any field name and returns
    # 's:<name>' as the “specification”. The '_valsByColSpecs' merely returns
    # what it received so that I can see that 'ColSpecSrc' passes what is
    # expected.

    class MockColSpecSrcHost(pgfm.ColSpecSrc):

        def _colSpec(self, name):
            return "s:" + name

        def _valsByColSpecs(self, item, colSpecs):
            return item, colSpecs

    # colSpec: Ask for a single field, get a single field.
    def testColSpecOne(self):
        subclass = self.MockColSpecSrcHost()
        res = subclass.colSpec("abc")
        self.assertEqual(res, "s:abc")

    # colSpec: Ask for multiple fields, get a list of fields.
    def testColSpecMany(self):
        subclass = self.MockColSpecSrcHost()
        res = subclass.colSpec("abc", "def")
        self.assertEqual(res, ["s:abc", "s:def"])

    # colSpec: See also tests for layout and portal specifications.

    # _colSpecs: pass a list of names, get a list of specs.
    def testColSpecsOne(self):
        subclass = self.MockColSpecSrcHost()
        res = subclass._colSpecs(["abc"])
        self.assertEqual(res, ["s:abc"])

    # _colSpecs: same, multiple names.
    def testColSpecsMany(self):
        subclass = self.MockColSpecSrcHost()
        res = subclass._colSpecs(["abc", "def"])
        self.assertEqual(res, ["s:abc", "s:def"])

    # _valsByColNames: call _valsByColSpecs with same item and specs.
    def testValsByColNamesOne(self):
        subclass = self.MockColSpecSrcHost()
        item = object()
        res = subclass._valsByColNames(item, ["abc"])
        self.assertEqual(res, (item, ["s:abc"]))

    # _valsByColNames: same, multiple names.
    def testValsByColNamesMany(self):
        subclass = self.MockColSpecSrcHost()
        item = object()
        res = subclass._valsByColNames(item, ["abc", "def"])
        self.assertEqual(res, (item, ["s:abc", "s:def"]))

    # _valsByColNames: see also tests for records and rows.

# ============================================================================

class TestDate(unittest.TestCase):

    # Fmt: format as a FileMaker date.
    def testFmt(self):
        val = pgfm.Date.Fmt(2023, 1, 2)
        self.assertEqual(val, "1/2/2023")
        val = pgfm.Date.Fmt(2023, 1, 15)
        self.assertEqual(val, "1/15/2023")

    # FromInt: create from number of days.
    def testFromInt(self):
        val = pgfm.Date.FromInt(738535)
        self.assertIsInstance(val, pgfm.Date)
        self.assertEqual(val, "1/15/2023")

    # FromNum: create from number of days.
    def testFromNum(self):
        val = pgfm.Date.FromNum(738535)
        self.assertIsInstance(val, pgfm.Date)
        self.assertEqual(val, "1/15/2023")

    # FromPyDate: from Python date.
    def testFromPyDate(self):
        val = pgfm.Date.FromPyDate(datetime.date(2023, 1, 15))
        self.assertIsInstance(val, pgfm.Date)
        self.assertEqual(val, "1/15/2023")

    # FromStr: create from str, not empty.
    def testFromStr(self):
        val = pgfm.Date.FromStr("1/15/2023")
        self.assertIsInstance(val, pgfm.Date)
        self.assertEqual(val.toYmd(), (2023, 1, 15))

    # FromStr: create from str, empty.
    def testFromStrEmpty(self):
        val = pgfm.Date.FromStr("")
        self.assertIs(val, pgfm.emptyVal)

    # FromYmd: create from year, month, days.
    def testFromYmd(self):
        val = pgfm.Date.FromYmd(2023, 1, 15)
        self.assertIsInstance(val, pgfm.Date)
        self.assertEqual(val, "1/15/2023")

    # __new__: from str, not empty.
    def testNewStr(self):
        val = pgfm.Date("1/15/2023")
        self.assertIsInstance(val, pgfm.Date)
        self.assertEqual(val.toYmd(), (2023, 1, 15))

    # __new__: from str, empty.
    def testNewStrEmpty(self):
        val = pgfm.Date("")
        self.assertIs(val, pgfm.emptyVal)

    # __new__: from int.
    def testNewInt(self):
        val = pgfm.Date(738535)
        self.assertIsInstance(val, pgfm.Date)
        self.assertEqual(val, "1/15/2023")

    # __new__: from Python date.
    def testNewPyDate(self):
        val = pgfm.Date(datetime.date(2023, 1, 15))
        self.assertIsInstance(val, pgfm.Date)
        self.assertEqual(val, "1/15/2023")

    # __new__: from None.
    def testNewNone(self):
        val = pgfm.Date(None)
        self.assertIs(val, pgfm.emptyVal)

    # __new__: from Ymd.
    def testNewYmd(self):
        val = pgfm.Date(2023, 1, 15)
        self.assertIsInstance(val, pgfm.Date)
        self.assertEqual(val, "1/15/2023")

    # __new__: from Number.
    def testNewNumber(self):
        val1 = pgfm.Date(2023, 1, 15)
        val2 = pgfm.Date(val1)
        self.assertIs(val1, val2)

    # __new__: bad args, 1.
    def testNewErr1(self):
        try:
            pgfm.Date(object())
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrDateNew)
            self.assertIsInstance(str(e), str)

    # __new__: bad args, 2.
    def testNewErr2(self):
        try:
            pgfm.Date(2023, 1)
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrDateNew)
            self.assertIsInstance(str(e), str)

    # __hash__: same for same dates.
    def testHash(self):
        val1 = pgfm.Date(2023, 1, 15)
        val2 = pgfm.Date("1/15/2023")
        self.assertEqual(hash(val1), hash(val2))

    # cmpEx: testing via Python methods in 'Cmp', 'Val.cmp', 'cmpEx'.
    # compares as date, converts parameters.
    def testCmpEx(self):
        # Lexicographically '1/10/2024' < '1/15/2023' < '1/2/2023'.
        val = pgfm.Date("1/15/2023")
        self.assertNotEqual(val, "1/2/2023")
        self.assertGreater(val, "1/2/2023")
        self.assertGreaterEqual(val, "1/2/2023")
        self.assertGreaterEqual(val, "1/15/2023")
        self.assertEqual(val, "1/15/2023")
        self.assertLessEqual(val, "1/15/2023")
        self.assertLessEqual(val, "1/10/2024")
        self.assertLess(val, "1/10/2024")
        self.assertNotEqual(val, "1/10/2024")

    # toInt: get integer.
    def testToInt(self):
        val = pgfm.Date("1/15/2023")
        self.assertEqual(val.toInt(), 738535)
        self.assertEqual(pgfm.Date(val.toInt()), val)

    # toNum: get integer.
    def testToNum(self):
        val = pgfm.Date("1/15/2023")
        self.assertEqual(val.toNum(), 738535)
        self.assertEqual(pgfm.Date(val.toNum()), val)

    # toPyDate
    def testToPyDate(self):
        val = pgfm.Date("1/15/2023")
        self.assertEqual(val.toPyDate(), datetime.date(2023, 1, 15))
        self.assertEqual(pgfm.Date(val.toPyDate()), val)

    # toStr
    def testToStr(self):
        val = pgfm.Date("1/15/2023")
        self.assertEqual(val.toStr(), "1/15/2023")
        self.assertEqual(pgfm.Date(val.toStr()), val)

    # toYmd
    def testToStr(self):
        val = pgfm.Date("1/15/2023")
        self.assertEqual(val.toYmd(), (2023, 1, 15))
        self.assertEqual(pgfm.Date(*val.toYmd()), val)

# ============================================================================
# Tests for exceptions mostly test whether an exception can be printed: they
# make sure the '__str__' method has no errors and returns a string. They do
# not check the wording.
# ============================================================================

class TestErrFm(unittest.TestCase):

    # __init__: basic
    def testInit(self):
        err = pgfm.ErrFm(401)
        self.assertEqual(err.code, 401)
        self.assertIsInstance(err.text, None)

    # __init__: explicit text.
    def testInit(self):
        err = pgfm.ErrFm(401, "text")
        self.assertEqual(err.code, 401)
        self.assertEqual(err.text, "text")

    # __str__: no text, standard error.
    def testStr(self):
        err = pgfm.ErrFm(401)
        res = str(err)
        self.assertIsInstance(res, str)
        # Testing the text of this one.
        self.assertEqual(res, "FileMaker error 401: "
                "No records match the request.")

    # __str__: no text, unknown error.
    def testStrUnk(self):
        err = pgfm.ErrFm(450) # presumed to be unknown
        res = str(err)
        self.assertIsInstance(res, str)
        self.assertEqual(res, ("Unknown FileMaker error, code 450."))

    # __str__: explicit text.
    def testStrExlp(self):
        err = pgfm.ErrFm(401, "text")
        res = str(err)
        self.assertIsInstance(res, str)
        self.assertEqual(res, "text")

    # __getattr__: access own attributes.
    def testGetattr(self):
        err = pgfm.ErrFm(401)
        err.text # works

    # __getattr__: error on other attributes
    def testGetattrErr(self):
        err = pgfm.ErrFm(401)
        with self.assertRaises(pgfm.ErrFm) as c:
            err.rec(0)
        self.assertIs(c.exception, err)

    # __iter__: error on iter.
    def testIter(self):
        err = pgfm.ErrFm(401)
        with self.assertRaises(pgfm.ErrFm) as c:
            for item in err:
                pass
        self.assertIs(c.exception, err)

# ============================================================================

class TestFolder(unittest.TestCase):
    
    # __init__
    def testInit(self):
        folder = pgfm.Folder("test")
        self.assertIsInstance(folder, pgfm.Folder)
        self.assertIsInstance(folder, list)
        self.assertEqual(folder.name, "TEST") # ignore case

# ============================================================================

class TestGlobal(unittest.TestCase):

    def testDefaultApi(self):
        self.assertIn(pgfm.defaultApi, (pgfm.ApiData1,
                                        pgfm.ApiData2,
                                        pgfm.ApiDataLatest,
                                        pgfm.ApiXmlLay,
                                        pgfm.ApiXmlNew,
                                        pgfm.ApiXmlOld))

# ============================================================================

class TestHttpReq(unittest.TestCase):

    # To create a request we need verb and path.

    # __init__: minimal.
    def testInit(self):
        req = pgfm.HttpReq("GET", "/path")
        self.assertIsInstance(req, pgfm.HttpReq)
        self.assertEqual(req.verb, "GET")
        self.assertEqual(req.path, "/path")
        self.assertIs(req.data, None)
        self.assertEqual(req._headers, {})

    # __init__: data, bytes.
    def testInitBytes(self):
        req = pgfm.HttpReq("GET", "/path", b"abc")
        self.assertIs(req.data, b"abc")

    # __init__: data, string, safe for Latin-1.
    def testInitStr(self):
        req = pgfm.HttpReq("GET", "/path", "mañana")
        self.assertEqual(req.data, "mañana".encode("latin-1"))

    # __init__: data, string, unsafe for Latin-1.
    def testInitStrErr(self):
        try:
            pgfm.HttpReq("GET", "/path", "ЖФЦ")
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrHttpReqStr)
            self.assertIsInstance(str(e), str)

    # __init__: data, neither bytes nor string.
    def testInitDataErr(self):
        try:
            pgfm.HttpReq("GET", "/path", 123)
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrHttpReqData)
            self.assertIsInstance(str(e), str)

    # __init__: data and MIME.
    def testInitMime(self):
        req = pgfm.HttpReq("GET", "/path", b"abc", "text/plain")
        self.assertEqual(req._headers, {"content-type": "text/plain"})

        # The headers are for writing, so text strings are not normalized and
        # thus case-sensitive: testing for 'Content-Type' won't work.

    # __init__: MIME without data.
    def testInitMimeErr(self):
        try:
            pgfm.HttpReq("GET", "/path", mime="text/plain")
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrHttpReqMime)
            self.assertIsInstance(str(e), str)

    # send: without authentification.
    def testSend(self):
        srv = pgfm.Srv("url")
        httpReq = pgfm.HttpReq("GET", "/path", b"{}", "application/json")
        with ReplaceReq() as repl:
            httpResp = httpReq.send(srv)
        self.assertIsInstance(httpResp, pgfm.HttpResp)
        req = repl.req(0)
        self.assertEqual(req.verb, "GET")
        self.assertEqual(req.url, "url/path")
        self.assertEqual(req.data, b"{}")
        self.assertEqual(req.headers["content-type"], "application/json")
        self.assertNotIn("authorization", req.headers)

    # send: with User authentification.
    def testSendUser(self):
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        httpReq = pgfm.HttpReq("GET", "/path", b"{}", "application/json")
        with ReplaceReq() as repl:
            httpResp = httpReq.send(srv, user)
        req = repl.req(0)
        self.assertIn("authorization", req.headers)
        # Authentification does not get into HttpReq itself.
        self.assertNotIn("authorization", httpReq._headers)

    # send: with Session authentification.
    def testSendSession(self):
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        # Response to the login request.
        httpReq = pgfm.HttpReq("GET", "/path", b"{}", "application/json")
        session = pgfm.Session(srv, "file", user)
        resp = MockReqResp(200, {"x-fm-data-access-token":"TOK"})
        with ReplaceReq(resp) as repl:
            try:
                httpResp = httpReq.send(srv, session)
            finally:
                # Explicitly logout to have the call caught by 'repl'.
                session.logout()
        # When sending a request with a session that is not yet active it will
        # automatically activate (log in) when the request accesses its 'auth'
        # property. Later, when the session is destroyed, it will log out. (In
        # our case we log out explicitly to catch that request within the
        # 'with' block.) The overall sequence of calls will be that:
        #
        # 1. Session logs in in with basic authentification and gets a token.
        # 2. Main request goes with bearer authentification.
        # 3. Session logs out.
        self.assertEqual(len(repl), 3)
        req = repl.req(1) # 2nd request.
        self.assertEqual(req.headers["authorization"], "bearer TOK")
        # Authentification does not get into HttpReq itself.
        self.assertNotIn("authorization", httpReq._headers)

# ============================================================================

class TestHttpResp(unittest.TestCase):

    # __init__: typical.
    def testInit(self):
        srv = object()
        auth = object()
        httpReq = pgfm.HttpReq("GET", "/path")
        headers = {"content-type": "text/plain"}
        content = b"abc"
        httpResp = pgfm.HttpResp(httpReq, srv, auth, 200, headers, content)
        self.assertIsInstance(httpResp, pgfm.HttpResp)
        self.assertIs(httpResp.srv, srv)
        self.assertIs(httpResp.auth, auth)
        self.assertIs(httpResp.req, httpReq)
        self.assertEqual(httpResp.code, 200)
        self.assertIs(httpResp.hdrs, headers)
        self.assertIs(httpResp.data, content)
        self.assertIsNone(httpResp.error)

    # __init__: with code 4xx or greater.
    def testInitError(self):
        srv = object()
        auth = object()
        httpReq = pgfm.HttpReq("GET", "/path")
        headers = {"content-type": "text/plain"}
        content = b"abc"
        httpResp = pgfm.HttpResp(srv, auth, httpReq, 400, headers, content)
        self.assertIsInstance(httpResp.error, pgfm.ErrHttpResp)
        self.assertIsInstance(str(httpResp.error), str)

    # header
    def testHeader(self):
        srv = object()
        auth = object()
        httpReq = pgfm.HttpReq("GET", "/path")
        headers = {"content-type": "text/plain"}
        content = b"abc"
        httpResp = pgfm.HttpResp(srv, auth, httpReq, 200, headers, content)
        self.assertEqual(httpResp.header("content-type"), "text/plain")

        # The real headers object comes from 'requests' and has
        # case-insensitive keys, but we do not test it here.

# ============================================================================

class TestLayDesc(unittest.TestCase):
    
    # __init__
    def testInit(self):
        layDesc = pgfm.LayDesc()
        self.assertIsInstance(layDesc, pgfm.LayDesc)

    # col: set.
    def testCol(self):
        layDesc = pgfm.LayDesc()
        layDesc.col("aa", 2)
        self.assertEqual(layDesc.colReps("AA"), 2)
        layDesc.col("b::bb", 3)
        self.assertEqual(layDesc.colReps("B::BB"), 3)

    # col: set same value.
    def testColSame(self):
        layDesc = pgfm.LayDesc()
        layDesc.col("aa", 2)
        layDesc.col("aa", 2)

    # col: set different value.
    def testColDiff(self):
        layDesc = pgfm.LayDesc()
        layDesc.col("aa", 2)
        with self.assertRaises(pgfm.ErrLayDescCol) as c:
            layDesc.col("aa", 3)
        str(c.exception)
        self.assertEqual(layDesc.colReps("aa"), 2)

    # rel: set.
    def testRel(self):
        layDesc = pgfm.LayDesc()
        layDesc.rel("a", "a::aa", "b::bb", "cc")
        self.assertEqual(layDesc.relName("A::AA"), "A")
        self.assertEqual(layDesc.relName("B::BB"), "A")
        self.assertEqual(layDesc.relName("A::CC"), "A") # added table name

    # rel: set same.
    def testRelSame(self):
        layDesc = pgfm.LayDesc()
        layDesc.rel("a", "a::aa")
        layDesc.rel("A", "AA")
        self.assertEqual(len(layDesc._cnamToRnam), 1)
        self.assertEqual(layDesc.relName("A::AA"), "A")

    # rel: set different.
    def testRelDiff(self):
        layDesc = pgfm.LayDesc()
        layDesc.rel("a", "aa")
        with self.assertRaises(pgfm.ErrLayDescRel) as c:
            layDesc.rel("B", "A::AA")
        str(c.exception)
        self.assertEqual(layDesc.relName("A::AA"), "A")

    # rel: conflict with 'lay'
    def testLay(self):
        layDesc = pgfm.LayDesc()
        layDesc.rel("a", "aaa")
        with self.assertRaises(pgfm.ErrLayDescRel) as c:
            layDesc.lay("A::AA")
        str(c.exception)
        self.assertEqual(layDesc.relName("A::AA"), "A")

    # lay: set.
    def testLay(self):
        layDesc = pgfm.LayDesc()
        layDesc.lay("a::aa", "b::bb")
        self.assertEqual(layDesc.relName("A::AA"), "")
        self.assertEqual(layDesc.relName("B::BB"), "")

    # lay: set same.
    def testLay(self):
        layDesc = pgfm.LayDesc()
        layDesc.lay("a::aa")
        layDesc.lay("a::aa")
        self.assertEqual(layDesc.relName("a::aa"), "")
        self.assertEqual(layDesc.relName("b::bb"), "")

    # lay: conflict with 'rel'
    def testLay(self):
        layDesc = pgfm.LayDesc()
        layDesc.lay("a::aa")
        with self.assertRaises(pgfm.ErrLayDescRel) as c:
            layDesc.rel("A", "AA")
        str(c.exception)
        self.assertEqual(layDesc.relName("A::AA"), "")

    # relName
    def testRelName(self):
        layDesc = pgfm.LayDesc()
        layDesc.rel("a", "b::bb")
        self.assertEqual(layDesc.relName("B::BB"), "A")

    # colReps
    def testColReps(self):
        layDesc = pgfm.LayDesc()
        layDesc.col("a::aa", 2)
        self.assertEqual(layDesc.colReps("A::AA"), 2)

    # relNames
    def testRelNames(self):
        layDesc = pgfm.LayDesc()
        layDesc.rel("a", "b:bb", "c::cc")
        layDesc.lay("d", "e::ee")
        relNames = list(layDesc.relNames())
        self.assertEqual(relNames, ["A"])

    # laySlot: basic
    def testLaySlot(self):
        layDesc = pgfm.LayDesc()
        laySlot = layDesc.laySlot(pgfm.ApiXmlOld)
        self.assertIsInstance(laySlot, pgfm.LaySlot)

    # laySlot: same object for same class.
    def testLaySlotAgain(self):
        layDesc = pgfm.LayDesc()
        api = pgfm.ApiXmlOld
        laySlot1 = layDesc.laySlot(api)
        laySlot2 = layDesc.laySlot(api)
        self.assertIs(laySlot1, laySlot2)

    # laySlot: another object for another class.
    def testLaySlotOther(self):
        layDesc = pgfm.LayDesc()
        laySlot1 = layDesc.laySlot(pgfm.ApiXmlOld)
        laySlot2 = layDesc.laySlot(pgfm.ApiXmlNew)
        self.assertIsNot(laySlot1, laySlot2)

# ============================================================================
# A LaySlot is a part of LayDesc that stores a cached layout of a specific
# class. It is a simple structure with two public fields.

class TestLaySlot(unittest.TestCase):

    # Create without parameters.
    def testInit(self):
        laySlot = pgfm.LaySlot()
        self.assertIsInstance(laySlot, pgfm.LaySlot)
        self.assertIsNone(laySlot.key)
        self.assertIsNone(laySlot.lay)

    # Can edit 'key'.
    def testKey(self):
        mockKey = object()
        laySlot = pgfm.LaySlot()
        laySlot.key = mockKey
        self.assertIs(laySlot.key, mockKey)

    # Can edit 'lay'.
    def testLay(self):
        mockLay = object()
        laySlot = pgfm.LaySlot()
        laySlot.lay = mockLay
        self.assertIs(laySlot.lay, mockLay)

# ============================================================================

class TestLaySpec(unittest.TestCase):

    # __init__: basic
    def testInit(self):
        laySpec = pgfm.LaySpec("db", "lay", "dpic", "ipic")
        self.assertEqual(laySpec.fnam, "DB") # ignore case
        self.assertEqual(laySpec.lnam, "LAY") # ignore case
        self.assertEqual(laySpec.tnam, "")
        self.assertEqual(laySpec.dpic, "dpic")
        self.assertEqual(laySpec.ipic, "ipic")
        self.assertEqual(laySpec.mpic, "dpic ipic")

    # __init__: with 'tnam' and 'mpic'
    def testInitEx(self):
        laySpec = pgfm.LaySpec("db", "lay", "dpic", "ipic", "tbl", "mpic")
        self.assertEqual(laySpec.tnam, "TBL") # ignore case
        self.assertIs(laySpec.mpic, "mpic")

    # relSpec: brings what is in '_rels'.
    def testRelSpec(self):
        laySpec = pgfm.LaySpec("db", "lay", "dpic", "ipic")
        relSpec = object()
        laySpec._rels[pgfm.Name("abc")] = relSpec
        self.assertIs(laySpec.relSpec("ABC"), relSpec) # ignore case

    # relSpec: see also specific LaySpec subclasses.

    # _colSpec: brings what is in '_cols'.
    def testColSpec(self):
        laySpec = pgfm.LaySpec("db", "lay", "dpic", "ipic")
        colSpec = object()
        laySpec._cols[pgfm.Name("abc")] = colSpec
        self.assertIs(laySpec._colSpec("ABC"), colSpec) # ignore case

    # _colSpec: see also specific LaySpec subclasses.

    # To test '_rel' we need a RelSpec that has a '_rel' method that takes a 
    # single argument.
    
    class MockRelSpec:
        def _rel(self, rec):
            return self, rec
    
    # _rel: basic.
    def testRel(self):
        laySpec = pgfm.LaySpec("db", "lay", "dpic", "ipic")
        relSpec = self.MockRelSpec()
        laySpec._rels[pgfm.Name("abc")] = relSpec
        rec = object()
        rel = laySpec._rel(rec, "ABC")
        self.assertEqual(rel, (relSpec, rec))
    
    # _rel: see also Rec tests.

    # To test '_valsByColSpecs' we need a ColSpec that has a '_recCol' method
    # that takes a single argument.
    
    class MockColSpec:
        def recCol(self, rec):
            return self, rec

    # _valsByColSpecs: one spec.
    def testValsByColSpecsOne(self):
        laySpec = pgfm.LaySpec("db", "lay", "dpic", "ipic")
        colSpec = self.MockColSpec() 
        rec = object()
        res = laySpec._valsByColSpecs(rec, (colSpec,))
        self.assertEqual(res, (colSpec, rec))

    # _valsByColSpecs: multiple specs.
    def testValsByColSpecsOne(self):
        laySpec = pgfm.LaySpec("db", "lay", "dpic", "ipic")
        colSpec1 = self.MockColSpec() 
        colSpec2 = self.MockColSpec() 
        rec = object()
        res = laySpec._valsByColSpecs(rec, (colSpec1, colSpec2))
        self.assertEqual(res, [(colSpec1, rec), (colSpec2, rec)])

# ============================================================================

class TestLaySpecXmlNew(unittest.TestCase):

    # __init__: without description.
    def testInit(self):
        laySpec = pgfm.LaySpecXapiNew(Xml.Get("New"))
        self.assertIsInstance(laySpec, pgfm.LaySpecXapiNew)
        self.assertEqual(laySpec.fnam, "Db")
        self.assertEqual(laySpec.lnam, "Lay")
        self.assertEqual(laySpec.tnam, "Tbl")
        relSpecNames = [r.name for r in laySpec._rels.values()]
        self.assertEqual(relSpecNames, ["c"])
        colSpecNames = [c.name for c in laySpec._cols.values()]
        self.assertEqual(colSpecNames, ["aa", "b::bb", "c::cc", "d::dd"])
        conv = [int, int, pgfm.Text, pgfm.Text, pgfm.Text,
                int, int, pgfm.Text, pgfm.Text, pgfm.Text, pgfm.Text]
        self.assertEqual(laySpec._conv, conv)

    # __init__: with description.
    def testInitDesc(self):
        laySpec = pgfm.LaySpecXapiNew(Xml.Get("New"), Xml.LayDesc)
        self.assertIsInstance(laySpec, pgfm.LaySpecXapiNew)
        self.assertEqual(laySpec.fnam, "Db")
        self.assertEqual(laySpec.lnam, "Lay")
        self.assertEqual(laySpec.tnam, "Tbl")
        relSpecNames = [r.name for r in laySpec._rels.values()]
        self.assertEqual(relSpecNames, ["c"])
        colSpecNames = [c.name for c in laySpec._cols.values()]
        self.assertEqual(colSpecNames, ["aa", "b::bb", "c::cc", "d::dd"])
        conv = [int, int, pgfm.Text, pgfm.Text, pgfm.Text,
                int, int, pgfm.Text, pgfm.Text, pgfm.Text] # one less
        self.assertEqual(laySpec._conv, conv)

    # '_addConv' and '_addFelt' are low-level methods that are called during 
    # '__init__'. For testing we call them separately. The temporary 'LaySpec'
    # we use for this gets invalid, but we test the functionalify of the 
    # methods.

    # _addConv
    def testAddConv(self):
        laySpec = pgfm.LaySpecXapiNew(Xml.Get("New"))
        laySpec._addConv(str, 3)
        self.assertEqual(laySpec._conv[-3:], [str, str, str])

    FELT = b'''<field name="e" result="date" max-repeat="3"/>'''

    # _addFelt: without description
    def testAddFelt(self):
        felt = lxml.etree.fromstring(self.FELT)
        laySpec = pgfm.LaySpecXapiNew(Xml.Get("New"))
        colSpec = laySpec._addFelt(felt, None, None, 4)
        self.assertEqual(colSpec.name, "E")
        self.assertIs(colSpec.type, pgfm.Date)
        self.assertEqual(colSpec.reps, 3)
        self.assertEqual(colSpec.voff, 4)
        self.assertEqual(laySpec._conv[-3:], [pgfm.Date, pgfm.Date, 
                pgfm.Date])

    # _addFelt: with description, without settings for this field.
    def testAddFeltDescOmit(self):
        felt = lxml.etree.fromstring(self.FELT)
        layDesc = pgfm.LayDesc().col("f", 2)
        laySpec = pgfm.LaySpecXapiNew(Xml.Get("New"), layDesc)
        colSpec = laySpec._addFelt(felt, layDesc, None, 4)
        self.assertEqual(colSpec.reps, 3) # no difference.

    # _addFelt: with description, with settings for this field.
    def testAddFeltDesc(self):
        felt = lxml.etree.fromstring(self.FELT)
        layDesc = pgfm.LayDesc().col("e", 2)
        laySpec = pgfm.LaySpecXapiNew(Xml.Get("New"), layDesc)
        colSpec = laySpec._addFelt(felt, layDesc, None, 4)
        self.assertEqual(colSpec.reps, 2) # from description
        self.assertEqual(laySpec._conv[-2:], [pgfm.Date, pgfm.Date])

    # recset.
    def testRecset(self):
        xml = Xml.Get("New")
        laySpec = pgfm.LaySpecXapiNew(xml, Xml.LayDesc)
        recset = laySpec.recset(xml)
        Xml.checkRecset(self, recset)

    # _item
    def testItem(self):
        xml = Xml.Get("New")
        laySpec = pgfm.LaySpecXapiNew(xml, Xml.LayDesc)
        recset = laySpec.recset(xml)
        item = laySpec._item(recset, 0)
        self.assertIsInstance(item, pgfm.Rec)

    # _recid
    def testRecid(self):
        xml = Xml.Get("New")
        laySpec = pgfm.LaySpecXapiNew(xml, Xml.LayDesc)
        recset = laySpec.recset(xml)
        rec = recset[0]
        recid = laySpec._recid(rec)
        self.assertEqual(recid, 1)
        
    # _modid
    def testModid(self):
        xml = Xml.Get("New")
        laySpec = pgfm.LaySpecXapiNew(xml, Xml.LayDesc)
        recset = laySpec.recset(xml)
        rec = recset[0]
        modid = laySpec._modid(rec)
        self.assertEqual(modid, 2)

# ============================================================================

class TestLaySpecXmlOld(unittest.TestCase):

    # __init__: without description.
    def testInit(self):
        laySpec = pgfm.LaySpecXapiOld(Xml.Get("OldWeb"))
        self.assertIsInstance(laySpec, pgfm.LaySpecXapiOld)
        relSpecNames = [r.name for r in laySpec._rels.values()]
        self.assertEqual(relSpecNames, ["b", "c", "d"])
        colSpecNames = [c.name for c in laySpec._cols.values()]
        self.assertEqual(colSpecNames, ["aa", "b::bb", "c::cc", "d::dd"])
        colSpecB = laySpec.colSpec("b::bb")
        self.assertEqual(colSpecB.name, "b::bb")
        self.assertEqual(colSpecB.reps, 2)
        self.assertEqual(colSpecB.relSpec.name, "b") # from metadata
        colSpecC = laySpec.colSpec("c::cc")
        self.assertEqual(colSpecC.name, "c::cc")
        self.assertEqual(colSpecC.reps, 1)
        self.assertEqual(colSpecC.relSpec.name, "c") # from metadata
        colSpecD = laySpec.colSpec("d::dd")
        self.assertEqual(colSpecD.name, "d::dd")
        self.assertEqual(colSpecD.reps, 3) # from metadata
        self.assertEqual(colSpecD.relSpec.name, "d") # from metadata

    # __init__: with description.
    def testInitDesc(self):
        laySpec = pgfm.LaySpecXapiOld(Xml.Get("OldWeb"), Xml.LayDesc)
        self.assertIsInstance(laySpec, pgfm.LaySpecXapiOld)
        relSpecNames = [r.name for r in laySpec._rels.values()]
        self.assertEqual(relSpecNames, ["c"])
        colSpecNames = [c.name for c in laySpec._cols.values()]
        self.assertEqual(colSpecNames, ["aa", "b::bb", "c::cc", "d::dd"])

        colSpecB = laySpec.colSpec("b::bb")
        self.assertEqual(colSpecB.name, "b::bb")
        self.assertEqual(colSpecB.reps, 2)
        self.assertIs(colSpecB.relSpec, None) # from description

        colSpecC = laySpec.colSpec("c::cc")
        self.assertEqual(colSpecC.name, "c::cc")
        self.assertEqual(colSpecC.reps, 1)
        self.assertEqual(colSpecC.relSpec.name, "c") # from description

        colSpecD = laySpec.colSpec("d::dd")
        self.assertEqual(colSpecD.name, "d::dd")
        self.assertEqual(colSpecD.reps, 2) # from description
        self.assertEqual(colSpecD.relSpec.name, "c") # from description

    # recset: from server.
    def testRecsetSrv(self):
        xml = Xml.Get("OldWeb")
        laySpec = pgfm.LaySpecXapiOld(xml, Xml.LayDesc)
        recset = laySpec.recset(xml)
        Xml.checkRecset(self, recset)

    # recset: from export.
    def testRecsetExp(self):
        xml = Xml.Get("OldExp")
        laySpec = pgfm.LaySpecXapiOld(xml, Xml.LayDesc)
        recset = laySpec.recset(xml)
        Xml.checkRecset(self, recset)
    
    # _item
    def testItem(self):
        xml = Xml.Get("OldWeb")
        laySpec = pgfm.LaySpecXapiOld(xml, Xml.LayDesc)
        recset = laySpec.recset(xml)
        item = laySpec._item(recset, 0)
        self.assertIsInstance(item, pgfm.Rec)

    # _recid
    def testRecid(self):
        xml = Xml.Get("OldWeb")
        laySpec = pgfm.LaySpecXapiOld(xml, Xml.LayDesc)
        recset = laySpec.recset(xml)
        rec = recset[0]
        recid = laySpec._recid(rec)
        self.assertEqual(recid, 1)
        
    # _modid
    def testModid(self):
        xml = Xml.Get("OldWeb")
        laySpec = pgfm.LaySpecXapiOld(xml, Xml.LayDesc)
        recset = laySpec.recset(xml)
        rec = recset[0]
        modid = laySpec._modid(rec)
        self.assertEqual(modid, 2)

# ============================================================================

class TestName(unittest.TestCase):

    # 'Name' is a subclass of 'str'.
    def testSubclass(self):
        self.assertTrue(issubclass(pgfm.Name, str))

    # __new__: create from a 'str', get a new 'Name'.
    def testNewStr(self):
        name = pgfm.Name("A")
        self.assertIsInstance(name, pgfm.Name)

    # __new__: create from an empty 'str', get 'emptyName'.
    def testNewEmptyStr(self):
        name1 = pgfm.Name("")
        name2 = pgfm.Name("")
        self.assertIs(name1, pgfm.emptyName)
        self.assertIs(name2, pgfm.emptyName)

    # __new__: create from another 'Name', get the same object.
    def testNewName(self):
        name1 = pgfm.Name("A")
        name2 = pgfm.Name(name1)
        self.assertIs(name1, name2)

    # __new__: create from something else, get an error.
    def testNewErr(self):
        try:
            pgfm.Name(1)
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrNameNew)
            self.assertIsInstance(str(e), str)

    # __repr__: is a string.
    def testRepr(self):
        name = pgfm.Name("A")
        self.assertIsInstance(repr(name), str)

    # cmp: compare converts arguments, ignores case.
    def testCmp(self):
        name = pgfm.Name("B")
        self.assertEqual(name.cmp("a"), +1) # name is greater
        self.assertEqual(name.cmp("b"),  0) # name is equal
        self.assertEqual(name.cmp("c"), -1) # name is less

# ============================================================================

class TestNumber(unittest.TestCase):

    # FromNum: create from 'int'.
    def testFromNumInt(self):
        val = pgfm.Number.FromNum(1)
        self.assertIsInstance(val, pgfm.Number)
        self.assertEqual(val, "1")

    # FromNum: create from 'float'.
    def testFromNumFloat(self):
        val = pgfm.Number.FromNum(1.2)
        self.assertIsInstance(val, pgfm.Number)
        self.assertEqual(val, "1.2")

    # FromStr: create from 'str', int.
    def testFromStrInt(self):
        val = pgfm.Number.FromStr("1")
        self.assertIsInstance(val, pgfm.Number)
        self.assertEqual(val, 1)

    # FromStr: create from 'str', float.
    def testFromStrFloat(self):
        val = pgfm.Number.FromStr("1.2")
        self.assertIsInstance(val, pgfm.Number)
        self.assertEqual(val, 1.2)

    # __new__: from 'Number'.
    def testNewNumber(self):
        val1 = pgfm.Number(1)
        val2 = pgfm.Number(val1)
        self.assertIs(val1, val2)

    # __new__: from 'str', int.
    def testNewStrInt(self):
        val = pgfm.Number("1")
        self.assertIsInstance(val, pgfm.Number)
        self.assertEqual(val, 1)

    # __new__: from 'str', float.
    def testNewStrFloat(self):
        val = pgfm.Number("1.2")
        self.assertIsInstance(val, pgfm.Number)
        self.assertEqual(val, 1.2)

    # __new__: from 'int'.
    def testNewInt(self):
        val = pgfm.Number(1)
        self.assertIsInstance(val, pgfm.Number)
        self.assertEqual(val, "1")

    # __new__: from 'float'.
    def testNewInt(self):
        val = pgfm.Number(1.2)
        self.assertIsInstance(val, pgfm.Number)
        self.assertEqual(val, "1.2")

    # __new__: from empty 'str'.
    def testNewInt(self):
        val = pgfm.Number("")
        self.assertIs(val, pgfm.emptyVal)

    # __new__: from 'None'.
    def testNewInt(self):
        val = pgfm.Number(None)
        self.assertIs(val, pgfm.emptyVal)

    # __new__: from other object.
    def testNewInt(self):
        try:
            pgfm.Number(object())
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrNumberNew)
            self.assertIsInstance(str(e), str)

    # __hash__: uses numeric value.
    def testHash(self):
        val1 = pgfm.Number("1")
        val2 = pgfm.Number(1)
        self.assertEqual(hash(val1), hash(val2))

    # cmpEx: testing via Python methods in 'Cmp', 'Val.cmp', 'cmpEx'.
    # compares numerically, converts parameters.
    def testCmp(self):
        val = pgfm.Number(2)
        self.assertNotEqual(val, "1")
        self.assertGreater(val, "1")
        self.assertGreaterEqual(val, "1")
        self.assertGreaterEqual(val, "2")
        self.assertEqual(val, "2")
        self.assertLessEqual(val, "2")
        self.assertLessEqual(val, "3")
        self.assertLess(val, "3")
        self.assertNotEqual(val, "3")

    # toNum: 'int'.
    def testToNumInt(self):
        val = pgfm.Number("1")
        self.assertEqual(val.toNum(), 1)

    # toNum: 'float'.
    def testToNumInt(self):
        val = pgfm.Number("1.2")
        self.assertEqual(val.toNum(), 1.2)

    # toStr: int.
    def testToNumInt(self):
        val = pgfm.Number(1)
        self.assertEqual(val.toStr(), "1")

    # toStr: float.
    def testToNumInt(self):
        val = pgfm.Number(1.2)
        self.assertEqual(val.toStr(), "1.2")

# ============================================================================

class TestRcmd(unittest.TestCase):

    # __init__
    def test(self):
        key = object()
        val = object()
        rcmd = pgfm.Rcmd(key, val)
        self.assertIs(rcmd.key, key)
        self.assertIs(rcmd.val, val)

# ============================================================================

class TestRec(unittest.TestCase):

    class MockSpec:
        def _rel(self, rec, name):
            return self, rec, name

    # rel
    def testRel(self):
        spec = self.MockSpec()
        rec = pgfm.Rec(spec, None)
        res = rec.rel("abc")
        self.assertEqual(res, (spec, rec, "abc"))

# ============================================================================

class TestReclike(unittest.TestCase):

    # __init__
    def testInit(self):
        spec = object()
        data = object()
        reclike = pgfm.Reclike(spec, data)
        self.assertIsInstance(reclike, pgfm.Reclike)
        self.assertIs(reclike.spec, spec)
        self.assertEqual(reclike.data, (data,))

    # 'Reclike' redirects all requests to its 'spec'.
    
    class MockSpec:
        def _recid(self, reclike):
            return "recid", self, reclike
        def _modid(self, reclike):
            return "modid", self, reclike
        def _valsByColNames(self, reclike, names):
            return self, reclike, names
    
    # recid
    def testRecid(self):
        spec = self.MockSpec()
        reclike = pgfm.Reclike(spec, None)
        res = reclike.recid()
        self.assertEqual(res, ("recid", spec, reclike))

    # modid
    def testModid(self):
        spec = self.MockSpec()
        reclike = pgfm.Reclike(spec, None)
        res = reclike.modid()
        self.assertEqual(res, ("modid", spec, reclike))

    # col
    def testCol(self):
        spec = self.MockSpec()
        reclike = pgfm.Reclike(spec, None)
        res = reclike.col("abc", "def")
        self.assertEqual(res, (spec, reclike, ("abc", "def")))

# ============================================================================

class TestRecset(unittest.TestCase):

    # __init__
    def testInit(self):
        spec = object()
        data = object()
        recset = pgfm.Recset(spec, 1, 2, 3, data)
        self.assertIsInstance(recset, pgfm.Recset)
        self.assertIs(recset.spec, spec)
        self.assertEqual(recset.total, 1)
        self.assertEqual(recset.found, 2)
        self.assertEqual(recset.count, 3)
        self.assertEqual(recset._data, (data,))

# ============================================================================

class TestRecsetlike(unittest.TestCase):
    
    # _init__
    def testInit(self):
        spec = object()
        data = object()
        res = pgfm.Recsetlike(spec, 3, data)
        self.assertIsInstance(res, pgfm.Recsetlike)
        self.assertIs(res.spec, spec)
        self.assertEqual(res.count, 3)
        self.assertEqual(res._data, (data,))

    # The 'item' method calls '_item' of the 'spec'.
    class MockSpec:
        def _item(self, recsetlike, pos):
            return self, recsetlike, pos

    # item: basic
    def testItem(self):
        spec = self.MockSpec()
        recsetlike = pgfm.Recsetlike(spec, 2, None)
        res1 = recsetlike.item(0)
        self.assertEqual(res1, (spec, recsetlike, 0))
        res2 = recsetlike.item(1)
        self.assertEqual(res2, (spec, recsetlike, 1))

    # item: negative
    def testItemNeg(self):
        spec = self.MockSpec()
        recsetlike = pgfm.Recsetlike(spec, 2, None)
        res1 = recsetlike.item(-1)
        self.assertEqual(res1, (spec, recsetlike, 1))
        res2 = recsetlike.item(-2)
        self.assertEqual(res2, (spec, recsetlike, 0))

    # item: invalid
    def testItemErr(self):
        spec = self.MockSpec()
        recsetlike = pgfm.Recsetlike(spec, 2, None)
        with self.assertRaises(IndexError):
            recsetlike.item(2)
        with self.assertRaises(IndexError):
            recsetlike.item(-3)

    # __getitem__: basic.
    def testGetitem(self):
        spec = self.MockSpec()
        recsetlike = pgfm.Recsetlike(spec, 2, None)
        res1 = recsetlike[0]
        self.assertEqual(res1, (spec, recsetlike, 0))
        res2 = recsetlike[1]
        self.assertEqual(res2, (spec, recsetlike, 1))

    # __getitem__: negative
    def testGetitemNeg(self):
        spec = self.MockSpec()
        recsetlike = pgfm.Recsetlike(spec, 2, None)
        res1 = recsetlike[-1]
        self.assertEqual(res1, (spec, recsetlike, 1))
        res2 = recsetlike[-2]
        self.assertEqual(res2, (spec, recsetlike, 0))

    # __getitem__: invalid
    def testGetitemErr(self):
        spec = self.MockSpec()
        recsetlike = pgfm.Recsetlike(spec, 2, None)
        with self.assertRaises(IndexError):
            recsetlike[2]
        with self.assertRaises(IndexError):
            recsetlike[-3]

    # __len__
    def testLen(self):
        recsetlike = pgfm.Recsetlike(None, 2, None)
        self.assertEqual(len(recsetlike), 2)

    # __iter__
    def testIter(self):
        spec = self.MockSpec()
        recsetlike = pgfm.Recsetlike(spec, 2, None)
        res = list(recsetlike)
        self.assertEqual(res, [(spec, recsetlike, 0), (spec, recsetlike, 1)])

    # __reversed__
    def testReversed(self):
        spec = self.MockSpec()
        recsetlike = pgfm.Recsetlike(spec, 2, None)
        res = list(reversed(recsetlike))
        self.assertEqual(res, [(spec, recsetlike, 1), (spec, recsetlike, 0)])

# ============================================================================

class TestRel(unittest.TestCase):

    # The class has no methods and fully covered by 'Recsetlike'

    pass

# ============================================================================

class TestRelSpec(unittest.TestCase):
    
    # __init__
    def testInit(self):
        laySpec = object()
        relSpec = pgfm.RelSpec(laySpec, "name")
        self.assertIs(relSpec.laySpec, laySpec)
        self.assertEqual(relSpec.name, "NAME") # ignore case.

    # To test '_colSpec' and '_valsByColSpecs' we need a layout specification 
    # that would return a column specification by name. The column 
    # specification must know its portal specification.
    
    class MockColSpec:
        def __init__(self, name, relSpec):
            self.name = pgfm.ColName(name)
            self.relSpec = relSpec # tested
        def rowCol(self, row):
            return self, row

    class MockLaySpec:
        def __init__(self, fnam, lnam):
            self.fnam = fnam
            self.lnam = lnam
            self._cols = {}
        def addColSpec(self, colSpec):
            self._cols[colSpec.name] = colSpec
        def colSpec(self, name): # tested
            return self._cols[name]

    # _colSpec: column in a portal, short name.
    def testColSpecShort(self):
        laySpec = self.MockLaySpec("Db", "Lay")
        relSpec = pgfm.RelSpec(laySpec, "a")
        colSpec = self.MockColSpec("a::aa", relSpec)
        laySpec.addColSpec(colSpec)
        res = relSpec.colSpec("aa") # without table name
        self.assertIs(res, colSpec)

    # _colSpec: column in a portal, full name.
    def testColSpec(self):
        laySpec = self.MockLaySpec("Db", "Lay")
        relSpec = pgfm.RelSpec(laySpec, "a")
        colSpec = self.MockColSpec("b::bb", relSpec)
        laySpec.addColSpec(colSpec)
        res = relSpec.colSpec("b::bb")
        self.assertIs(res, colSpec)

    # _colSpec: column not in a portal.
    def testColSpecErr(self):
        laySpec = self.MockLaySpec("Db", "Lay")
        relSpec1 = pgfm.RelSpec(laySpec, "a")
        relSpec2 = pgfm.RelSpec(laySpec, "b")
        colSpec = self.MockColSpec("c::cc", relSpec1)
        laySpec.addColSpec(colSpec)
        with self.assertRaises(pgfm.ErrRelSpecCol) as c:
            relSpec2.colSpec("c::cc")
        str(c.exception)

    # _valsByColSpec: one specification.
    def testValsByColSpecsOne(self):
        relSpec = pgfm.RelSpec(None, "a")
        colSpec = self.MockColSpec("a", relSpec)
        row = object()
        res = relSpec._valsByColSpecs(row, (colSpec,))
        self.assertEqual(res, (colSpec, row))

    # _valsByColSpec: multiple specification.
    def testValsByColSpecsMany(self):
        relSpec = pgfm.RelSpec(None, "a")
        colSpec1 = self.MockColSpec("a", relSpec)
        colSpec2 = self.MockColSpec("b", relSpec)
        row = object()
        res = relSpec._valsByColSpecs(row, (colSpec1, colSpec2))
        self.assertEqual(res, [(colSpec1, row), (colSpec2, row)])

# ============================================================================

class TestRelSpecNew(unittest.TestCase):

    # __init__
    def testInit(self):
        laySpec = object()
        relSpec = pgfm.RelSpecNew(laySpec, "a", 1)
        self.assertIsInstance(relSpec, pgfm.RelSpecNew)
        self.assertIs(relSpec.laySpec, laySpec)
        self.assertEqual(relSpec.name, "A")
        self.assertEqual(relSpec._moff, 1)
        self.assertEqual(relSpec._vblk, 2)

    # _rel
    def testRel(self):
        xml = Xml.Get("New")
        laySpec = pgfm.LaySpecXapiNew(xml, Xml.LayDesc)
        relSpec = laySpec.relSpec("c")
        recset = laySpec.recset(xml)
        rec = recset[0]
        res = relSpec._rel(rec)
        self.assertIsInstance(res, pgfm.Rel)

    # _item
    def testItem(self):
        xml = Xml.Get("New")
        laySpec = pgfm.LaySpecXapiNew(xml, Xml.LayDesc)
        relSpec = laySpec.relSpec("c")
        recset = laySpec.recset(xml)
        rec = recset[0]
        rel = rec.rel("c")
        res = relSpec._item(rel, 0)
        self.assertIsInstance(res, pgfm.Row)

    # _recid
    def testRecid(self):
        xml = Xml.Get("New")
        laySpec = pgfm.LaySpecXapiNew(xml, Xml.LayDesc)
        relSpec = laySpec.relSpec("c")
        recset = laySpec.recset(xml)
        rec = recset[0]
        rel = rec.rel("c")
        row = rel[0]
        res = relSpec._recid(row)
        self.assertEqual(res, 3)

    # _modid
    def testModid(self):
        xml = Xml.Get("New")
        laySpec = pgfm.LaySpecXapiNew(xml, Xml.LayDesc)
        relSpec = laySpec.relSpec("c")
        recset = laySpec.recset(xml)
        rec = recset[0]
        rel = rec.rel("c")
        row = rel[0]
        res = relSpec._modid(row)
        self.assertEqual(res, 4)

# ============================================================================

class TestRelSpecOld(unittest.TestCase):

    # __init__
    def testInit(self):
        laySpec = object()
        relSpec = pgfm.RelSpecOld(laySpec, "name")
        self.assertIsInstance(relSpec, pgfm.RelSpecOld)
        self.assertIs(relSpec.laySpec, laySpec)
        self.assertEqual(relSpec.name, "NAME") # ignore case
        self.assertIsNone(relSpec.col)
        self.assertEqual(relSpec._ccnt, 0)

    # _rel
    def testRel(self):
        xml = Xml.Get("OldWeb")
        laySpec = pgfm.LaySpecXapiOld(xml, Xml.LayDesc)
        relSpec = laySpec.relSpec("c")
        recset = laySpec.recset(xml)
        rec = recset[0]
        res = relSpec._rel(rec)
        self.assertIsInstance(res, pgfm.Rel)

    # _item
    def testItem(self):
        xml = Xml.Get("OldWeb")
        laySpec = pgfm.LaySpecXapiOld(xml, Xml.LayDesc)
        relSpec = laySpec.relSpec("c")
        recset = laySpec.recset(xml)
        rec = recset[0]
        rel = rec.rel("c")
        res = relSpec._item(rel, 0)
        self.assertIsInstance(res, pgfm.Row)

    # _recid
    def testRecid(self):
        xml = Xml.Get("OldWeb")
        laySpec = pgfm.LaySpecXapiOld(xml, Xml.LayDesc)
        relSpec = laySpec.relSpec("c")
        recset = laySpec.recset(xml)
        rec = recset[0]
        rel = rec.rel("c")
        row = rel[0]
        with self.assertRaises(pgfm.ErrRelSpecOldMeta) as c:
            relSpec._recid(row)
        str(c.exception)

    # _modid
    def testModid(self):
        xml = Xml.Get("OldWeb")
        laySpec = pgfm.LaySpecXapiOld(xml, Xml.LayDesc)
        relSpec = laySpec.relSpec("c")
        recset = laySpec.recset(xml)
        rec = recset[0]
        rel = rec.rel("c")
        row = rel[0]
        with self.assertRaises(pgfm.ErrRelSpecOldMeta) as c:
            relSpec._modid(row)
        str(c.exception)

# ============================================================================

class TestReq(unittest.TestCase):

    # Request is an abstract class with a lot of functionality, so we use one
    # of subclasses to test each method.

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.Req.rtyp, "recset")

    # init: no base
    def testInitNoBase(self):
        req = pgfm.Req()
        self.assertIsInstance(req, pgfm.Req)
        self.assertIsNone(req.base)
        self.assertEqual(req._exp, 0)
        self.assertEqual(req._set, 0)
        self.assertIsNone(req.file)
        self.assertEqual(req._cmds, [])
        self.assertIsNone(req._xapi)
        self.assertIsNone(req._dapi)
        self.assertFalse(req._lock)

    class Req1(pgfm.Req):
        pass

    # init: base, same type
    def testInitBaseSame(self):
        req1 = self.Req1()
        req1._exp = 1
        req1._set = 2
        req1.file = object()
        req2 = self.Req1(req1)
        self.assertIsInstance(req2, self.Req1)
        self.assertIs(req2.base, req1)
        self.assertEqual(req2._exp, 1)
        self.assertEqual(req2._set, 2)
        self.assertIs(req2.file, req1.file)
        self.assertTrue(req1._lock)

    class Req2(pgfm.Req):
        pass
    
    # init: base, other type
    def testInitBaseOther(self):
        req1 = self.Req1()
        with self.assertRaises(pgfm.ErrReqInit) as c:
            self.Req2(req1)
        str(c.exception)

    # lock
    def testLock(self):
        req = pgfm.Req()
        self.assertFalse(req._lock)
        req.lock()
        self.assertTrue(req._lock)

    # copy
    def testCopy(self):
        req1 = pgfm.Req()
        req2 = req1.copy()
        self.assertIsInstance(req2, pgfm.Req)
        self.assertIs(req2.base, req1)
        self.assertTrue(req1._lock)

    # exp
    def testExp(self):
        req = pgfm.Req()
        self.assertEqual(req._exp, 0)
        req.exp(0b1000)
        self.assertEqual(req._exp, 0b1000)
        req.exp(0b0010)
        self.assertEqual(req._exp, 0b1010)

    # edit: editable request.
    def testEditEditable(self):
        req = pgfm.Req()
        self.assertFalse(req._lock)
        res = req.edit()
        self.assertIs(res, req)

    # edit: non-editable request.
    def testEditNonEditable(self):
        req = pgfm.Req()
        req.lock()
        self.assertTrue(req._lock)
        with self.assertRaises(pgfm.ErrReqEdit) as c:
            req.edit()
        str(c.exception)

    # set: no args
    def testSetNoArgs(self):
        req = pgfm.Req()
        req.set(0b1, pgfm.NONE, pgfm.ANY)
        self.assertEqual(req._set & 0b1, 0b1)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, 0b1)
        self.assertEqual(req._cmds[0].val, ())

    # set: some args
    def testSetArgs(self):
        req = pgfm.Req()
        req.set(0b1, pgfm.NONE, pgfm.ANY, "a", "b")
        self.assertEqual(req._set & 0b1, 0b1)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, 0b1)
        self.assertEqual(req._cmds[0].val, ("a", "b"))

    # set: req ONE
    def testSetReqOne(self):
        req = pgfm.Req()
        req._exp = 0b1
        req.set(0b1, pgfm.ONE, pgfm.ANY)
        self.assertEqual(req._exp & 0b1, 0)

    # set: let ONE
    def testSetLetOne(self):
        req = pgfm.Req()
        req.set(pgfm.DB, pgfm.NONE, pgfm.ONE)
        with self.assertRaises(pgfm.ErrReqSet) as c:
            req.set(pgfm.DB, pgfm.NONE, pgfm.ONE)
        str(c.exception)
    
    # set: let ANY
    def testSetLetAny(self):
        req = pgfm.Req()
        req.set(0b1, pgfm.NONE, pgfm.ANY)
        req.set(0b1, pgfm.NONE, pgfm.ANY)

    # isSet
    def testIsSet(self):
        req = pgfm.Req()
        req._set = 0b1
        self.assertTrue(req.isSet(0b1))

    # unset
    def testUnset(self):
        req = pgfm.Req()
        req._set = 0b1
        req.unset(0b1)
        self.assertEqual(req._set, 0)

    # ownCmds
    def testOwnCmds(self):
        req1 = pgfm.Req()
        req1.set(0b001, pgfm.NONE, pgfm.ANY, "a")
        req2 = pgfm.Req(req1)
        req2.set(0b010, pgfm.NONE, pgfm.ANY, "b")
        req2.set(0b100, pgfm.NONE, pgfm.ANY, "c")
        res = list(req2.ownCmds())
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].key, 0b010)
        self.assertEqual(res[0].val, ("b",))
        self.assertEqual(res[1].key, 0b100)
        self.assertEqual(res[1].val, ("c",))
        
    # allCmds
    def testAllCmds(self):
        req1 = pgfm.Req()
        req1.set(0b0001, pgfm.NONE, pgfm.ANY, "a")
        req1.set(0b0010, pgfm.NONE, pgfm.ANY, "b")
        req2 = pgfm.Req(req1)
        req2.set(0b0100, pgfm.NONE, pgfm.ANY, "c")
        req2.set(0b1000, pgfm.NONE, pgfm.ANY, "d")
        res = list(req2.allCmds())
        self.assertEqual(len(res), 4)
        self.assertEqual(res[0].key, 0b1000)
        self.assertEqual(res[0].val, ("d",))
        self.assertEqual(res[1].key, 0b0100)
        self.assertEqual(res[1].val, ("c",))
        self.assertEqual(res[2].key, 0b0010)
        self.assertEqual(res[2].val, ("b",))
        self.assertEqual(res[3].key, 0b0001)
        self.assertEqual(res[3].val, ("a",))

    class ReqXapi(pgfm.Req):
        Xapi = "val"
    class ReqDapi(pgfm.Req):
        Dapi = "val", "val" # Dapi format

    # rfmt: xml, first time
    def testRfmtXmlFirst(self):
        req = self.ReqXapi()
        rfmt = req.rfmt(pgfm.ApiXml)
        self.assertIsInstance(rfmt, pgfm.RfmtXapi)

    # rfmt: xml, next time
    def testRfmtXmlNext(self):
        req = self.ReqXapi()
        rfmt1 = req.rfmt(pgfm.ApiXml)
        rfmt2 = req.rfmt(pgfm.ApiXml)
        self.assertIs(rfmt1, rfmt2)

    # rfmt: xml, incompatible
    def testRfmtXmlErr(self):
        req = self.ReqDapi()
        with self.assertRaises(pgfm.ErrReqRfmtReqApi) as c:
            req.rfmt(pgfm.ApiXml)
        str(c.exception)

    # rfmt: data, first time
    def testRfmtDataFirst(self):
        req = self.ReqDapi()
        rfmt = req.rfmt(pgfm.ApiData)
        self.assertIsInstance(rfmt, pgfm.RfmtDapi)

    # rfmt: data, next time
    def testRfmtDataNext(self):
        req = self.ReqDapi()
        rfmt1 = req.rfmt(pgfm.ApiData)
        rfmt2 = req.rfmt(pgfm.ApiData)
        self.assertIs(rfmt1, rfmt2)

    # rfmt: data, incompatible
    def testRfmtDataErr(self):
        req = self.ReqXapi()
        with self.assertRaises(pgfm.ErrReqRfmtReqApi) as c:
            req.rfmt(pgfm.ApiData)
        str(c.exception)

    # rfmt: other
    def testRfmtOther(self):
        req = self.ReqXapi()
        with self.assertRaises(pgfm.ErrReqRfmtApi) as c:
            req.rfmt(pgfm.Api)
        str(c.exception)

    # All 'send' requests that do not raise an error will attempt to send an 
    # HTTP request and thus we enclose them into 'ReplReq'. This requires 
    # '.rfmt', 'Rfmt.httpReq', 'HttpReq.send' and 'RespSrv' to work.

    # send: incomplete
    def testSendIncompl(self):
        req = pgfm.Req()
        req._exp = 0b1
        srv = object()
        with self.assertRaises(pgfm.ErrReqSendExp) as c:
            req.send(srv, None, None, None)
        str(c.exception)

    class ReqSend1(pgfm.Req):
        Xapi = "-action"
        Dapi = "VERB", "path"
        Auth = "none"

    class ReqSend2(pgfm.Req):
        Xapi = "-action"
        Auth = "none"

    class ReqSend3(pgfm.Req):
        Dapi = "VERB", "path"
        Auth = "none"

    # send: explicit API, compatible.
    def testSendExplApi(self):
        req = self.ReqSend1()
        srv = pgfm.Srv("http://example.com")
        with ReplaceReq():
            resp = req.send(srv, None, None, pgfm.ApiXmlNew)
            self.assertIsInstance(resp, pgfm.RespSrv)
            self.assertIs(resp.httpResp.srv, srv)

    # send: explicit API, not compatible, XML/no XML.
    def testSendExplApiErr1(self):
        req = self.ReqSend3()
        srv = pgfm.Srv("http://example.com")
        with self.assertRaises(pgfm.ErrReqSendApi) as c:
            req.send(srv, None, None, pgfm.ApiXmlNew)
        str(c.exception)

    # send: explicit API, not compatible, Data/no Data.
    def testSendExplApiErr2(self):
        req = self.ReqSend2()
        srv = pgfm.Srv("http://example.com")
        with self.assertRaises(pgfm.ErrReqSendApi) as c:
            req.send(srv, None, None, pgfm.ApiDataLatest)
        str(c.exception)

    # send: explicit API, not compatible, ApiXmlLay.
    def testSendExplApiErr3(self):
        req = pgfm.ReqSrvDbs()
        srv = pgfm.Srv("http://example.com")
        with self.assertRaises(pgfm.ErrReqSendApi) as c:
            req.send(srv, None, None, pgfm.ApiXmlLay)
        str(c.exception)

    # send: explicit API, not compatible, ReqLayFmt.
    def testSendExplApiErr4(self):
        req = pgfm.ReqLayFmt().db("Db").lay("Lay")
        srv = pgfm.Srv("http://example.com")
        with self.assertRaises(pgfm.ErrReqSendApi) as c:
            req.send(srv, None, None, pgfm.ApiXmlNew)
        str(c.exception)

    # send: no explicit API, compatible default API.
    def testFoundApiDefault(self):
        req = self.ReqSend2() # only xml
        srv = pgfm.Srv("http://example.com", api=pgfm.ApiDataLatest)
        with ReplApi(pgfm.ApiXmlNew), ReplaceReq():
            resp = req.send(srv, None, None, None)
            self.assertIs(resp.api, pgfm.ApiXmlNew)
    
    # send: no explicit API, compatible server API.
    def testFoundApiServer(self):
        req = self.ReqSend2() # only xml
        srv = pgfm.Srv("http://example.com", api=pgfm.ApiXmlNew)
        session = srv.session("file", pgfm.User("name", "****"), 
                api=pgfm.ApiDataLatest)
        with ReplApi(pgfm.ApiXmlOld), ReplaceReq():
            resp = req.send(None, None, session, None)
            self.assertIs(resp.api, pgfm.ApiXmlNew)

    # send: no explicit API, compatible session API.
    def testFoundApiSession(self):
        req = self.ReqSend2() # only xml
        srv = pgfm.Srv("http://example.com", api=pgfm.ApiData1)
        session = srv.session("file", pgfm.User("name", "****"), 
                api=pgfm.ApiXmlNew)
        with ReplApi(pgfm.ApiData2), ReplaceReq():
            resp = req.send(None, None, session, None)
            self.assertIs(resp.api, pgfm.ApiXmlNew)

    # send: no explicit API, incompatible API, XML/no XML.
    def testFoundApiAutoXml(self):
        req = self.ReqSend2() # only xml
        srv = pgfm.Srv("http://example.com")
        with ReplApi(pgfm.ApiDataLatest), ReplaceReq():
            resp = req.send(srv, None, None, None)
            self.assertIs(resp.api, pgfm.ApiXmlNew)

    # send: no explicit API, incompatible API, Data/no Data.
    def testFoundApiAutoData(self):
        req = self.ReqSend3() # only Data
        srv = pgfm.Srv("http://example.com")
        with ReplApi(pgfm.ApiXmlNew), ReplaceReq():
            resp = req.send(srv, None, None, None)
            self.assertIs(resp.api, pgfm.ApiDataLatest)

    # send: no explicit API, ReqLayFmt.
    def testFoundApiAutoXmlLay(self):
        req = pgfm.ReqLayFmt().db("Db").lay("Lay")
        srv = pgfm.Srv("http://example.com")
        user = pgfm.User("abc", "***")
        with ReplApi(pgfm.ApiXmlNew), ReplaceReq():
            resp = req.send(srv, user, None, None)
            self.assertIs(resp.api, pgfm.ApiXmlLay)

    # send: no explicit API, ApiXmlLay.
    def testFoundApiAutoXmlNew(self):
        req = self.ReqSend1()
        srv = pgfm.Srv("http://example.com")
        with ReplApi(pgfm.ApiXmlLay), ReplaceReq():
            with self.assertWarns(UserWarning) as c:
                resp = req.send(srv, None, None, None)
            str(c.warning)
            self.assertIs(resp.api, pgfm.ApiXmlNew)

    # send: no auth.
    def testSendNoAuth(self):
        req = pgfm.ReqSrvInf()
        srv = pgfm.Srv("http://example.com")
        user = pgfm.User("abc", "***")
        with ReplaceReq():
            resp = req.send(srv, user, None, None)
        self.assertIs(resp.httpResp.auth, None)

    # send: cond auth, expl user.
    def testSendCondExpl(self):
        req = pgfm.ReqSrvDbs()
        srv = pgfm.Srv("http://example.com")
        user = pgfm.User("abc", "***")
        with ReplaceReq():
            resp = req.send(srv, user, None, None)
        self.assertIs(resp.httpResp.auth, user)

    # send: cond auth, no user.
    def testSendCondNoUser(self):
        req = pgfm.ReqSrvDbs()
        srv = pgfm.Srv("http://example.com")
        with ReplaceReq():
            resp = req.send(srv, None, None, None)
        self.assertIs(resp.httpResp.auth, None)

    # send: cond auth, session user.
    def testSendCondSess(self):
        req = pgfm.ReqSrvDbs()
        srv = pgfm.Srv("http://example.com")
        user = pgfm.User("abc", "***")
        session = srv.session("file", user)
        with ReplaceReq():
            resp = req.send(None, None, session, None)
        self.assertIs(resp.httpResp.auth, user)

    # send: cond auth, server user.
    def testSendCondServ(self):
        req = pgfm.ReqSrvDbs()
        user = pgfm.User("abc", "***")
        srv = pgfm.Srv("http://example.com", user)
        with ReplaceReq():
            resp = req.send(srv, None, None, None)
        self.assertIs(resp.httpResp.auth, user)

    # send: cond auth, default user.
    def testSendCondDflt(self):
        req = pgfm.ReqSrvDbs()
        user = pgfm.User("abc", "***")
        srv = pgfm.Srv("http://example.com")
        with ReplaceReq(), ReplUser(user):
            resp = req.send(srv, None, None, None)
        self.assertIs(resp.httpResp.auth, user)

    # send: mand auth, no user (XML).
    def testSendMandUserNone(self):
        req = pgfm.ReqDbLays().db("Db")
        srv = pgfm.Srv("http://example.com")
        with ReplaceReq():
            with self.assertRaises(pgfm.ErrReqSendAuth) as c:
                req.send(srv, None, None, None)
            str(c.exception)

    # send: mand auth, XML, expl user.
    def testSendMandXmlUserExpl(self):
        req = pgfm.ReqDbLays().db("Db")
        user = pgfm.User("abc", "***")
        srv = pgfm.Srv("http://example.com")
        with ReplaceReq():
            resp = req.send(srv, user, None, None)
        self.assertIs(resp.httpResp.auth, user)

    # send: mand auth, XML, session user.
    def testSendMandXmlUserSess(self):
        req = pgfm.ReqDbLays().db("Db")
        user = pgfm.User("abc", "***")
        srv = pgfm.Srv("http://example.com")
        session = srv.session("Db", user)
        with ReplaceReq():
            resp = req.send(None, None, session, pgfm.ApiXmlNew)
        self.assertIs(resp.httpResp.auth, user)

    # send: mand auth, XML, expl user.
    def testSendMandXmlUserServ(self):
        req = pgfm.ReqDbLays().db("Db")
        user = pgfm.User("abc", "***")
        srv = pgfm.Srv("http://example.com", user)
        with ReplaceReq():
            resp = req.send(srv, None, None, None)
        self.assertIs(resp.httpResp.auth, user)

    # send: mand auth, XML, default user.
    def testSendMandXmlUserDflt(self):
        req = pgfm.ReqDbLays().db("Db")
        user = pgfm.User("abc", "***")
        srv = pgfm.Srv("http://example.com", user)
        with ReplaceReq(), ReplUser(user):
            resp = req.send(srv, None, None, None)
        self.assertIs(resp.httpResp.auth, user)

    # send: mand auth, Data, no user.
    def testSendMandDataUserNone(self):
        req = pgfm.ReqDbLays().db("Db")
        srv = pgfm.Srv("http://example.com")
        with ReplaceReq():
            with self.assertRaises(pgfm.ErrReqSendAuth) as c:
                req.send(srv, None, None, pgfm.ApiDataLatest)
            str(c.exception)
    
    # send: mand auth, Data.
    def testSendMandData(self):
        req = pgfm.ReqDbLays().db("Db")
        user = pgfm.User("abc", "***")
        srv = pgfm.Srv("http://example.com")
        with ReplaceReq():
            with self.assertRaises(pgfm.ErrReqSendData) as c:
                req.send(srv, user, None, pgfm.ApiDataLatest)
            str(c.exception)

# ============================================================================

class TestReqCmn(unittest.TestCase):

    # lay2
    def testLay2(self):
        req = pgfm.ReqCmn()
        req.lay2("Lay2")
        self.assertTrue(req._set & pgfm.LAY2)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.LAY2)
        self.assertEqual(req._cmds[0].val, ("Lay2",))

    # par1
    def testPar1(self):
        req = pgfm.ReqCmn()
        req.par1("Par1")
        self.assertTrue(req._set & pgfm.PAR1)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.PAR1)
        self.assertEqual(req._cmds[0].val, ("Par1",))

    # par2
    def testPar2(self):
        req = pgfm.ReqCmn()
        req.par2("Par2")
        self.assertTrue(req._set & pgfm.PAR2)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.PAR2)
        self.assertEqual(req._cmds[0].val, ("Par2",))

    # scr1
    def testScr1(self):
        req = pgfm.ReqCmn()
        req.scr1("Scr1")
        self.assertTrue(req._set & pgfm.SCR1)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.SCR1)
        self.assertEqual(req._cmds[0].val, ("Scr1",))        

    # scr2
    def testScr2(self):
        req = pgfm.ReqCmn()
        req.scr2("Scr2")
        self.assertTrue(req._set & pgfm.SCR2)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.SCR2)
        self.assertEqual(req._cmds[0].val, ("Scr2",))

# ============================================================================

class TestReqCol(unittest.TestCase):
    
    # col: first.
    def testColFirst(self):
        req = pgfm.ReqCol()
        res = req.col(pgfm.NONE, "Col", "Val")
        self.assertIs(res, req)
        self.assertEqual(len(res._cmds), 1)
        self.assertEqual(res._cmds[0].key, pgfm.COL)
        self.assertEqual(res._cmds[0].val, ("Col", "Val"))
    
    # col: next, other (across requests).
    def testColNextOther(self):
        req1 = pgfm.ReqCol()
        req1.col(pgfm.NONE, "Col1", "Val")
        req2 = pgfm.ReqCol(req1)
        req2.col(pgfm.NONE, "Col2", "Val")

    # col: next, same (across requests).
    def testColNextSame(self):
        req1 = pgfm.ReqCol()
        req1.col(pgfm.NONE, "col", "val1")
        req2 = pgfm.ReqCol(req1)
        with self.assertRaises(pgfm.ErrReqColCol) as c:
            req2.col(pgfm.NONE, "COL", "VAL2") # ignore case
        str(c.exception)

# ============================================================================

class TestReqDb(unittest.TestCase):
    
    # db
    def testDb(self):
        req = pgfm.ReqDb()
        res = req.db("DB")
        self.assertIs(req, req)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.DB)
        self.assertEqual(req._cmds[0].val, ("DB",))
        self.assertEqual(req.file, "db") # ignore case

# ============================================================================

class TestReqFset(unittest.TestCase):
    
    # max
    def testMax(self):
        req = pgfm.ReqFset()
        res = req.max(12)
        self.assertIs(req, req)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.MAX)
        self.assertEqual(req._cmds[0].val, (12,))

    # skip
    def testSkip(self):
        req = pgfm.ReqFset()
        res = req.skip(34)
        self.assertIs(req, req)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.SKIP)
        self.assertEqual(req._cmds[0].val, (34,))

    # sort, basic
    def testSort(self):
        req = pgfm.ReqFset()
        res = req.sort("col", "order")
        self.assertIs(req, req)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.SORT)
        self.assertEqual(req._cmds[0].val, ("col", "order"))

    # sort, more than 9 steps
    def testSort10(self):
        req = pgfm.ReqFset()
        res = req.sort("f1", "order")
        res = req.sort("f2", "order")
        res = req.sort("f3", "order")
        res = req.sort("f4", "order")
        res = req.sort("f5", "order")
        res = req.sort("f6", "order")
        res = req.sort("f7", "order")
        res = req.sort("f8", "order")
        res = req.sort("f9", "order")
        res = req.sort("f10", "order") # no error

# ============================================================================

class TestReqLay(unittest.TestCase):
    
    # lay1
    def testLay1(self):
        req = pgfm.ReqLay()
        res = req.lay1("LAY")
        self.assertIs(req, req)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.LAY1)
        self.assertEqual(req._cmds[0].val, ("LAY",))

    # lay
    def testLay(self):
        self.assertIs(pgfm.ReqLay.lay, pgfm.ReqLay.lay1)

# ============================================================================

class TestReqMid(unittest.TestCase):
    
    # modid
    def testModid(self):
        req = pgfm.ReqMid()
        res = req.modid(123)
        self.assertIs(req, req)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.MODID)
        self.assertEqual(req._cmds[0].val, (123,))

# ============================================================================

class TestReqRid(unittest.TestCase):

    # recid
    def testRecid(self):
        req = pgfm.ReqRid()
        res = req.recid(123)
        self.assertIs(req, req)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.RECID)
        self.assertEqual(req._cmds[0].val, (123,))

class TestReqScr3(unittest.TestCase):
    
    # setPar: script not set.
    def testSetPar(self):
        req = pgfm.ReqScr3()
        res = req.setPar(pgfm.PAR1, pgfm.SCR1, 
            (None,
            "",
            "A",
            1,
            1.1,
            datetime.date(2023, 1, 15),
            datetime.time(12, 34, 56, 789000),
            datetime.timedelta(hours=12, minutes=34, seconds=56,
                milliseconds=789),
            datetime.datetime(2023, 1, 15, 12, 34, 56, 789000),
            [1, 2, 3],
            {"abc": "def"},
            pgfm.emptyVal,
            pgfm.Text("A"),
            pgfm.Number(123),
            pgfm.Date("1/15/2023"),
            pgfm.Time("12:34:56.789"),
            pgfm.Timestamp("1/15/2023", "12:34:56.789")))
        self.assertIs(res, req)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.PAR1)
        self.assertEqual(req._cmds[0].val[0].split("\r"),
            ["",
            "",
            "A",
            "1",
            "1.1",
            "1/15/2023",
            "12:34:56.789",
            "12:34:56.789",
            "1/15/2023 12:34:56.789",
            "[1, 2, 3]",
            '{"abc": "def"}',
            "",
            "A",
            "123",
            "1/15/2023",
            "12:34:56.789",
            "1/15/2023 12:34:56.789"])

    # setPar: script set.
    def testSetParScript(self):
        req = pgfm.ReqScr3()
        req._set = req._set | pgfm.SCR1
        self.assertFalse(req._exp & pgfm.SCR1)
        res = req.setPar(pgfm.PAR1, pgfm.SCR1, ("A",))
        self.assertFalse(req._exp & pgfm.SCR1)

    # par3
    def testPar3(self):
        req = pgfm.ReqScr3()
        req.par3("A")
        self.assertTrue(req._set & pgfm.PAR3)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.PAR3)
        self.assertEqual(req._cmds[0].val, ("A",))

    # par
    def testPar(self):
        self.assertIs(pgfm.ReqScr3.par, pgfm.ReqScr3.par3)

    # setScr
    def testSetScr(self):
        req = pgfm.ReqScr3()
        req.setScr(pgfm.SCR1, "Scr")
        self.assertTrue(req._set & pgfm.SCR1)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.SCR1)
        self.assertEqual(req._cmds[0].val, ("Scr",))

    # scr3
    def testScr3(self):
        req = pgfm.ReqScr3()
        req.scr3("Scr")
        self.assertTrue(req._set & pgfm.SCR3)
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.SCR3)
        self.assertEqual(req._cmds[0].val, ("Scr",))

    # scr
    def testScr(self):
        self.assertIs(pgfm.ReqScr3.scr, pgfm.ReqScr3.scr3)

# ============================================================================
# Tests for specific request types test initialization, allowed and required
# fields, methods specific to a single request ('ReqLaySel'), 'rfmt' for each
# API.
# ============================================================================

class TestReqDbLays(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqDbLays.rtyp, "dbLays")

    # Xapi
    def testXapi(self):
        self.assertTrue(hasattr(pgfm.ReqDbLays, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertTrue(hasattr(pgfm.ReqDbLays, "Dapi"))

    # auth
    def testExp(self):
        self.assertEqual(pgfm.ReqDbLays.Exp, pgfm.DB)

# ============================================================================

class TestReqDbScrs(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqDbScrs.rtyp, "dbScrs")

    # Xapi
    def testXapi(self):
        self.assertTrue(hasattr(pgfm.ReqDbScrs, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertTrue(hasattr(pgfm.ReqDbScrs, "Dapi"))

    # auth
    def testExp(self):
        self.assertEqual(pgfm.ReqDbScrs.Exp, pgfm.DB)

# ============================================================================

class TestReqLayAll(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqLayAll.rtyp, "recset")

    # Xapi
    def testXapi(self):
        self.assertTrue(hasattr(pgfm.ReqLayAll, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertTrue(hasattr(pgfm.ReqLayAll, "Dapi"))

    # Exp
    def testExp(self):
        self.assertEqual(pgfm.ReqLayAll.Exp, pgfm.DB + pgfm.LAY1)

# ============================================================================

class TestReqLayAny(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqLayAny.rtyp, "recset")

    # Xapi
    def testXapi(self):
        self.assertTrue(hasattr(pgfm.ReqLayAny, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertFalse(hasattr(pgfm.ReqLayAny, "Dapi"))

    # Exp
    def testExp(self):
        self.assertEqual(pgfm.ReqLayAny.Exp, pgfm.DB + pgfm.LAY1)

# ============================================================================

class TestReqLayFmt(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqLayFmt.rtyp, "layFmt")

    # Xapi
    def testXapi(self):
        self.assertTrue(hasattr(pgfm.ReqLayFmt, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertTrue(hasattr(pgfm.ReqLayFmt, "Dapi"))

    # Exp
    def testExp(self):
        self.assertEqual(pgfm.ReqLayFmt.Exp, pgfm.DB + pgfm.LAY1)

# ============================================================================

class TestReqLayInf(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqLayInf.rtyp, "layInf")

    # Xapi
    def testXapi(self):
        self.assertTrue(hasattr(pgfm.ReqLayInf, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertTrue(hasattr(pgfm.ReqLayInf, "Dapi"))

    # Exp
    def testExp(self):
        self.assertEqual(pgfm.ReqLayInf.Exp, pgfm.DB + pgfm.LAY1)

# ============================================================================

class TestReqLayNew(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqLayNew.rtyp, "recset")

    # Xapi
    def testXapi(self):
        self.assertTrue(hasattr(pgfm.ReqLayNew, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertTrue(hasattr(pgfm.ReqLayNew, "Dapi"))

    # Exp
    def testExp(self):
        self.assertEqual(pgfm.ReqLayNew.Exp, pgfm.DB + pgfm.LAY1)

    # col
    def testCol(self):
        req = pgfm.ReqLayNew()
        req.col("Col", "Val")
        self.assertEqual(req._cmds[-1].key, pgfm.COL)
        self.assertEqual(req._cmds[-1].val, ("Col", "Val"))

# ============================================================================

class TestReqLayOne(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqLayOne.rtyp, "recset")

    # Xapi
    def testXapi(self):
        self.assertTrue(hasattr(pgfm.ReqLayOne, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertTrue(hasattr(pgfm.ReqLayOne, "Dapi"))

    # Exp
    def testExp(self):
        self.assertEqual(pgfm.ReqLayOne.Exp, pgfm.DB + pgfm.LAY1 + pgfm.RECID)

# ============================================================================

class TestReqLayScr(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqLayScr.rtyp, "recset")

    # Xapi
    def testXapi(self):
        self.assertTrue(hasattr(pgfm.ReqLayScr, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertTrue(hasattr(pgfm.ReqLayScr, "Dapi"))

    # Exp
    def testExp(self):
        self.assertEqual(pgfm.ReqLayScr.Exp, pgfm.DB + pgfm.LAY1 + pgfm.SCR3)

# ============================================================================

class TestReqLaySel(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqLaySel.rtyp, "recset")

    # Xapi
    def testXapi(self):
        self.assertTrue(hasattr(pgfm.ReqLaySel, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertTrue(hasattr(pgfm.ReqLaySel, "Dapi"))

    # Exp
    def testExp(self):
        self.assertEqual(pgfm.ReqLaySel.Exp, pgfm.DB + pgfm.LAY1 + pgfm.REQ)

    # col: not set.
    def testColNotSet(self):
        req = pgfm.ReqLaySel()
        req.col("Col", "Val")
        self.assertEqual(req._cmds[-1].key, pgfm.COL)
        self.assertEqual(req._cmds[-1].val, ("Col", "Val"))

    # col: set, different.
    def testColSetDiff(self):
        req = pgfm.ReqLaySel()
        req.col("Col", "Val")
        req.col("Col2", "Val")
        self.assertEqual(req._cmds[-1].key, pgfm.COL)
        self.assertEqual(req._cmds[-1].val, ("Col2", "Val"))

    # col: set, same (across requests)
    def testColSetSame(self):
        req1 = pgfm.ReqLaySel()
        req1.col("Col", "Val1")
        req2 = req1.copy()
        with self.assertRaises(pgfm.ErrReqLaySelCol) as c:
            req2.col("Col", "Val2")
        str(c.exception)

    # col: set, same, different sample.
    def testColSetSameDiffSmpl(self):
        req = pgfm.ReqLaySel()
        req.col("Col", "Val1")
        req.req()
        req.col("Col", "Val1")

    # col: adds req.
    def testColAutoReq(self):
        req = pgfm.ReqLaySel()
        req.col("Col", "Val")
        self.assertEqual(len(req._cmds), 2)
        self.assertEqual(req._cmds[0].key, pgfm.REQ)
        self.assertEqual(req._cmds[0].val, ())
        self.assertEqual(req._cmds[1].key, pgfm.COL)
        self.assertEqual(req._cmds[1].val, ("Col", "Val"))

    # col: does not add req if added (across requests).
    def testColExplReq(self):
        req1 = pgfm.ReqLaySel()
        req1.req()
        req2 = req1.copy()
        req2.col("Col", "Val")
        self.assertEqual(len(req1._cmds), 1)
        self.assertEqual(req1._cmds[0].key, pgfm.REQ)
        self.assertEqual(req1._cmds[0].val, ())
        self.assertEqual(len(req2._cmds), 1)
        self.assertEqual(req2._cmds[0].key, pgfm.COL)
        self.assertEqual(req2._cmds[0].val, ("Col", "Val"))

    # omit: adds req.
    def testOmitImpl(self):
        req = pgfm.ReqLaySel()
        req.omit()
        self.assertEqual(len(req._cmds), 2)
        self.assertEqual(req._cmds[0].key, pgfm.REQ)
        self.assertEqual(req._cmds[0].val, ())
        self.assertEqual(req._cmds[1].key, pgfm.OMIT)
        self.assertEqual(req._cmds[1].val, ())

    # omit: does not add req if exists (acrosss requests).
    def testOmitExpl(self):
        req1 = pgfm.ReqLaySel()
        req1.req()
        req2 = req1.copy()
        req2.omit()
        self.assertEqual(len(req1._cmds), 1)
        self.assertEqual(req1._cmds[0].key, pgfm.REQ)
        self.assertEqual(req1._cmds[0].val, ())
        self.assertEqual(len(req2._cmds), 1)
        self.assertEqual(req2._cmds[0].key, pgfm.OMIT)
        self.assertEqual(req2._cmds[0].val, ())

    # req: adds sample.
    def testReq(self):
        req = pgfm.ReqLaySel()
        req.req()
        self.assertEqual(len(req._cmds), 1)
        self.assertEqual(req._cmds[0].key, pgfm.REQ)
        self.assertEqual(req._cmds[0].val, ())

    # req: does not add sample if the current one is empty
    def testReqErr(self):
        req = pgfm.ReqLaySel()
        req.req()
        with self.assertRaises(pgfm.ErrReqLaySelReq) as c:
            req.req()
        str(c.exception)

# ============================================================================

class TestReqRecDel(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqRecDel.rtyp, "recset")

    # Xapi
    def testXapi(self):
        self.assertTrue(hasattr(pgfm.ReqRecDel, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertTrue(hasattr(pgfm.ReqRecDel, "Dapi"))

    # Exp
    def testExp(self):
        self.assertEqual(pgfm.ReqRecDel.Exp, pgfm.DB + pgfm.LAY1 + pgfm.RECID)

# ============================================================================

class TestReqRecDup(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqRecDup.rtyp, "recset")

    # Xapi
    def testXapi(self):
        self.assertTrue(hasattr(pgfm.ReqRecDup, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertTrue(hasattr(pgfm.ReqRecDup, "Dapi"))

    # Exp
    def testExp(self):
        self.assertEqual(pgfm.ReqRecDup.Exp, pgfm.DB + pgfm.LAY1 + pgfm.RECID)

# ============================================================================

class TestReqRecUpd(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqRecUpd.rtyp, "recset")

    # Xapi
    def testXapi(self):
        self.assertTrue(hasattr(pgfm.ReqRecUpd, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertTrue(hasattr(pgfm.ReqRecUpd, "Dapi"))

    # Exp
    def testExp(self):
        self.assertEqual(pgfm.ReqRecUpd.Exp, pgfm.DB + pgfm.LAY1 + 
                pgfm.RECID + pgfm.COL)

# ============================================================================

class TestReqSrvDbs(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqSrvDbs.rtyp, "srvDbs")

    # Xapi
    def testXapi(self):
        self.assertTrue(hasattr(pgfm.ReqSrvDbs, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertTrue(hasattr(pgfm.ReqSrvDbs, "Dapi"))

    # auth
    def testAuth(self):
        self.assertEqual(pgfm.ReqSrvDbs.Auth, "cond")

# ============================================================================

class TestReqSrvInf(unittest.TestCase):

    # rtyp
    def testRtyp(self):
        self.assertEqual(pgfm.ReqSrvInf.rtyp, "srvInf")

    # Xapi
    def testXapi(self):
        self.assertFalse(hasattr(pgfm.ReqSrvInf, "Xapi"))

    # Dapi
    def testDapi(self):
        self.assertTrue(hasattr(pgfm.ReqSrvInf, "Dapi"))

    # auth
    def testAuth(self):
        self.assertEqual(pgfm.ReqSrvInf.Auth, "none")

# ============================================================================

class TestResp(unittest.TestCase):
    
    # __init__
    def testInit(self):
        req = object()
        api = object()
        resp = pgfm.Resp(req, api)
        self.assertIsInstance(resp, pgfm.Resp)
        self.assertIs(resp.req, req)
        self.assertIs(resp.api, api)

    # Resp subclasses have the 'error' attribute that can be None or an an 
    # instance of an Exception. If it is set, then reading fails raising that 
    # exception.
    
    class Resp(pgfm.Resp):
        def __init__(self, req=None, api=None, data=b"", error=None):
            super().__init__(req, api) 
            self.error = error
            self.data = data
    
    # read: error
    def TestReadErr(self):
        error = Exception()
        resp = self.RespSub(error=error)
        self.assertIs(resp.error, error)
        with self.assertRaises(Exception) as c:
            resp.read()
        self.assertIs(c.exception, error)

    # If a 'Resp' has an 'api' and 'req' it trusts 'api' to read the data and 
    # detect the FileMaker error, 'req' to determine the response type, and 
    # then 'api' to provide a method to read that type.
    
    class Api:
        def __init__(self, enum=0, estr=""):
            self.enum = enum
            self.estr = estr
        def read(self, rawData):
            return "readData", rawData
        def error(self, readData):
            return self.enum, self.estr
        def readRes(self, readData, *hints):
            return "readRes", readData, hints

    class Req:
        rtyp = "readRes"

    # read: with api, no error 
    def testReadApi(self):
        req = self.Req()
        api = self.Api()
        hints = object()
        resp = self.Resp(req, api)
        res = resp.read(hints)
        self.assertEqual(res, ("readRes", ("readData", b""), (hints,)))

    # read: with api, error
    def testReadApiErr(self):
        req = self.Req()
        api = self.Api(401, "Not found")
        resp = self.Resp(req, api)
        res = resp.read()
        self.assertIsInstance(res, pgfm.ErrFm)
        self.assertEqual(res.code, 401)
        self.assertEqual(res.text, "Not found")

    # When we read responses from disk we do not have API and request and have
    # to detect the format and derive the API and then guess the approximate 
    # response type. The code there uses hardcoded APIs and thus we have to 
    # test all possible combinations of the format and the underlying data. We
    # use the 
    
    # read: without api, old XML, error.
    def testReadOldXmlErr(self):
        res = self.Resp(data=XOLDERR).read()
        self.assertIsInstance(res, pgfm.ErrFm)
    
    # read: without api, old XML, SrvDbs.
    def testReadOldSrvDbs(self):
        res = self.Resp(data=XOLDSRVDBS).read()
        self.assertIsInstance(res, tuple)
        # TODO

    # read: without api, old XML, DbLays.
    def testReadOldDbLays(self):
        res = self.Resp(data=XOLDDBLAYS).read()
        self.assertIsInstance(res, list)
        # TODO

    # read: without api, old XML, DbScrs.
    def testReadOldDbScrs(self):
        res = self.Resp(data=XOLDDBSCRS).read()
        self.assertIsInstance(res, list)
        # TODO

    # read: without api, old XML, Lay.
    def testReadOldLay(self):
        res = self.Resp(data=XOLDLAYINF).read()
        self.assertIsInstance(res, pgfm.LaySpecXapiOld)

    # read: without api, old XML, Rset.
    def testReadOldRecset(self):
        res = self.Resp(data=XOLDLAYSEL).read()
        self.assertIsInstance(res, pgfm.Recset)

    # read: without api, new XML, error.
    def testReadNewXmlErr(self):
        res = self.Resp(data=XNEWERR).read()
        self.assertIsInstance(res, pgfm.ErrFm)

    # read: without api, new XML, SrvDbs.
    def testReadNewSrvDbs(self):
        res = self.Resp(data=XNEWSRVDBS).read()
        self.assertIsInstance(res, tuple)
        # TODO

    # read: without api, new XML, DbLays.
    def testReadNewDbLays(self):
        res = self.Resp(data=XNEWDBLAYS).read()
        self.assertIsInstance(res, list)
        # TODO

    # read: without api, new XML, DbScrs.
    def testReadNewDbScrs(self):
        res = self.Resp(data=XNEWDBSCRS).read()
        self.assertIsInstance(res, list)
        # TODO

    # read: without api, new XML, Lay.
    def testReadNewLay(self):
        res = self.Resp(data=XNEWLAYINF).read()
        self.assertIsInstance(res, pgfm.LaySpecXapiNew)

    # read: without api, new XML, Rset.
    def testReadNewRecset(self):
        res = self.Resp(data=XNEWLAYSEL).read()
        self.assertIsInstance(res, pgfm.Recset)

    # read: without api, Data (in progress)
    def testReadData1Err(self):
        with self.assertRaises(pgfm.ErrRespReadDataApi) as c:
            self.Resp(data="{}").read()
        str(c.exception)
        

    # read: without api, lay XML

    # read: without api, Data 1, error
    # read: without api, Data 1, SrvInf
    # ...
    # read: without api, Data 2, error
    # read: without api, Data 2, SrvInf
    # ...
    # read: without api, Data latest, error
    # read: without api, Data latest, SrvInf
    # ...

# ============================================================================

class TestRespDisk(unittest.TestCase):

    class File:
        def read(self):
            return b"abc"
    
    # __init__, normal
    def testInit(self):
        respDisk = pgfm.RespDisk(self.File())
        self.assertIsInstance(respDisk, pgfm.RespDisk)
        self.assertEqual(respDisk.data, b"abc")
        self.assertIsNone(respDisk.error)

    class FileErr:
        def read(self):
            raise Exception()

    # __init__, error
    def testInit(self):
        respDisk = pgfm.RespDisk(self.FileErr())
        self.assertIsInstance(respDisk, pgfm.RespDisk)
        self.assertEqual(respDisk.data, b"")
        self.assertIsInstance(respDisk.error, Exception)

# ============================================================================

class TestRespSrv(unittest.TestCase):
    
    # __init__.
    def testInit(self):
        req = object()
        api = object()
        httpResp = object()
        respSrv = pgfm.RespSrv(req, api, httpResp)
        self.assertIsInstance(respSrv, pgfm.RespSrv)
        self.assertIs(respSrv.req, req)
        self.assertIs(respSrv.api, api)
        self.assertIs(respSrv.httpResp, httpResp)

    class HttpResp:
        def __init__(self):
            self.data = object()
            self.error = object()

    # data & error
    def testDataError(self):
        httpResp = self.HttpResp()
        respSrv = pgfm.RespSrv(None, None, httpResp)
        self.assertIs(respSrv.data, httpResp.data)
        self.assertIs(respSrv.error, httpResp.error)

# ============================================================================

class TestRfmt(unittest.TestCase):
    
    # __init__: locks request
    def testInit(self):
       req = pgfm.ReqSrvDbs()
       self.assertFalse(req._lock)
       rfmt = req.rfmt(pgfm.ApiXmlOld)
       self.assertTrue(req._lock)

# ============================================================================

class TestRfmtDapi(unittest.TestCase):
    
    # __init__: works.
    def testInit(self):
        req = pgfm.ReqSrvInf()
        rfmt = req.rfmt(pgfm.ApiData1)
        self.assertIsInstance(rfmt, pgfm.RfmtDapi)

    # httpReq: SrvInf.
    def testHttpReq(self):
        req = pgfm.ReqSrvInf()
        httpReq = req.httpReq(pgfm.ApiData1)
        self.assertIsInstance(httpReq, pgfm.HttpReq)
        self.assertEqual(httpReq.verb, "GET")
        self.assertEqual(httpReq.path, "/fmi/data/v1/productInfo")
        self.assertIs(httpReq.data, None)

    # httpData: SrvDbs.
    def testHttpReq(self):
        req = pgfm.ReqSrvDbs()
        httpReq = pgfm.RfmtDapi(req).httpReq(pgfm.ApiData1)
        self.assertIsInstance(httpReq, pgfm.HttpReq)
        self.assertEqual(httpReq.verb, "GET")
        self.assertEqual(httpReq.path, "/fmi/data/v1/databases")
        self.assertIs(httpReq.data, None)

# ============================================================================

class TestRfmtXapi(unittest.TestCase):

    # The request format for the XML API is a Web form. During testing we need
    # to check whether the code creates a correct form. A form consists of
    # fields that may come in any order. (Technically I know the order, but
    # I do not want to rely on it.) To test a form we need to compare the
    # created fields with what we expect.
    #
    # FileMaker form fields may or may not have a value. If they have a value
    # then the value may be empty. The differences are that:
    #
    #   ...&foo=bar&...  field 'foo' has the value 'bar'.
    #   ...&foo=&...     field 'foo' has an empty value; it is empty.
    #   ...&foo&...      field 'foo' has no value; it is valueless.
    #
    # A FileMaker request always has a single valueless key that specifies the
    # action (such as '-dbnames') and zero or more fields with values, empty
    # or not. To make the test syntax more readable I merely list key-value
    # pairs and at the end put the single valueless form action, for example:
    #
    #    Check(rfmt, '-db', 'Db', '-layoutnames')

    def Check(self, req, *keys):
        "Test if the XML request has the specified key."
        # -> req: request, a subclass of Req.
        # -> keys: form keys, key-value pairs plus valueless action key,
        api = pgfm.ApiXmlOld
        httpReq = req.rfmt(api).httpReq(api)
        data = httpReq.data.decode("ascii")

        # By default Python 'parse_qs' ignores valueless and empty fields.
        # When we tell it to keep blank values, it represents values of such
        # fields with an empty string. Python assumes a key may repeat and
        # thus represents field values as a list of values. In FileMaker forms
        # keys do not repeat, so we always expect a single value.
        form = urllib.parse.parse_qs(data, keep_blank_values=True)
        # A form is never empty.
        i = 0; n = len(keys) - 1
        self.assertEqual(len(form), n / 2 + 1)
        while i < n:
            key = keys[i]
            i += 1
            val = keys[i]
            i += 1
            vals = form.get(key)
            self.assertIsInstance(vals, list)
            self.assertEqual(len(vals), 1) # always one value.
            self.assertEqual(vals[0], val)
        # Last valueless action key.
        vals = form.get(keys[n])
        self.assertEqual(len(vals), 1)
        self.assertEqual(vals[0], "")

    # __init__: calls parent __init__ and locks request.
    def testInit(self):
        req = pgfm.ReqSrvDbs()
        self.assertFalse(req._lock)
        rfmt = req.rfmt(pgfm.ApiXmlOld)
        self.assertTrue(req._lock)

    # __init__: complex request with base and query that spans two requests.
    def testInitBase(self):
        req1 = pgfm.ReqLaySel()
        req1.db("Db").lay("Lay").col("C1", "V1a").col("C2", "V2")
        req1.rfmt(pgfm.ApiXmlOld)
        req2 = req1.copy()
        req2.omit().req().col("C1", "V1b")
        self.Check(req2, 
                "-db", "Db", 
                "-lay", "Lay", 
                "-q1", "C1",
                "-q1.value", "V1a", 
                "-q2", "C2",
                "-q2.value", "V2", 
                "-q3", "C1", 
                "-q3.value", "V1b",
                "-query", "!(q1,q2);(q3)",
                "-findquery")

    # addKey: implicitly tested by numerous logical tests.
    # qreq: implicitly tested by numerous logical tests with search requests.

    # Normally we request the format from a request (with 'Req.rfmt'). The
    # request first checks if it is complete and then returns itself in the
    # specified format. A format merely reads the commands and renders them
    # as appropriate. It does not check the request because this is already
    # done. This means that we can test request formats using incomplete
    # requests.

    # List files.
    def testReqSrvDbs(self):
        req = pgfm.ReqSrvDbs()
        self.Check(req, "-dbnames")

    # List layouts.
    def testReqDbLays(self):
        req = pgfm.ReqDbLays().db("Db")
        self.Check(req, "-db", "Db", "-layoutnames")

    # List scripts.
    def testReqDbScrs(self):
        req = pgfm.ReqDbScrs().db("Db")
        self.Check(req, "-db", "Db", "-scriptnames")

    # View all records (only required parameters).
    def testReqLayAll(self):
        req = pgfm.ReqLayAll().db("Db").lay("Lay")
        self.Check(req, "-db", "Db", "-lay", "Lay", "-findall")

    # Start with random record (only required parameters).
    def testReqLayAll(self):
        req = pgfm.ReqLayAny().db("Db").lay("Lay")
        self.Check(req, "-db", "Db", "-lay", "Lay", "-findany")

    # Show a single record (only required parameters).
    def testReqLayOne(self):
        req = pgfm.ReqLayOne().db("Db").lay("Lay").recid(1)
        self.Check(req, "-db", "Db", "-lay", "Lay", "-recid", "1", "-find")

    # Run a script (only required parameters).
    def testReqLayScr(self):
        req = pgfm.ReqLayScr().db("Db").lay("Lay").scr("Scr")
        self.Check(req, "-db", "Db", "-lay", "Lay", "-script", "Scr",
                "-findany")

    # Search (only required parameters).
    def testReqLaySel(self):
        req = pgfm.ReqLaySel().db("Db").lay("Lay").col("Col", "Val")
        self.Check(req, "-db", "Db", "-lay", "Lay", "-query", "(q1)",
                "-q1", "Col", "-q1.value", "Val", "-findquery")

    # New record (only required parameters).
    def testReqLayNew(self):
        req = pgfm.ReqLayNew().db("Db").lay("Lay")
        self.Check(req, "-db", "Db", "-lay", "Lay", "-new")

    # Duplicate record (only required parameters).
    def testReqRecDup(self):
        req = pgfm.ReqRecDup().db("Db").lay("Lay").recid(1)
        self.Check(req, "-db", "Db", "-lay", "Lay", "-recid", "1", "-dup")

    # Update record (only required parameters).
    def testReqReqUpd(self):
        req = pgfm.ReqRecUpd().db("Db").lay("Lay").recid(1).col("Col", "Val")
        self.Check(req, "-db", "Db", "-lay", "Lay", "-recid", "1", "Col",
                "Val", "-edit")

    # Delete record (only required parameters).
    def testReqRecDel(self):
        req = pgfm.ReqRecDel().db("Db").lay("Lay").recid(1)
        self.Check(req, "-db", "Db", "-lay", "Lay", "-recid", "1", "-delete")

    # View layout information.
    def testReqLayInf(self):
        req = pgfm.ReqLayInf().db("Db").lay("Lay")
        self.Check(req, "-db", "Db", "-lay", "Lay", "-view")

    # Optional fields.

    # Using 'lay2' (with LayAll)
    def testLay2(self):
        req = pgfm.ReqLayAll().db("Db").lay("Lay").lay2("Lay2")
        self.Check(req, "-db", "Db", "-lay", "Lay", "-lay.response", "Lay2",
                "-findall")

    # Using 'max' (with LayAll).
    def testMax(self):
        req = pgfm.ReqLayAll().db("Db").lay("Lay").max(20)
        self.Check(req, "-db", "Db", "-lay", "Lay", "-max", "20", "-findall")

    # Using 'scr1' and 'par1' (with LayAll).
    def testScrPar1(self):
        req = pgfm.ReqLayAll().db("Db").lay("Lay").scr1("Scr").par1("Par")
        self.Check(req, "-db", "Db", "-lay", "Lay", "-script.prefind", "Scr",
                "-script.prefind.param", "Par", "-findall")

    # Using 'scr2' and 'par2' (with LayAll).
    def testScrPar2(self):
        req = pgfm.ReqLayAll().db("Db").lay("Lay").scr2("Scr").par2("Par")
        self.Check(req, "-db", "Db", "-lay", "Lay", "-script.presort", "Scr",
                "-script.presort.param", "Par", "-findall")

    # Using 'scr3' and 'par3' (with LayAll).
    def testScrPar3(self):
        req = pgfm.ReqLayAll().db("Db").lay("Lay").scr3("Scr").par3("Par")
        self.Check(req, "-db", "Db", "-lay", "Lay", "-script", "Scr",
                "-script.param", "Par", "-findall")

    # Using 'skip'' (with LayAll).
    def testSkip(self):
        req = pgfm.ReqLayAll().db("Db").lay("Lay").skip(40)
        self.Check(req, "-db", "Db", "-lay", "Lay", "-skip", "40", "-findall")

    # Using 'sort' (with LayAll).
    def testSort(self):
        req = pgfm.ReqLayAll().db("Db").lay("Lay").sort("Col", "asc")
        self.Check(req, "-db", "Db", "-lay", "Lay", "-sortfield.1", "Col",
                "-sortorder.1", "asc", "-findall")

    # Using 'modid' (with RecUpd).
    def testModid(self):
        req = pgfm.ReqRecUpd().db("Db").lay("Lay").recid(1).col("Col", "Val")
        req.modid(2)
        self.Check(req, "-db", "Db", "-lay", "Lay", "-recid", "1", "-modid",
                "2", "Col", "Val", "-edit")

    # Using maximal 'sort' steps (with LayAll).
    def testSortMax(self):
        req = pgfm.ReqLayAll().db("Db").lay("Lay")
        req.sort("f1", "asc")
        req.sort("f2", "desc")
        req.sort("f3", "Abc")
        req.sort("f4", "asc")
        req.sort("f5", "desc")
        req.sort("f6", "Def")
        req.sort("f7", "asc")
        req.sort("f8", "desc")
        req.sort("f9", "Ghi")
        self.Check(req, "-db", "Db", "-lay", "Lay",
                "-sortfield.1", "f1", "-sortorder.1", "asc",
                "-sortfield.2", "f2", "-sortorder.2", "desc",
                "-sortfield.3", "f3", "-sortorder.3", "Abc",
                "-sortfield.4", "f4", "-sortorder.4", "asc",
                "-sortfield.5", "f5", "-sortorder.5", "desc",
                "-sortfield.6", "f6", "-sortorder.6", "Def",
                "-sortfield.7", "f7", "-sortorder.7", "asc",
                "-sortfield.8", "f8", "-sortorder.8", "desc",
                "-sortfield.9", "f9", "-sortorder.9", "Ghi",
                "-findall")

    # Exceeding maximal 'sort' steps (with LayAll).
    def testSortErr(self):
        req = pgfm.ReqLayAll().db("Db").lay("Lay")
        req.sort("f1", "asc")
        req.sort("f2", "decs")
        req.sort("f3", "Abc")
        req.sort("f4", "asc")
        req.sort("f5", "desc")
        req.sort("f6", "Def")
        req.sort("f7", "asc")
        req.sort("f8", "desc")
        req.sort("f9", "Ghi")
        req.sort("f10", "asc")

        # It is OK to use more than 9 sort steps with a request, but such a
        # request cannot be sent via the XML API.
        with self.assertRaises(pgfm.ErrRfmtXapiSort) as c:
            req.rfmt(pgfm.ApiXmlOld)
        str(c.exception)

    # Using 'omit' (with LaySel).
    def testOmit(self):
        req = pgfm.ReqLaySel().db("Db").lay("Lay").col("Col", "Val").omit()
        self.Check(req, "-db", "Db", "-lay", "Lay", "-query", "!(q1)",
                "-q1", "Col", "-q1.value", "Val", "-findquery")

    # Using multiple fields and search requests (with LaySel).
    def testReq(self):
        req = pgfm.ReqLaySel().db("Db").lay("Lay")
        req.col("f1", "v1").col("f2", "v2").omit()
        req.req().col("f1", "v1").col("f2", "v2")
        self.Check(req, "-db", "Db", "-lay", "Lay", "-query",
                "!(q1,q2);(q3,q4)",
                "-q1", "f1", "-q1.value", "v1",
                "-q2", "f2", "-q2.value", "v2",
                "-q3", "f1", "-q3.value", "v1",
                "-q4", "f2", "-q4.value", "v2",
                "-findquery")

    # Requests to the old XML API go to 'FMPXMLRESULT.xml'.
    def testHttpReqOld(self):
        req = pgfm.ReqSrvDbs()
        api = pgfm.ApiXmlOld
        httpReq = req.rfmt(api).httpReq(api)
        self.assertEqual(httpReq.path, "/fmi/xml/FMPXMLRESULT.xml")

    # Requests to the new XML API go to 'fmresultset.xml'.
    def testHttpReqNew(self):
        req = pgfm.ReqSrvDbs()
        api = pgfm.ApiXmlNew
        httpReq = req.rfmt(api).httpReq(api)
        self.assertEqual(httpReq.path, "/fmi/xml/fmresultset.xml")

    # Requests to the layout XML API go to 'FMPXMLLAYOUT.xml'.
    def testHttpReqLay(self):
        req = pgfm.ReqLayFmt().db("Db").lay("Lay")
        api = pgfm.ApiXmlLay
        httpReq = req.rfmt(api).httpReq(api)
        self.assertEqual(httpReq.path, "/fmi/xml/FMPXMLLAYOUT.xml")

# ============================================================================

class TestRkey(unittest.TestCase):

    # The 'Rkey' class is removed from 'pgfm' after use, so we can only test
    # instances of 'Rkey'. They have known names and are unique single-bit 
    # integers suitable for a bitset.

    def test(self):
        fullSet = 0
        for name in ("COL", "DB", "LAY1", "LAY2", "MAX", "MODID", "OMIT",
                "PAR1", "PAR2", "PAR3", "RECID", "REQ", "SCR1", "SCR2",
                "SCR3", "SKIP", "SORT"):
            rkey = getattr(pgfm, name)
            self.assertIsInstance(rkey, int)
            self.assertEqual(rkey.name, name.lower())
            self.assertEqual(rkey & fullSet, 0) # unique
            fullSet = fullSet | rkey

# ============================================================================

class TestRow(unittest.TestCase):

    # The class has no methods.

    pass

# ============================================================================

class TestSel(unittest.TestCase):
    
    # __init__
    def testInit(self):
        sel = pgfm.Sel("abc", "def")
        self.assertEqual(sel.names, ("abc", "def"))
        self.assertIsNone(sel._spec)
        self.assertIsNone(sel._cols)
    
    class MockSrc:
        def __init__(self, spec):
            self.spec = spec

    class MockSpec:
        def _colSpecs(self, names):
            return self, names
        def _valsByColSpecs(self, src, colSpecs):
            return self, src, colSpecs
    
    # __call__: first
    def testCall(self):
        sel = pgfm.Sel("abc", "def")
        spec = self.MockSpec()
        src = self.MockSrc(spec)
        res = sel(src)
        self.assertIs(sel._spec, spec)
        self.assertEqual(sel._cols, (spec, ("abc", "def")))
        self.assertEqual(res, (spec, src, (spec, ("abc", "def"))))

    # __call__: same
    def testCallSame(self):
        sel = pgfm.Sel("abc", "def")
        spec = self.MockSpec()
        src1 = self.MockSrc(spec)
        src2 = self.MockSrc(spec)
        sel(src1)
        self.assertIs(sel._spec, spec)
        selCols = sel._cols
        sel(src2)
        self.assertIs(sel._spec, spec)
        self.assertIs(sel._cols, selCols)

    # __call__: changed
    def testCallDiff(self):
        sel = pgfm.Sel("abc", "def")
        spec1 = self.MockSpec()
        spec2 = self.MockSpec()
        src1 = self.MockSrc(spec1)
        src2 = self.MockSrc(spec2)
        sel(src1)
        self.assertIs(sel._spec, spec1)
        self.assertEqual(sel._cols, (spec1, ("abc", "def")))
        sel(src2)
        self.assertIs(sel._spec, spec2)
        self.assertEqual(sel._cols, (spec2, ("abc", "def")))

# ============================================================================

class TestSession(unittest.TestCase):

    # __init__: with user.
    def testInitUser(self):
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user)
        self.assertIs(session.user, user)

    # __init__: with API
    def testInitApi(self):
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        api = pgfm.ApiDataLatest
        session = pgfm.Session(srv, "file", user, api)
        self.assertIs(session.api, api)

    # __init__: with XML API (allowed).
    def testInitApiXml(self):
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        api = pgfm.ApiXmlOld
        session = pgfm.Session(srv, "file", user, api)
        self.assertIs(session.api, api)

    # __del__: logged in: logout. 
    def testDelActive(self):
        resp = MockReqResp(200, {"x-fm-data-access-token":"ABC"})
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user)
        with ReplaceReq(resp) as repl:
            session.login()
            self.assertEqual(len(repl), 1) # login request.
            del session # will logout.
        self.assertEqual(len(repl), 2) # login and logout requests.
        req2 = repl.req(1)
        self.assertEqual(req2.verb, "DELETE") # logout request

    # __del__ not logged in: no logout.
    def testDelInactive(self):
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user)
        with ReplaceReq() as repl:
            del session # will not log out
        self.assertEqual(len(repl), 0) # no requests are made.

    # __del__: logged out: no logout.
    def testDelInactive2(self):
        resp = MockReqResp(200, {"x-fm-data-access-token":"ABC"})
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user)
        with ReplaceReq(resp) as repl:
            session.login() # request 1
            session.logout()    # request 2
            del session         # no more requests
        self.assertEqual(len(repl), 2) # only two requests

    # When testing session login we have to both replace the HTTP sending
    # machinery and call 'logout' within this block. An active session will
    # automatically call 'logout' when garbage collected anyway so once it is
    # activated we need to deactivate it in a controlled manner. This is why 
    # all tests for 'login' explicitly call 'logout'.

    # __login__: basic, with explicit user.
    def testLoginLogout(self):
        resp = MockReqResp(200, {"x-fm-data-access-token":"TOK"})
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user)
        with ReplaceReq(resp) as repl:
            res = session.login()
            self.assertIs(res, session)
            self.assertIs(session.api, pgfm.ApiDataLatest)
            self.assertEqual(session.token, "TOK")
            self.assertEqual(session.authHdr, "bearer TOK")
            self.assertEqual(session.auth, "bearer TOK")
            session.logout()
            self.assertIsNone(session.api)
            self.assertIsNone(session.token)
            self.assertIsNone(session.authHdr)

        # First request.
        req = repl.req(0)
        self.assertEqual(req.verb, "POST")
        self.assertEqual(req.url,
                "url/fmi/data/vLatest/databases/file/sessions")
        self.assertEqual(req.data, b"{}")
        self.assertEqual(req.headers["content-type"], "application/json")
        self.assertEqual(req.headers["authorization"], user.auth)

        # Second request.
        req = repl.req(1)
        self.assertEqual(req.verb, "DELETE")
        self.assertEqual(req.url,
                "url/fmi/data/vLatest/databases/file/sessions/TOK")
        self.assertEqual(req.headers["authorization"], "bearer TOK")

    # __login__: cannot login if the explicit API is XML.
    def testLoginXml(self):
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user)
        api = pgfm.ApiXmlOld
        with self.assertRaises(pgfm.ErrSessionLoginApi) as c:
            session.login(api)
        str(c.exception)

    # __login__: can login with any data API.
    def testLoginData(self):
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        for api in (pgfm.ApiData1, pgfm.ApiData2, pgfm.ApiDataLatest):
            resp = MockReqResp(200, {"x-fm-data-access-token":"TOK"})
            session = pgfm.Session(srv, "file", user)
            with ReplApi(pgfm.ApiXmlOld), ReplaceReq(resp):
                try:
                    session.login(api)
                    self.assertIs(session.api, api)
                finally:
                    session.logout()

    # __login: if default APIs have no data API, pick latest Data API.
    def testLoginDataAuto(self):
        resp = MockReqResp(200, {"x-fm-data-access-token":"TOK"})
        srv = pgfm.Srv("url", api=pgfm.ApiXmlOld)
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user, pgfm.ApiXmlOld)
        with ReplApi(pgfm.ApiXmlOld), ReplaceReq(resp):
            try:
                session.login()
                self.assertIs(session.api, pgfm.ApiDataLatest) # auto
            finally:
                session.logout()

    #  __login__: pick the session API, if set.
    def testLoginDataSession(self):
        resp = MockReqResp(200, {"x-fm-data-access-token":"TOK"})
        srv = pgfm.Srv("url", api=pgfm.ApiData2)
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user, pgfm.ApiData1)
        with ReplApi(pgfm.ApiDataLatest), ReplaceReq(resp):
            try:
                session.login()
                self.assertIs(session.api, pgfm.ApiData1)
            finally:
                session.logout()

    #  __login__: pick the server API, if set.
    def testLoginDataServer(self):
        resp = MockReqResp(200, {"x-fm-data-access-token":"TOK"})
        srv = pgfm.Srv("url", api=pgfm.ApiData2)
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user, pgfm.ApiXmlOld)
        with ReplApi(pgfm.ApiDataLatest), ReplaceReq(resp):
            try:
                session.login()
                self.assertIs(session.api, pgfm.ApiData2)
            finally:
                session.logout()

    # login: pick the default API, if set.
    def testLoginDataGlobal(self):
        resp = MockReqResp(200, {"x-fm-data-access-token":"TOK"})
        srv = pgfm.Srv("url", api=pgfm.ApiXmlOld)
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user, pgfm.ApiXmlOld)
        with ReplApi(pgfm.ApiData1), ReplaceReq(resp):
            try:
                session.login()
                self.assertIs(session.api, pgfm.ApiData1)
            finally:
                session.logout()

    # __login__: if logged in, log out.
    def testLoginActive(self):
        resp1 = MockReqResp(200, {"x-fm-data-access-token":"ABC"})
        resp2 = MockReqResp()
        resp3 = MockReqResp(200, {"x-fm-data-access-token":"DEF"})
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user)
        with ReplaceReq(resp1, resp2, resp3) as repl:
            try:
                session.login()
                self.assertEqual(session.token, "ABC")
                session.login() # logs out first
                self.assertEqual(session.token, "DEF")
            finally:
                session.logout()
        self.assertEqual(len(repl.reqs), 4) # login/logout, two times.

    # __login__: if there is an HTTP error during login, will raise that error 
    # and won't make any changes.
    def testLoginErr(self):
        resp1 = MockReqResp(400)
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user)
        with ReplaceReq(resp1) as repl:
            with self.assertRaises(pgfm.ErrHttpResp):
                session.login()
            self.assertIsNone(session.token)

    # logout: basic.
    def testLogout(self):
        resp = MockReqResp(200, {"x-fm-data-access-token":"ABC"})
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user)
        with ReplaceReq(resp) as repl:
            session.login()
            session.logout()
        self.assertIsNone(session.api)
        self.assertIsNone(session.token)
        self.assertEqual(len(repl.reqs), 2)
        req = repl.reqs[1]
        self.assertEqual(req.verb, "DELETE")
        self.assertEqual(req.url, 
                "url/fmi/data/vLatest/databases/file/sessions/ABC")

    # logout: no action if not logged in..
    def testLogoutInactive(self):
        resp = MockReqResp(200, {"x-fm-data-access-token":"ABC"})
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user)
        with ReplaceReq(resp) as repl:
            session.logout()
        self.assertEqual(len(repl.reqs), 0)

    # logout: on error clear all fields and raise the error.
    def testLogoutErr(self):
        resp1 = MockReqResp(200, {"x-fm-data-access-token":"ABC"})
        resp2 = MockReqResp(400)
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user)
        with ReplaceReq(resp1, resp2) as repl:
            session.login()
            with self.assertRaises(pgfm.ErrHttpResp) as c:
                session.logout()
            str(c.exception)
        self.assertIsNone(session.token)
        self.assertIsNone(session.api)

    # api: return the session API when inactive, current API when active.
    def testApi(self):
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        api1 = pgfm.ApiData1
        api2 = pgfm.ApiData2
        self.assertIsNot(api1, api2)
        session = pgfm.Session(srv, "file", user, api1)
        self.assertIs(session.api, api1)
        resp = MockReqResp(200, {"x-fm-data-access-token":"ABC"})
        with ReplaceReq(resp) as repl:
            try:
                session.login(api=api2)
                self.assertIs(session.api, api2)
            finally:
                session.logout()
        self.assertIs(session.api, api1)

    # auth: automatically login if inactive.
    def testAuthInactive(self):
        resp1 = MockReqResp(200, {"x-fm-data-access-token":"ABC"})
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user)
        with ReplaceReq(resp1):
            try:
                session.auth
                self.assertEqual(session.token, "ABC")
            finally:
                session.logout()

    # auth: no login if already active.
    def testAuthActive(self):
        resp1 = MockReqResp(200, {"x-fm-data-access-token":"ABC"})
        srv = pgfm.Srv("url")
        user = pgfm.User("username", "password")
        session = pgfm.Session(srv, "file", user)
        with ReplaceReq(resp1) as repl:
            try:
                session.login()
                self.assertEqual(len(repl), 1) # single request
                session.auth
                self.assertEqual(len(repl), 1) # no more requests
            finally:
                session.logout()

    # The 'send' method simply calls 'req.send'.

    class Req:
        def send(self, srv, user, session, api):
            return "send", self, srv, user, session, api

    # send: basic
    def testSend(self):
        srv = object()
        user = object()
        session = pgfm.Session(srv, "Db", user)
        req = self.Req()
        res = session.send(req)
        self.assertEqual(res, ("send", req, None, None, session, None))

    # send: with api.
    def testSendApi(self):
        srv = object()
        user = object()
        api = object()
        session = pgfm.Session(srv, "Db", user)
        req = self.Req()
        res = session.send(req, api)
        self.assertEqual(res, ("send", req, None, None, session, api))

# ============================================================================

class TestSrv(unittest.TestCase):

    # A FileMaker server.

    # __init__: minimal.
    def testInit(self):
        srv = pgfm.Srv("https://example.com/")
        self.assertIsInstance(srv, pgfm.Srv)
        self.assertEqual(srv.url, "https://example.com") # no trailing '/'.
        self.assertIs(srv.verifySsl, True)
        self.assertIsInstance(repr(srv), str)

    # __init__: with user.
    def testInitUser(self):
        user = pgfm.User("username", "password")
        srv = pgfm.Srv("https://example.com/", user)
        self.assertIs(srv.user, user)
        self.assertIsInstance(repr(srv), str)

    # __init__: with API.
    def testInitApi(self):
        api = pgfm.ApiXmlOld
        srv = pgfm.Srv("https://example.com/", api=api)
        self.assertIs(srv.api, api)
        self.assertIsInstance(repr(srv), str)

    # __init__: without server identity verification.
    def testInitVerifySsl(self):
        srv = pgfm.Srv("https://example.com/", verifySsl=False)
        self.assertIs(srv.verifySsl, False)
        self.assertIsInstance(repr(srv), str)

    # session: no user.
    def testSessionNoUser(self):
        srv = pgfm.Srv("https://example.com/")
        with self.assertRaises(pgfm.ErrSrvSession) as c:
            srv.session("Db")
        str(c.exception)

    # session: server user.
    def testSessionSrvUser(self):
        user = object()
        srv = pgfm.Srv("https://example.com/", user=user)
        session = srv.session("Db")
        self.assertIsInstance(session, pgfm.Session)
        self.assertEqual(session.file, "db") # case-insensitive
        self.assertIs(session.user, user)
        self.assertIs(session.api, None)

    # session: explicit user.
    def testSessionExplUser(self):
        user1 = object()
        user2 = object()
        srv = pgfm.Srv("https://example.com/", user=user1)
        session = srv.session("Db", user2)
        self.assertIs(session.user, user2)

    # session: server api.
    def testSessionSrvApi(self):
        user = object()
        api = object()
        srv = pgfm.Srv("https://example.com/", api=api)
        session = srv.session("Db", user)
        self.assertIs(session.api, None) # does not copy

    # session: explicit api.
    def testSessionExplApi(self):
        user = object()
        api = object()
        srv = pgfm.Srv("https://example.com/")
        session = srv.session("Db", user, api)
        self.assertIs(session.api, api)

    # session: XML API (allowed)
    def testSessionExplApiXml(self):
        user = object()
        api = pgfm.ApiXmlNew
        srv = pgfm.Srv("https://example.com/")
        session = srv.session("Db", user, api)
        self.assertIs(session.api, api)

    # The 'send' method simply calls 'req.send'.

    class Req:
        def send(self, srv, user, session, api):
            return "send", self, srv, user, session, api

    # send
    def testSend(self):
        srv = pgfm.Srv("https://example.com")
        user = object()
        api = object()
        req = self.Req()
        res = srv.send(req, user, api)
        self.assertEqual(res, ("send", req, srv, user, None, api))

# ============================================================================

class TestText(unittest.TestCase):

    # FromStr: create from non-empty string.
    def testFromStr(self):
        val = pgfm.Text.FromStr("a")
        self.assertIsInstance(val, pgfm.Text)

    # FromStr: create from empty string.
    def testFromStrEmpty(self):
        val = pgfm.Text.FromStr("")
        self.assertIs(val, pgfm.emptyVal)

    # __new__: create from non-empty 'str'.
    def testNewStr(self):
        val = pgfm.Text("a")
        self.assertIsInstance(val, pgfm.Text)

    # __new__: create from empty 'str'.
    def testNewStrEmpty(self):
        val = pgfm.Text("")
        self.assertIs(val, pgfm.emptyVal)

    # __new__: create from another 'Text'.
    def testNewText(self):
        val1 = pgfm.Text("a")
        val2 = pgfm.Text(val1)
        self.assertIs(val1, val2)

    # __new__: create from 'None'.
    def testNewNone(self):
        val = pgfm.Text(None)
        self.assertIs(val, pgfm.emptyVal)

    # __new__: create from something else.
    def testNewErr(self):
        try:
            pgfm.Text(object())
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrTextNew)
            self.assertIsInstance(str(e), str)

    # __hash__: same for different case.
    def testHash(self):
        val1 = pgfm.Text("a")
        val2 = pgfm.Text("A")
        self.assertEqual(hash(val1), hash(val2))

    # cmpEx: testing via Python methods in 'Cmp', 'Val.cmp', 'cmpEx'.
    # compares lexicographically, ignores case, converts parameters.
    def cmpEx(self):
        val = pgfm.Text("b")
        self.assertNotEqual(val, "a")
        self.assertGreater(val, "a")
        self.assertGreaterEqual(val, "a")
        self.assertGreaterEqual(val, "B")
        self.assertEqual(val, "B")
        self.assertLessEqual(val, "B")
        self.assertLessEqual(val, "C")
        self.assertLess(val, "C")
        self.assertNotEqual(val, "C")

# ============================================================================

class TestTime(unittest.TestCase):

    # HmsToStr
    def testHmsToStr(self):
        val1 = pgfm.Time.HmsToStr(12, 34, 56.789)
        self.assertEqual(val1, "12:34:56.789")
        val2 = pgfm.Time.HmsToStr(2, 4, 6)
        self.assertEqual(val2, "2:04:06")

    # HmsToNum
    def testHmsToNum(self):
        val = pgfm.Time.HmsToNum(12, 34, 56.789)
        num = round(((12 * 60 + 34) * 60 + 56.789) * 1000000)
        self.assertEqual(val, num)

    # NumToHms
    def testNumToHms(self):
        num = round(((12 * 60 + 34) * 60 + 56.789) * 1000000)
        val = pgfm.Time.NumToHms(num)
        self.assertEqual(val, (12, 34, 56.789))

    # FromHms
    def testFromHms(self):
        val = pgfm.Time.FromHms(12, 34, 56.789)
        self.assertIsInstance(val, pgfm.Time)
        self.assertEqual(val, "12:34:56.789")

    # FromNum
    def testFromNum(self):
        num = (12 * 60 + 34) * 60 + 56.789
        val = pgfm.Time.FromNum(num)
        self.assertIsInstance(val, pgfm.Time)
        self.assertEqual(val, "12:34:56.789")

    # FromStr, non-empty.
    def testFromStr(self):
        val = pgfm.Time.FromStr("12:34:56.789")
        self.assertIsInstance(val, pgfm.Time)
        self.assertEqual(val.toHms(), (12, 34, 56.789))

    # FromStr, empty.
    def testFromStrEmpty(self):
        val = pgfm.Time.FromStr("")
        self.assertIs(val, pgfm.emptyVal)

    # FromPyTime
    def testFromPyTime(self):
        obj = datetime.time(12, 34, 56, 789000)
        val = pgfm.Time.FromPyTime(obj)
        self.assertIsInstance(val, pgfm.Time)
        self.assertEqual(val, "12:34:56.789")

    # FromPyDelta
    def testFromPyDelta(self):
        obj = datetime.timedelta(hours=12, minutes=34, seconds=56,
                milliseconds=789)
        val = pgfm.Time.FromPyDelta(obj)
        self.assertIsInstance(val, pgfm.Time)
        self.assertEqual(val, "12:34:56.789")

    # __new__: another instance.
    def testNewTime(self):
        val1 = pgfm.Time("12:34:56.789")
        val2 = pgfm.Time(val1)
        self.assertIs(val1, val2)

    # __new__: str, non-empty.
    def testFromStr(self):
        val = pgfm.Time("12:34:56.789")
        self.assertIsInstance(val, pgfm.Time)
        self.assertEqual(val.toHms(), (12, 34, 56.789))

    # __new__: str, empty.
    def testFromStrEmpty(self):
        val = pgfm.Time("")
        self.assertIs(val, pgfm.emptyVal)

    # __new__: number.
    def testNewNum(self):
        num = (12 * 60 + 34) * 60 + 56.789
        val = pgfm.Time(num)
        self.assertIsInstance(val, pgfm.Time)
        self.assertEqual(val, "12:34:56.789")

    # __new__: datetime.time
    def testNewPyTime(self):
        obj = datetime.time(12, 34, 56, 789000)
        val = pgfm.Time(obj)
        self.assertIsInstance(val, pgfm.Time)
        self.assertEqual(val, "12:34:56.789")

    # __new__: datetime.timedelta
    def testNewPyDelta(self):
        obj = datetime.timedelta(hours=12, minutes=34, seconds=56,
                milliseconds=789)
        val = pgfm.Time(obj)
        self.assertIsInstance(val, pgfm.Time)
        self.assertEqual(val, "12:34:56.789")

    # __new__: None
    def testNewNone(self):
        val = pgfm.Time(None)
        self.assertIs(val, pgfm.emptyVal)

    # __new__: h, m, s
    def testNewHms(self):
        val = pgfm.Time(12, 34, 56.789)
        self.assertIsInstance(val, pgfm.Time)
        self.assertEqual(val, "12:34:56.789")

    # __new__: other objects.
    def testNewErr1(self):
        try:
            pgfm.Time(object())
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrTimeNew)
            self.assertIsInstance(str(e), str)

    # __new__: wrong number of arguments.
    def testNewErr2(self):
        try:
            pgfm.Time(12, 34)
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrTimeNew)
            self.assertIsInstance(str(e), str)

    # __hash__: same for same time.
    def testHash(self):
        val1 = pgfm.Time("12:34:56.789")
        obj = datetime.time(12, 34, 56, 789000)
        val2 = pgfm.Time.FromPyTime(obj)
        self.assertEqual(hash(val1), hash(val2))

    # cmpEx: testing via Python methods in 'Cmp', 'Val.cmp', 'cmpEx'.
    # compares lexicographically, ignores case, converts parameters.
    def cmpEx(self):
        val = pgfm.Time("12:34:56.789")
        self.assertNotEqual(val, "2:34:56.789")
        self.assertGreater(val, "2:34:56.789")
        self.assertGreaterEqual(val, "2:34:56.789")
        self.assertGreaterEqual(val, "12:34:56.789")
        self.assertEqual(val, "12:34:56.789")
        self.assertLessEqual(val, "12:34:56.789")
        self.assertLessEqual(val, "12:35:56.789")
        self.assertLess(val, "12:35:56.789")
        self.assertNotEqual(val, "12:35:56.789")

    # toHms
    def testToHms(self):
        val = pgfm.Time("12:34:56.789")
        self.assertEqual(val.toHms(), (12, 34, 56.789))
        self.assertEqual(pgfm.Time(*val.toHms()), val)

    # toNum
    def testToNum(self):
        val = pgfm.Time("12:34:56.789")
        num = (12 * 60 + 34) * 60 + 56.789
        self.assertEqual(val.toNum(), num)
        self.assertEqual(pgfm.Time(val.toNum()), val)

    # toPyTime
    def testToPyTime(self):
        val = pgfm.Time("12:34:56.789")
        obj = datetime.time(12, 34, 56, 789000)
        self.assertEqual(val.toPyTime(), obj)
        self.assertEqual(pgfm.Time(val.toPyTime()), val)

    # toPyDelta
    def testToPyDelta(self):
        val = pgfm.Time("12:34:56.789")
        obj = datetime.timedelta(hours=12, minutes=34, seconds=56,
                milliseconds=789)
        self.assertEqual(val.toPyDelta(), obj)
        self.assertEqual(pgfm.Time(val.toPyDelta()), val)

    # toStr
    def testToStr(self):
        val = pgfm.Time(12, 34, 56.789)
        self.assertEqual(val.toStr(), "12:34:56.789")
        self.assertEqual(pgfm.Time(val.toStr()), val)

# ============================================================================

class TestTimestamp(unittest.TestCase):

   # FromDateTime
    def testFromDateTime(self):
        val = pgfm.Timestamp.FromDateTime("1/15/2023", "12:34:56.789")
        self.assertIsInstance(val, pgfm.Timestamp)
        self.assertEqual(val, "1/15/2023 12:34:56.789")

    # FromPyDatetime
    def testFromPyDatetime(self):
        obj = datetime.datetime(2023, 1, 15, 12, 34, 56, 789000)
        val = pgfm.Timestamp.FromPyDatetime(obj)
        self.assertIsInstance(val, pgfm.Timestamp)
        self.assertEqual(val, "1/15/2023 12:34:56.789")

    # FromStr: non-empty.
    def testFromStr(self):
        val = pgfm.Timestamp.FromStr("1/15/2023 12:34:56.789")
        self.assertIsInstance(val, pgfm.Timestamp)
        self.assertEqual(val.date, "1/15/2023")
        self.assertEqual(val.time, "12:34:56.789")

    # FromStr: empty.
    def testFromStrEmpty(self):
        val = pgfm.Timestamp.FromStr("")
        self.assertIs(val, pgfm.emptyVal)

    # __new__: Timestamp.
    def testNewTimestamp(self):
        val1 = pgfm.Timestamp("1/15/2023 12:34:56.789")
        val2 = pgfm.Timestamp(val1)
        self.assertIs(val1, val2)

    # __new__: str, non-empty
    def testNewStr(self):
        val = pgfm.Timestamp("1/15/2023 12:34:56.789")
        self.assertIsInstance(val, pgfm.Timestamp)
        self.assertEqual(val.date, "1/15/2023")
        self.assertEqual(val.time, "12:34:56.789")

    # __new__: str, empty.
    def testNewStrEmpty(self):
        val = pgfm.Timestamp("")
        self.assertIs(val, pgfm.emptyVal)

    # __new__: datetime.datetime
    def testNewPyDatetime(self):
        obj = datetime.datetime(2023, 1, 15, 12, 34, 56, 789000)
        val = pgfm.Timestamp(obj)
        self.assertIsInstance(val, pgfm.Timestamp)
        self.assertEqual(val, "1/15/2023 12:34:56.789")

    # __new__: None.
    def testNewNone(self):
        val = pgfm.Timestamp(None)
        self.assertIs(val, pgfm.emptyVal)

    # __new__: date, time.
    def testNewDateTime(self):
        val = pgfm.Timestamp("1/15/2023", "12:34:56.789")
        self.assertIsInstance(val, pgfm.Timestamp)
        self.assertEqual(val, "1/15/2023 12:34:56.789")

    # __new__: Y, M, D, h, m, s.
    def testNewYmdhms(self):
        val = pgfm.Timestamp(2023, 1, 15, 12, 34, 56.789)
        self.assertIsInstance(val, pgfm.Timestamp)
        self.assertEqual(val, "1/15/2023 12:34:56.789")

    # __new__: wrong type.
    def testNewErr1(self):
        try:
            pgfm.Timestamp(object())
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrTimestampNew)
            self.assertIsInstance(str(e), str)

    # __new__: wrong number of arguments.
    def testNewErr2(self):
        try:
            pgfm.Timestamp(2023, 1, 15)
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrTimestampNew)
            self.assertIsInstance(str(e), str)

    # __new__: wrong argument for date.
    def testNewErr3a(self):
        try:
            pgfm.Timestamp(None, "12:34:56.789")
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrTimestampFromDateTime)
            self.assertIsInstance(str(e), str)

    # __new__: wrong argument for time.
    def testNewErr3b(self):
        try:
            pgfm.Timestamp("1/15/2023", None)
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrTimestampFromDateTime)
            self.assertIsInstance(str(e), str)

    # date
    def testDate(self):
        val = pgfm.Timestamp("1/15/2023 12:34:56.789")
        self.assertIsInstance(val, pgfm.Timestamp)
        self.assertIsInstance(val.date, pgfm.Date)
        self.assertEqual(val.date, "1/15/2023")

    # time
    def testTime(self):
        val = pgfm.Timestamp("1/15/2023 12:34:56.789")
        self.assertIsInstance(val, pgfm.Timestamp)
        self.assertIsInstance(val.time, pgfm.Time)
        self.assertEqual(val.time, "12:34:56.789")

    # __hash__
    def testHash(self):
        val1 = pgfm.Timestamp(2023, 1, 15, 12, 34, 56.789)
        val2 = pgfm.Timestamp("1/15/2023", "12:34:56.789")
        self.assertEqual(hash(val1), hash(val2))

    # cmpEx: testing via Python methods in 'Cmp', 'Val.cmp', 'cmpEx'.
    # compares lexicographically, ignores case, converts parameters.
    def testCmpEx(self):
        val = pgfm.Timestamp("1/15/2023 12:34:56.789")
        cmpE = "1/15/2023 12:34:56.789"
        cmpL = "1/2/2023 12:34:56.789"
        cmpG = "1/10/2024 12:34:56.789"
        self.assertNotEqual(val, cmpL)
        self.assertGreater(val, cmpL)
        self.assertGreaterEqual(val, cmpL)
        self.assertGreaterEqual(val, cmpE)
        self.assertEqual(val, cmpE)
        self.assertLessEqual(val, cmpE)
        self.assertLessEqual(val, cmpG)
        self.assertLess(val, cmpG)
        self.assertNotEqual(val, cmpG)

    # toDateTime
    def testToDateTime(self):
        val = pgfm.Timestamp("1/15/2023 12:34:56.789")
        res = val.toDateTime()
        self.assertIsInstance(res, tuple)
        self.assertEqual(len(res), 2)
        self.assertIsInstance(res[0], pgfm.Date)
        self.assertEqual(res[0], "1/15/2023")
        self.assertIsInstance(res[1], pgfm.Time)
        self.assertEqual(res[1], "12:34:56.789")
        self.assertEqual(pgfm.Timestamp(*res), val)

    # testToPyDatetime
    def testToPyDatetime(self):
        val = pgfm.Timestamp("1/15/2023 12:34:56.789")
        obj = datetime.datetime(2023, 1, 15, 12, 34, 56, 789000)
        res = val.toPyDatetime()
        self.assertEqual(res, obj)
        self.assertEqual(pgfm.Timestamp(res), val)

# ============================================================================

class TestUser(unittest.TestCase):

    # __init__
    def testInit(self):
        user = pgfm.User("username", "password")
        self.assertIsInstance(user, pgfm.User)
        self.assertEqual(user.name, "username")
        self.assertIsInstance(user.auth, str)

        # Not testing for the contents of 'auth' as the test code will be a
        # mere reverse of our code and there is no standard code to unpack
        # the value.

# ============================================================================

class TestVal(unittest.TestCase):

    # 'Val' is a subclass of 'str'.
    def testSubclass(self):
        self.assertTrue(issubclass(pgfm.Val, str))

    # __new__: create from None, get 'emptyVal'.
    def testNewNone(self):
        a = pgfm.Val(None)
        self.assertIsInstance(a, pgfm.Val)
        self.assertIs(a, pgfm.emptyVal)

    # __new__: create from empty 'str', get 'emptyVal'.
    def testNewEmptyStr(self):
        a = pgfm.Val("")
        self.assertIsInstance(a, pgfm.Val)
        self.assertIs(a, pgfm.emptyVal)

    # __new__: empty values are the same object.
    def testNewNoneEmptyStr(self):
        a = pgfm.Val(None)
        b = pgfm.Val("")
        self.assertIs(a, b)

    # __new__: create from non-empty 'str', get 'Text'.
    def testNewStr(self):
        a = pgfm.Val("a")
        self.assertIsInstance(a, pgfm.Text)
        self.assertEqual(a, "A")

    # __new__: create from 'int', get 'Number'.
    def testNewInt(self):
        a = pgfm.Val(1)
        self.assertIsInstance(a, pgfm.Number)
        self.assertEqual(a, 1)

    # __new__: create from 'float', get 'Number'.
    def testNewFloat(self):
        a = pgfm.Val(1.2)
        self.assertIsInstance(a, pgfm.Number)
        self.assertEqual(a, 1.2)

    # __new__: create from Python date, get 'Date'.
    def testNewPyDate(self):
        a = pgfm.Val(datetime.date(2013, 1, 5))
        self.assertIsInstance(a, pgfm.Date)
        self.assertEqual(a, "1/5/2013")

    # __new__: create from Python time, get 'Time'.
    def testNewPyTime(self):
        a = pgfm.Val(datetime.time(12, 34, 56, microsecond=789000))
        self.assertIsInstance(a, pgfm.Time)
        self.assertEqual(a, "12:34:56.789")

    # __new__: create from Python timedelta, get 'Time'.
    def testNewPyDelta(self):
        a = pgfm.Val(datetime.timedelta(hours=12, minutes=34, seconds=56,
                milliseconds=789))
        self.assertIsInstance(a, pgfm.Time)
        self.assertEqual(a, "12:34:56.789")

    # __new__: create from Python datetime, get 'Timestamp'.
    def testNewPyDatetime(self):
        a = pgfm.Val(datetime.datetime(2013, 1, 5, 12, 34, 56,
                microsecond=789000))
        self.assertIsInstance(a, pgfm.Timestamp)
        self.assertEqual(a, "1/5/2013 12:34:56.789")

    # __new__: create from list, get 'Text' (JSON).
    def testNewList(self):
        obj = [1, 2, 3]
        val = pgfm.Val(obj)
        self.assertIsInstance(val, pgfm.Text)
        self.assertEqual(json.loads(val), obj)

    # __new__: create from dict, get 'Text' (JSON).
    def testNewDict(self):
        obj = dict(a=1, b=2, c=3)
        val = pgfm.Val(obj)
        self.assertIsInstance(val, pgfm.Text)
        self.assertEqual(json.loads(val), obj)

    # __new__: create from other, get an error.
    def testNewOther(self):
        try:
            pgfm.Val(object())
        except Exception as e:
            self.assertIsInstance(e, pgfm.ErrValNewType)
            self.assertIsInstance(str(e), str)

    # If the argument to '__new__' is 'emptyVal' or an instance of a subclass
    # of 'Val', it is returned as is.

    # __new__: create from 'emptyVal'.
    def testNewEmptyVal(self):
        val1 = pgfm.Val(pgfm.emptyVal)
        val2 = pgfm.Val(pgfm.emptyVal)
        self.assertIs(val1, val2)

    # __new__: create from 'Text'.
    def testNewText(self):
        val1 = pgfm.Text("A")
        val2 = pgfm.Val(val1)
        self.assertIs(val1, val2)

    # __new__: create from 'Number'.
    def testNewNumber(self):
        val1 = pgfm.Number(1)
        val2 = pgfm.Val(val1)
        self.assertIs(val1, val2)

    # __new__: create from 'Date'.
    def testNewDate(self):
        val1 = pgfm.Date("1/15/2023")
        val2 = pgfm.Val(val1)
        self.assertIs(val1, val2)

    # __new__: create from 'Time'.
    def testNewTime(self):
        val1 = pgfm.Time("12:34:56")
        val2 = pgfm.Val(val1)
        self.assertIs(val1, val2)

    # __new__: create from 'Timestamp'.
    def testNewTimestamp(self):
        val1 = pgfm.Timestamp("1/15/2023 12:34:56")
        val2 = pgfm.Val(val1)
        self.assertIs(val1, val2)

    # TODO: container?

    # '__new__' is also called as a part of creating instances of subclasses.
    # In these cases it simply creates a new instance from the passed string.
    # It is mostly tested in subclasses, so here we use a single sample with a
    # 'Number'.

    # __new__: called from a subclass.
    def testNewFromSubclass(self):
        val = pgfm.Number("1") # passing a string.
        self.assertIsInstance(val, pgfm.Number) # creates a number.
        self.assertEqual(val, "1")

    # __repr__: is printable.
    def testRepr(self):
        val = pgfm.Val("")
        self.assertIsInstance(repr(val), str)

    # 'Val' provides 'cmp' that handles comparison with empty values for all
    # subclasses. Non-empty values are compared using type-specific 'cmpEx'.
    # Here we test only comparison of empty values.

    # cmp: empty values are equal (of course; they are same).
    def testCmpEmpty(self):
        self.assertEqual(pgfm.emptyVal.cmp(pgfm.emptyVal), 0)

    # cmp: converts empty 'str' to 'emptyVal'.
    def testCmpEmptyStr(self):
        self.assertEqual(pgfm.emptyVal.cmp(""), 0)

    # cmp: converts 'None' to 'emptyVal'.
    def testCmpEmptyNone(self):
        self.assertEqual(pgfm.emptyVal.cmp(None), 0)

    # Non-empty values are always subclasses of 'Val'. They are always less
    # than an empty value.

    # cmp: 'emptyVal' and 'Text'.
    def testCmpEmptyText(self):
        val = pgfm.Text("a")
        self.assertEqual(pgfm.emptyVal.cmp(val), -1)

    # cmp: 'emptyVal' and 'Number'.
    def testCmpEmptyText(self):
        val = pgfm.Number(0)
        self.assertEqual(pgfm.emptyVal.cmp(val), -1)

    # cmp: 'emptyVal' and 'Date'.
    def testCmpEmptyText(self):
        val = pgfm.Date("1/15/2023")
        self.assertEqual(pgfm.emptyVal.cmp(val), -1)

    # cmp: 'emptyVal' and 'Time'.
    def testCmpEmptyText(self):
        val = pgfm.Time("12:34:56")
        self.assertEqual(pgfm.emptyVal.cmp(val), -1)

    # cmp: 'emptyVal' and 'Timestamp'.
    def testCmpEmptyText(self):
        val = pgfm.Container("1/15/2023 12:34:56")
        self.assertEqual(pgfm.emptyVal.cmp(val), -1)

    # TODO: container?

    # The 'toStr' method is a formal companion to 'FromStr' in subclasses.

    # toStr: gets the string (empty string for empty val).
    def testToStr(self):
        self.assertIsInstance(pgfm.emptyVal.toStr(), str)

# ============================================================================

class TestXfrm(unittest.TestCase):

    # __init__
    def test(self):
        xfrm = pgfm.Xfrm("A")
        self.assertIsInstance(xfrm, str)
        self.assertEqual(xfrm, "a")

# ============================================================================
# ============================================================================
# ============================================================================

# ============================================================================
# Sample FileMaker responses.

# Old XML format, error.

XOLDERR = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE FMPXMLRESULT PUBLIC "-//FMI//DTD FMPXMLRESULT//EN"
    "https://filemaker-staging.mitty.com/fmi/xml/FMPXMLRESULT.dtd">
<FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
    <ERRORCODE>401</ERRORCODE>
    <PRODUCT BUILD="3/16/2020" NAME="FileMaker Web Publishing Engine"
        VERSION="18.0.4.428"/>
    <DATABASE DATEFORMAT="" LAYOUT="" NAME="" RECORDS="0" TIMEFORMAT=""/>
    <METADATA/>
    <RESULTSET FOUND="0"/>
</FMPXMLRESULT>"""

# Old XML format, file names.

XOLDSRVDBS = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE FMPXMLRESULT PUBLIC "-//FMI//DTD FMPXMLRESULT//EN"
    "https://filemaker-staging.mitty.com/fmi/xml/FMPXMLRESULT.dtd">
<FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
    <ERRORCODE>0</ERRORCODE>
    <PRODUCT BUILD="3/16/2020" NAME="FileMaker Web Publishing Engine"
        VERSION="18.0.4.428"/>
    <DATABASE DATEFORMAT="" LAYOUT="" NAME="DBNAMES" RECORDS="3"
        TIMEFORMAT=""/>
    <METADATA>
        <FIELD EMPTYOK="NO" MAXREPEAT="1" NAME="DATABASE_NAME" TYPE="TEXT"/>
    </METADATA>
    <RESULTSET FOUND="3">
        <ROW MODID="0" RECORDID="0">
            <COL>
                <DATA>File 1</DATA>
            </COL>
        </ROW>
        <ROW MODID="0" RECORDID="0">
            <COL>
                <DATA>File 2</DATA>
            </COL>
        </ROW>
        <ROW MODID="0" RECORDID="0">
            <COL>
                <DATA>File 3</DATA>
            </COL>
        </ROW>
    </RESULTSET>
</FMPXMLRESULT>"""

# Old XML format, layout names. FileMaker does not preserve the hierarchy, but
# first outputs names of all layouts and separators and then adds a number of
# empty entries; these must be folders. By convention layout separators in
# FileMaker are actual layouts whose name is '-' (these layouts can even have
# elements).

XOLDDBLAYS = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE FMPXMLRESULT PUBLIC "-//FMI//DTD FMPXMLRESULT//EN"
    "https://filemaker-staging.mitty.com/fmi/xml/FMPXMLRESULT.dtd">
<FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
    <ERRORCODE>0</ERRORCODE>
    <PRODUCT BUILD="3/16/2020" NAME="FileMaker Web Publishing Engine"
        VERSION="18.0.4.428"/>
    <DATABASE DATEFORMAT="" LAYOUT="" NAME="mitty_webapi" RECORDS="157"
        TIMEFORMAT=""/>
    <METADATA>
        <FIELD EMPTYOK="NO" MAXREPEAT="1" NAME="LAYOUT_NAME" TYPE="TEXT"/>
    </METADATA>
    <RESULTSET FOUND="157">
        <ROW MODID="25" RECORDID="74">
            <COL>
                <DATA>Layout 1</DATA>
            </COL>
        </ROW>
        <ROW MODID="3" RECORDID="97">
            <COL>
                <DATA>Layout 2</DATA>
            </COL>
        </ROW>
        <ROW MODID="8" RECORDID="120">
            <COL>
                <DATA>-</DATA>
            </COL>
        </ROW>
        <ROW MODID="3" RECORDID="104">
            <COL>
                <DATA>Layout 3</DATA>
            </COL>
        </ROW>
        <ROW MODID="0" RECORDID="0">
            <COL>
                <DATA/>
            </COL>
        </ROW>
    </RESULTSET>
</FMPXMLRESULT>"""

# Old XML format, script names. Here FileMaker preserves the hierarchy. All
# entries go in prefix order using the following convention:

#  Abc   Normal script name
#  Abc  Script folder name. The '' is a Unicode character E001.
#  --   end of a script folder. The '' is a Unicode character E002.
#  -     separator

# In the sample below these characters are encoded in UTF-8:
#
# E001  ee8081  \xEE\x80\x81
# E002  ee8082  \xEE\x80\x82

XOLDDBSCRS = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE FMPXMLRESULT PUBLIC "-//FMI//DTD FMPXMLRESULT//EN" "https://filemaker-staging.mitty.com/fmi/xml/FMPXMLRESULT.dtd">
<FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
    <ERRORCODE>0</ERRORCODE>
    <PRODUCT BUILD="3/16/2020" NAME="FileMaker Web Publishing Engine" VERSION="18.0.4.428"/>
    <DATABASE DATEFORMAT="" LAYOUT="" NAME="mitty_webapi" RECORDS="7" TIMEFORMAT=""/>
    <METADATA>
        <FIELD EMPTYOK="NO" MAXREPEAT="1" NAME="SCRIPT_NAME" TYPE="TEXT"/>
    </METADATA>
    <RESULTSET FOUND="7">
        <ROW MODID="0" RECORDID="0">
            <COL>
                <DATA>\xEE\x80\x81Folder</DATA>
            </COL>
        </ROW>
        <ROW MODID="0" RECORDID="0">
            <COL>
                <DATA>Script 1</DATA>
            </COL>
        </ROW>
        <ROW MODID="0" RECORDID="0">
            <COL>
                <DATA>Script 2</DATA>
            </COL>
        </ROW>
        <ROW MODID="0" RECORDID="0">
            <COL>
                <DATA>-</DATA>
            </COL>
        </ROW>
        <ROW MODID="0" RECORDID="0">
            <COL>
                <DATA>\xEE\x80\x81Child Folder</DATA>
            </COL>
        </ROW>
        <ROW MODID="0" RECORDID="0">
            <COL>
                <DATA>\xEE\x80\x82--</DATA>
            </COL>
        </ROW>
        <ROW MODID="0" RECORDID="0">
            <COL>
                <DATA>\xEE\x80\x82--</DATA>
            </COL>
        </ROW>
    </RESULTSET>
</FMPXMLRESULT>"""

# Old XML format, layout information (or the response to a delete record).

XOLDLAYINF = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE FMPXMLRESULT PUBLIC "-//FMI//DTD FMPXMLRESULT//EN"
    "https://filemaker-staging.mitty.com/fmi/xml/FMPXMLRESULT.dtd">
<FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
    <ERRORCODE>0</ERRORCODE>
    <PRODUCT BUILD="3/16/2020" NAME="FileMaker Web Publishing Engine"
        VERSION="18.0.4.428"/>
    <DATABASE DATEFORMAT="MM/dd/yyyy" LAYOUT="Lay" NAME="Db" RECORDS="10"
            TIMEFORMAT="HH:mm:ss"/>
    <METADATA>
        <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="text" TYPE="TEXT"/>
        <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="number" TYPE="NUMBER"/>
        <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="date" TYPE="DATE"/>
        <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="time" TYPE="TIME"/>
        <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="timestamp" TYPE="TIMESTAMP"/>
        <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="container" TYPE="CONTAINER"/>
    </METADATA>
    <RESULTSET FOUND="0"/>
</FMPXMLRESULT>"""

# Old XML format, found set.

XOLDLAYSEL = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE FMPXMLRESULT PUBLIC "-//FMI//DTD FMPXMLRESULT//EN"
    "https://filemaker-staging.mitty.com/fmi/xml/FMPXMLRESULT.dtd">
<FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
    <ERRORCODE>0</ERRORCODE>
    <PRODUCT BUILD="3/16/2020" NAME="FileMaker Web Publishing Engine"
        VERSION="18.0.4.428"/>
    <DATABASE DATEFORMAT="MM/dd/yyyy" LAYOUT="Lay" NAME="DB" RECORDS="100"
            TIMEFORMAT="HH:mm:ss"/>
    <METADATA>
        <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="text" TYPE="TEXT"/>
        <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="number" TYPE="NUMBER"/>
        <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="date" TYPE="DATE"/>
        <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="time" TYPE="TIME"/>
        <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="timestamp" TYPE="TIMESTAMP"/>
        <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="container" TYPE="CONTAINER"/>
    </METADATA>
    <RESULTSET FOUND="10">
      <ROW MODID="2" RECORDID="1">
        <COL>
          <DATA>Text 1</DATA>
        </COL>
        <COL>
          <DATA>1</DATA>
        </COL>
        <COL>
          <DATA>1/13/2023</DATA>
        </COL>
        <COL>
          <DATA>12:34:56</DATA>
        </COL>
        <COL>
          <DATA>1/13/2023 12:34:56</DATA>
        </COL>
        <COL>
          <DATA />
        </COL>
      </ROW>
      <ROW MODID="4" RECORDID="3">
        <COL>
          <DATA />
        </COL>
        <COL>
          <DATA />
        </COL>
        <COL>
          <DATA />
        </COL>
        <COL>
          <DATA />
        </COL>
        <COL>
          <DATA />
        </COL>
        <COL>
          <DATA />
        </COL>
      </ROW>
    </RESULTSET>
</FMPXMLRESULT>"""

# New XML format, error.

XNEWERR = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE fmresultset PUBLIC "-//FMI//DTD fmresultset//EN"
    "https://filemaker-staging.mitty.com/fmi/xml/fmresultset.dtd">
<fmresultset xmlns="http://www.filemaker.com/xml/fmresultset" version="1.0">
    <error code="401"/>
    <product build="3/16/2020" name="FileMaker Web Publishing Engine"
        version="18.0.4.428"/>
    <datasource database="" date-format="" layout="" table="" time-format=""
        timestamp-format="" total-count="0"/>
    <metadata/>
    <resultset count="0" fetch-size="0"/>
</fmresultset>"""

# New XML format, file names.

XNEWSRVDBS = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE fmresultset PUBLIC "-//FMI//DTD fmresultset//EN"
    "https://filemaker-staging.mitty.com/fmi/xml/fmresultset.dtd">
<fmresultset xmlns="http://www.filemaker.com/xml/fmresultset" version="1.0">
    <error code="0"/>
    <product build="3/16/2020" name="FileMaker Web Publishing Engine"
        version="18.0.4.428"/>
    <datasource database="DBNAMES" date-format="" layout="" table=""
        time-format="" timestamp-format="" total-count="3"/>
    <metadata>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="DATABASE_NAME" not-empty="yes"
            numeric-only="no" result="text" time-of-day="no" type="normal"/>
    </metadata>
    <resultset count="3" fetch-size="3">
        <record mod-id="0" record-id="0">
            <field name="DATABASE_NAME">
                <data>File 1</data>
            </field>
        </record>
        <record mod-id="0" record-id="0">
            <field name="DATABASE_NAME">
                <data>File 2</data>
            </field>
        </record>
        <record mod-id="0" record-id="0">
            <field name="DATABASE_NAME">
                <data>File 3</data>
            </field>
        </record>
    </resultset>
</fmresultset>"""

# New XML, layout names. See the note for the old XML.

XNEWDBLAYS = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE fmresultset PUBLIC "-//FMI//DTD fmresultset//EN"
    "https://filemaker-staging.mitty.com/fmi/xml/fmresultset.dtd">
<fmresultset xmlns="http://www.filemaker.com/xml/fmresultset" version="1.0">
    <error code="0"/>
    <product build="3/16/2020" name="FileMaker Web Publishing Engine"
        version="18.0.4.428"/>
    <datasource database="mitty_webapi" date-format="" layout="" table=""
        time-format="" timestamp-format="" total-count="5"/>
    <metadata>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="LAYOUT_NAME" not-empty="yes"
            numeric-only="no" result="text" time-of-day="no" type="normal"/>
    </metadata>
    <resultset count="5" fetch-size="5">
        <record mod-id="25" record-id="74">
            <field name="LAYOUT_NAME">
                <data>Layout 1</data>
            </field>
        </record>
        <record mod-id="3" record-id="97">
            <field name="LAYOUT_NAME">
                <data>Layout 2</data>
            </field>
        </record>
        <record mod-id="8" record-id="120">
            <field name="LAYOUT_NAME">
                <data>-</data>
            </field>
        </record>
        <record mod-id="3" record-id="104">
            <field name="LAYOUT_NAME">
                <data>Layout 3</data>
            </field>
        </record>
        <record mod-id="0" record-id="0">
            <field name="LAYOUT_NAME">
                <data/>
            </field>
        </record>
    </resultset>
</fmresultset>"""

# New XML, script names. See the note for the old XML.

XNEWDBSCRS = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE fmresultset PUBLIC "-//FMI//DTD fmresultset//EN"
    "https://filemaker-staging.mitty.com/fmi/xml/fmresultset.dtd">
<fmresultset xmlns="http://www.filemaker.com/xml/fmresultset" version="1.0">
    <error code="0"/>
    <product build="3/16/2020" name="FileMaker Web Publishing Engine"
        version="18.0.4.428"/>
    <datasource database="mitty_webapi" date-format="" layout="" table=""
        time-format="" timestamp-format="" total-count="125"/>
    <metadata>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="SCRIPT_NAME" not-empty="yes"
            numeric-only="no" result="text" time-of-day="no" type="normal"/>
    </metadata>
    <resultset count="125" fetch-size="125">
        <record mod-id="0" record-id="0">
            <field name="SCRIPT_NAME">
                <data>\xEE\x80\x81Folder</data>
            </field>
        </record>
        <record mod-id="0" record-id="0">
            <field name="SCRIPT_NAME">
                <data>Script 1</data>
            </field>
        </record>
        <record mod-id="0" record-id="0">
            <field name="SCRIPT_NAME">
                <data>Script 2</data>
            </field>
        </record>
        <record mod-id="0" record-id="0">
            <field name="SCRIPT_NAME">
                <data>-</data>
            </field>
        </record>
        <record mod-id="0" record-id="0">
            <field name="SCRIPT_NAME">
                <data>\xEE\x80\x81Child Folder</data>
            </field>
        </record>
        <record mod-id="0" record-id="0">
            <field name="SCRIPT_NAME">
                <data>\xEE\x80\x82--</data>
            </field>
        </record>
        <record mod-id="0" record-id="0">
            <field name="SCRIPT_NAME">
                <data>\xEE\x80\x82--</data>
            </field>
        </record>
    </resultset>
</fmresultset>"""

# New XML, layout.

XNEWLAYINF = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE fmresultset PUBLIC "-//FMI//DTD fmresultset//EN"
    "https://filemaker-staging.mitty.com/fmi/xml/fmresultset.dtd">
<fmresultset xmlns="http://www.filemaker.com/xml/fmresultset" version="1.0">
    <error code="0"/>
    <product build="3/16/2020" name="FileMaker Web Publishing Engine"
        version="18.0.4.428"/>
    <datasource database="Db" date-format="MM/dd/yyyy" layout="Lay"
        table="Tbl" time-format="HH:mm:ss"
        timestamp-format="MM/dd/yyyy HH:mm:ss" total-count="10"/>
    <metadata>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="text" not-empty="no" numeric-only="no"
            result="text" time-of-day="no" type="normal"/>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="number" not-empty="no" numeric-only="no"
            result="number" time-of-day="no" type="normal"/>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="date" not-empty="no" numeric-only="no"
            result="date" time-of-day="no" type="normal"/>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="time" not-empty="no" numeric-only="no"
            result="time" time-of-day="no" type="normal"/>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="timestamp" not-empty="no" numeric-only="no"
            result="timestamp" time-of-day="no" type="normal"/>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="container" not-empty="no" numeric-only="no"
            result="container" time-of-day="no" type="normal"/>
    </metadata>
    <resultset count="0" fetch-size="0"/>
</fmresultset>"""

# New XML, layout.

XNEWLAYSEL = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE fmresultset PUBLIC "-//FMI//DTD fmresultset//EN"
    "https://filemaker-staging.mitty.com/fmi/xml/fmresultset.dtd">
<fmresultset xmlns="http://www.filemaker.com/xml/fmresultset" version="1.0">
    <error code="0"/>
    <product build="3/16/2020" name="FileMaker Web Publishing Engine"
        version="18.0.4.428"/>
    <datasource database="Db" date-format="MM/dd/yyyy" layout="Lay"
        table="Tbl" time-format="HH:mm:ss"
        timestamp-format="MM/dd/yyyy HH:mm:ss" total-count="100"/>
    <metadata>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="text" not-empty="no" numeric-only="no"
            result="text" time-of-day="no" type="normal"/>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="number" not-empty="no" numeric-only="no"
            result="number" time-of-day="no" type="normal"/>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="date" not-empty="no" numeric-only="no"
            result="date" time-of-day="no" type="normal"/>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="time" not-empty="no" numeric-only="no"
            result="time" time-of-day="no" type="normal"/>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="timestamp" not-empty="no" numeric-only="no"
            result="timestamp" time-of-day="no" type="normal"/>
        <field-definition auto-enter="no" four-digit-year="no" global="no"
            max-repeat="1" name="container" not-empty="no" numeric-only="no"
            result="container" time-of-day="no" type="normal"/>
    </metadata>
    <resultset count="10" fetch-size="2">
        <record mod-id="2" record-id="1">
            <field name="text">
                <data>Text 1</data>
            </field>
            <field name="number">
                <data>123</data>
            </field>
            <field name="date">
                <data>1/13/2023</data>
            </field>
            <field name="time">
                <data>12:34:56</data>
            </field>
            <field name="timestamp">
                <data>1/13/2023 12:34:56</data>
            </field>
            <field name="container">
                <data/>
            </field>
        </record>
        <record mod-id="4" record-id="3">
            <field name="text">
                <data/>
            </field>
            <field name="number">
                <data/>
            </field>
            <field name="date">
                <data/>
            </field>
            <field name="time">
                <data/>
            </field>
            <field name="timestamp">
                <data/>
            </field>
            <field name="container">
                <data/>
            </field>
        </record>
    </resultset>
</fmresultset>"""

# ============================================================================
# The data above are raw data. Some methods take parsed data.

def ParseXml(data):
    # -> data: XML data, bytes.
    # <- parsed XML.
    return lxml.etree.fromstring(data)

# ============================================================================
# In many tests we create a new layout. Layouts are cached and caching may
# interfere with testing. Here's a function to clear the cache.

def ClearLayCache():
    pgfm.Api.Lays.clear()




# ============================================================================
# RecsetXapiNew

# ============================================================================
# RecsetXapiOld





# ============================================================================
# Sample XML for the old XML format.

RespOldXmlA = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
  <FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
    <ERRORCODE>0</ERRORCODE>
    <PRODUCT BUILD="3/16/2020" NAME="FileMaker Web Publishing Engine" VERSION="18.0.4.428"/>
    <DATABASE DATEFORMAT="MM/dd/yyyy" LAYOUT="LNAM" NAME="FNAM" RECORDS="100" TIMEFORMAT="HH:mm:ss"/>
    <METADATA>
      <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="F1" TYPE="TEXT"/>
      <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="F2" TYPE="NUMBER"/>
      <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="F3" TYPE="DATE"/>
      <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="F4" TYPE="TIME"/>
      <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="F5" TYPE="TIMESTAMP"/>
      <FIELD EMPTYOK="YES" MAXREPEAT="2" NAME="T2::F6" TYPE="TEXT"/>
      <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="T3::F7" TYPE="TEXT"/>
      <FIELD EMPTYOK="YES" MAXREPEAT="2" NAME="T4::F8" TYPE="TEXT"/>
    </METADATA>
    <RESULTSET FOUND="10">
      <ROW MODID="2" RECORDID="1">
        <COL>
          <DATA>F1</DATA>
        </COL>
        <COL>
          <DATA>123</DATA>
        </COL>
        <COL>
          <DATA>1/13/2024</DATA>
        </COL>
        <COL>
          <DATA>12:34:56</DATA>
        </COL>
        <COL>
          <DATA>1/13/2024 12:34:56</DATA>
        </COL>
        <COL>
          <DATA>F6.C1</DATA>
          <DATA>F6.C2</DATA>
        </COL>
        <COL>
          <DATA>F7.R1</DATA>
          <DATA>F7.R2</DATA>
          <DATA>F7.R3</DATA>
        </COL>
        <COL>
          <DATA>F8.R1.C1</DATA>
          <DATA>F8.R1.C2</DATA>
          <DATA>F8.R2.C1</DATA>
          <DATA>F8.R2.C2</DATA>
          <DATA>F8.R3.C1</DATA>
          <DATA>F8.R3.C2</DATA>
        </COL>
      </ROW>
    </RESULTSET>
  </FMPXMLRESULT>"""

# Fields F7 and F8 are actually in the same portal to T3. FileMaker does not
# tell us this, so we have to provide this information manually.

RespOldXmlADesc = pgfm.LayDesc().rel("T3", "F7", "T4::F8")

RespOldXmlErr = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
  <FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
    <ERRORCODE>401</ERRORCODE>
    <PRODUCT BUILD="3/16/2020" NAME="FileMaker Web Publishing Engine" VERSION="18.0.4.428"/>
    <DATABASE DATEFORMAT="MM/dd/yyyy" LAYOUT="LNAM" NAME="FNAM" RECORDS="100" TIMEFORMAT="HH:mm:ss"/>
    <METADATA>
      <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="F1" TYPE="TEXT"/>
      <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="F2" TYPE="NUMBER"/>
      <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="F3" TYPE="DATE"/>
      <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="F4" TYPE="TIME"/>
      <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="F5" TYPE="TIMESTAMP"/>
      <FIELD EMPTYOK="YES" MAXREPEAT="2" NAME="T2::F6" TYPE="TEXT"/>
      <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="T3::F7" TYPE="TEXT"/>
      <FIELD EMPTYOK="YES" MAXREPEAT="2" NAME="T4::F8" TYPE="TEXT"/>
    </METADATA>
    <RESULTSET FOUND="0" />
  </FMPXMLRESULT>"""




# ============================================================================
# Sample response in the new XML format.

RespNewXmlA = b"""<?xml version="1.0" encoding="utf-8"?>
  <fmresultset xmlns="http://www.filemaker.com/xml/fmresultset" version="1.0">
    <error code="0"/>
    <product build="3/16/2020" name="FileMaker Web Publishing Engine"
        version="18.0.4.428"/>
    <datasource database="FNAM" date-format="MM/dd/yyyy" layout="LNAM"
        table="TNAM" time-format="HH:mm:ss"
        timestamp-format="MM/dd/yyyy HH:mm:ss" total-count="100"/>
    <metadata>
      <field-definition auto-enter="no" four-digit-year="no" global="no"
          max-repeat="2" name="T2::F6" not-empty="no" numeric-only="no"
          result="number" time-of-day="no" type="normal"/>
      <field-definition auto-enter="no" four-digit-year="no" global="no"
          max-repeat="1" name="F1" not-empty="no" numeric-only="no"
          result="text" time-of-day="no" type="normal"/>
      <field-definition auto-enter="no" four-digit-year="no" global="no"
          max-repeat="1" name="F2" not-empty="no" numeric-only="no"
          result="number" time-of-day="no" type="normal"/>
      <field-definition auto-enter="no" four-digit-year="no" global="no"
          max-repeat="1" name="F3" not-empty="no" numeric-only="no"
          result="date" time-of-day="no" type="normal"/>
      <field-definition auto-enter="no" four-digit-year="no" global="no"
          max-repeat="1" name="F4" not-empty="no" numeric-only="no"
          result="time" time-of-day="no" type="normal"/>
      <field-definition auto-enter="no" four-digit-year="no" global="no"
          max-repeat="1" name="F5" not-empty="no" numeric-only="no"
          result="timestamp" time-of-day="no" type="normal"/>
      <relatedset-definition table="T3">
        <field-definition auto-enter="yes" four-digit-year="no" global="no"
            max-repeat="2" name="T4::F8" not-empty="yes" numeric-only="no"
            result="text" time-of-day="no" type="normal"/>
        <field-definition auto-enter="yes" four-digit-year="no" global="no"
            max-repeat="1" name="T3::F7" not-empty="yes" numeric-only="no"
            result="text" time-of-day="no" type="normal"/>
      </relatedset-definition>
    </metadata>
    <resultset count="10" fetch-size="1">
      <record mod-id="2" record-id="1">
        <field name="T2::F6">
          <data>601</data>
          <data>602</data>
        </field>
        <field name="F1">
          <data>F1</data>
        </field>
        <field name="F2">
          <data>123</data>
        </field>
        <field name="F3">
          <data>1/13/2024</data>
        </field>
        <field name="F4">
          <data>12:34:56</data>
        </field>
        <field name="F5">
          <data>1/13/2024 12:34:56</data>
        </field>
        <relatedset count="2" table="T3">
          <record mod-id="4" record-id="3">
            <field name="T4::F8">
              <data>F8.R1.C1</data>
              <data>F8.R1.C2</data>
            </field>
            <field name="T3::F7">
              <data>F7.R1</data>
            </field>
          </record>
          <record mod-id="6" record-id="5">
            <field name="T4::F8">
              <data>F8.R2.C1</data>
              <data>F8.R2.C2</data>
            </field>
            <field name="T3::F7">
              <data>F7.R2</data>
            </field>
          </record>
        </relatedset>
      </record>
    </resultset>
  </fmresultset>
"""

RespNewXmlALxml = pgfm.LxmlFromstring(RespNewXmlA)

# Sample response with an error.

RespNewXmlErr = b"""<?xml version="1.0" encoding="utf-8"?>
  <fmresultset xmlns="http://www.filemaker.com/xml/fmresultset" version="1.0">
    <error code="401"/>
    <product build="3/16/2020" name="FileMaker Web Publishing Engine"
        version="18.0.4.428"/>
    <datasource database="FNAM" date-format="MM/dd/yyyy" layout="LNAM"
        table="TNAM" time-format="HH:mm:ss"
        timestamp-format="MM/dd/yyyy HH:mm:ss" total-count="100"/>
    <metadata>
      <field-definition auto-enter="no" four-digit-year="no" global="no"
          max-repeat="2" name="T2::F6" not-empty="no" numeric-only="no"
          result="number" time-of-day="no" type="normal"/>
      <field-definition auto-enter="no" four-digit-year="no" global="no"
          max-repeat="1" name="F1" not-empty="no" numeric-only="no"
          result="text" time-of-day="no" type="normal"/>
      <field-definition auto-enter="no" four-digit-year="no" global="no"
          max-repeat="1" name="F2" not-empty="no" numeric-only="no"
          result="number" time-of-day="no" type="normal"/>
      <field-definition auto-enter="no" four-digit-year="no" global="no"
          max-repeat="1" name="F3" not-empty="no" numeric-only="no"
          result="date" time-of-day="no" type="normal"/>
      <field-definition auto-enter="no" four-digit-year="no" global="no"
          max-repeat="1" name="F4" not-empty="no" numeric-only="no"
          result="time" time-of-day="no" type="normal"/>
      <field-definition auto-enter="no" four-digit-year="no" global="no"
          max-repeat="1" name="F5" not-empty="no" numeric-only="no"
          result="timestamp" time-of-day="no" type="normal"/>
      <relatedset-definition table="T3">
        <field-definition auto-enter="yes" four-digit-year="no" global="no"
            max-repeat="2" name="T4::F8" not-empty="yes" numeric-only="no"
            result="text" time-of-day="no" type="normal"/>
        <field-definition auto-enter="yes" four-digit-year="no" global="no"
            max-repeat="1" name="T3::F7" not-empty="yes" numeric-only="no"
            result="text" time-of-day="no" type="normal"/>
      </relatedset-definition>
    </metadata>
    <resultset count="0" fetch-size="0" />
  </fmresultset>
"""

# ============================================================================


DATA_2_SRVINF = b"""
  {
    "response":
    {
      "productInfo":
      {
        "name"           : "FileMaker Data API Engine",
        "buildDate"      : "03/16/2020",
        "version"        : "18.0.4.428",
        "dateFormat"     : "MM/dd/yyyy",
        "timeFormat"     : "HH:mm:ss",
        "timeStampFormat": "MM/dd/yyyy HH:mm:ss"
      }
    },
   "messages":
   [
     {
       "code":"0",
       "message":"OK"
     }
   ]
  }"""

# ============================================================================
# When testing 'RespDisk' we need file-like object that would raise an error
# on 'read()'.

class MockFile:

    def __enter__(self):
        return self

    def __exit__(self, cls, val, trc):
        pass

    def read(self):
        "Imitate reading."
        raise IOError()

# When testing 'ColSpec' and such we need to pass them 'Rec', 'Row', 'Recset'
# and 'Rel' objects. All these objects share the same interface: they have the
# 'data' property that stores the relevant data in a format opaque to the
# object itself. Then whatever object handles this 'Rec' or 'Row' takes that
# data and processes it as appropriate.

class MockDataHolder:

    def __init__(self, *data):
        self.data = data

# When testing code that sends HTTP requests we need to prevent actual HTTP
# requests from being sent and sometimes orchestrate responses. To do that we
# use a mock object to represent responses we get from the underlying HTTP
# module ('requests') and code that temporarily replaces that HTTP module in
# 'pgfm'. The intended usage is that:
#
#   with ReplaceReq():
#     <testCode>
#
# Here 'ReplaceReq' temporarily alters the HTTP sending machinery in 'pgfm' so
# that the each call will return a new 'MockReqResp' with status 200. We can
# also specify exactly what to return:
#
#   resp1 = MockReqResp(204, "No content")
#   resp2 = MockReqResp(404, "Not found")
#   with ReplaceReq(resp1, resp2):
#      <test code>
#
# Here the first two HTTP responses will be 'resp1' and 'resp2' and then the
# code will continue as above.

class MockReqReq:
    # Stores the received arguments for inspection.

    # verb: received verb, str.
    # url: received URL, str.
    # headers: received headers, {str:str}.
    # data: received data, bytes or None.
    # verifySsl: received indication whether to verify the server, bool.

    def __init__(self, verb, url, headers, data, verifySsl):
        self.verb = verb
        self.url = url
        self.headers = headers
        self.data = data
        self.verifySsl = verifySsl

class MockReqResp:
    # Imitates the result received from 'requests.request'.

    def __init__(self, code=200, headers={}, content=None):
        self.status_code = code
        self.headers = headers
        self.content = content

class ReplaceReq:
    # Replaces 'requests.request' in 'pgfm'.

    # reqs: requests log, [MockReqReq].
    # resps: a list of responses to return, [MockReqResp].
    # nextResp: next response, int.
    # oldReqReq: the original 'requests.request'.

    def __init__(self, *resps):
        # -> resps: responses to return, MockReqResp*.
        self.reqs = []
        self.resps = resps
        self.nextResp = 0

    def mock(self, verb, url, headers, data, verify):
        "Imitate a call to 'requests.request' (limited)."
        # -> verb: HTTP verb, str.
        # -> url: URL, str.
        # -> headers: HTTP headers, {str:str}.
        # -> data: data, bytes or None.
        # -> verify: whether to verify the server, bool.
        # <- response, MockReqResp.

        # Store the request for inspection.
        self.reqs.append(MockReqReq(verb, url, headers, data, verify))

        # Respond.
        if self.nextResp < len(self.resps):
            # Use a prepared response.
            resp = self.resps[self.nextResp]
            self.nextResp += 1
        else:
            # Use a default response.
            resp = MockReqResp()
        return resp

    def req(self, idx):
        "Get the specified request."
        # -> idx: request index, int.
        # <- request, MockReqReq.
        return self.reqs[idx]

    def __len__(self):
        "Get the number of requests."
        # <- number of requests, int.
        return len(self.reqs)

    def __enter__(self):
        "Replace 'requests.request' in 'pgfm'."
        # <- self.
        self.oldReqReq = pgfm.ReqReq
        pgfm.ReqReq = self.mock
        return self

    def __exit__(self, cls, val, trc):
        "Restore 'requests.request' in 'pgfm'."
        pgfm.ReqReq = self.oldReqReq

# 'pgfm' always sets the default API and may set the may set the default user.
# During testing we may need to temporarily replace these objects. Usage:
#
#    user = pgfm.User(...)
#    with ReplApi(pgfm.ApiXmlNew), ReplUser(user):
#       <test code>
#
# This will temporarily set 'defaultApi' to 'ApiXmlNew' and 'defaultUser'
# to the passed 'user'.

class ReplApi:

    # api     : the API to install, Api.
    # _oldApi : the previous API, None/Api.

    def __init__(self, api):
        # -> api: the API to install, Api.
        self.api = api
        self._oldApi = None

    def __enter__(self):
        # <- self
        self._oldApi = pgfm.defaultApi
        pgfm.defaultApi = self.api
        return self

    def __exit__(self, cls, val, trc):
        pgfm.defaultApi = self._oldApi

class ReplUser:

    # usr     : the user to install, User/None.
    # _oldUsr : the previous user, None/User.

    def __init__(self, usr):
        # -> usr: the User to install, User/None.
        self.usr = usr
        self._oldUsr = None

    def __enter__(self):
        # <- self
        self._oldUsr = pgfm.defaultUser
        pgfm.defaultUser = self.usr
        return self

    def __exit__(self, cls, val, trc):
        pgfm.defaultUser = self._oldUsr

# Layout specifications may be cached in the global cache. We normally need to
# clear the cache after testing.

class ReplLays:

    def __init__(self):
        self.lays = {}

    def __enter__(self):
        return self

    def __exit__(self, cls, val, trc):
        self.lays.update(pgfm.Api.Lays)
        pgfm.Api.Lays.clear()


#-----------------------------------------------------------------------------
# When the code reads the response it stores the data in an intermediate
# format. The format is specific to the way the data is organized in the
# response, so that it uses fewer transformations to read the data, but
# otherwise it tries to be as basic as possible.
#
# To test the code we need samples in that internal format for old and new XML
# APIs. In both cases we imitate a found set with two records. The layout has
# two fields on the layout and a portal with two fields. One file on the
# layout and in the portal has two repetitions. In the second record the
# portal is empty. Record IDs go from 1 to 2. Portal record IDs go from 21 to
# 22. Record versions are record ID + 100: 101, 102, etc.

# For the old XML format we keep two lists. One list stores record data:
#
#   [ <record 1>, ..., <record N> ]
#
# Here and below everything in '<>' indicates not an object, but a sequence
# of values. Each <record> sequence in the list stores metadata and field
# data:
#
#   ..., <metadata>, <data for field 1> ..., <data for field N>, ...
#
# The metadata consist of two values, internal version and ID. The field
# data consist of zero or more values. If a field is on a layout, then it
# has one value for each repetition. If a field is in a portal, then it
# has one value for each repetition for each portal row. If there are no
# rows in the portal, the field will have zero values. But it will still
# be mapped in the map.
#
# The map is a list of addresses of the values in the first list. Let's
# picture the values in the list so:
#
#   [ <r1m> <r1f1> <r1f2> <r1f3> <r2m> <r2f1> <r2f2> <r2f3> ... <rNf3> ]
#
# Here 'm' entries consist are metadata of two numbers and field entries
# consist of varying number of cells. The map stores addresses of gaps between
# these entries. The first entry in the map is always 0, the second is 2 (two
# integers of the metadata entry) and then it varies.

OLDVS = [ 101, 1,                                          # record 1
          "r1f1",                                          # field 1
          "r1f2c1", "r1f2c2",                              # field 2
          "r1f3p1", "r1f3p2",                              # field 3
          "r1f4c1p1", "r1f4c2p1", "r1f4c1p2", "r1f4c2p2" , # field 4
          102, 2,                                          # record 2
          "r2f1",                                          # field 1
          "r2f2c1", "r2f2c2"                               # field 2
                                                           # field 3 (empty)
                                                         ] # field 4 (empty)

OLDMS = [0, 2, 3, 5, 7, 11, 13, 14, 16, 16, 16]

MockOldRec1 = MockDataHolder(OLDMS, OLDVS,  0)
MockOldRec2 = MockDataHolder(OLDMS, OLDVS, 11)

# Data read from new XML format are stored in two lists. The list of values
# stores record data:
#
#   [ <record 1>, ..., <record N> ]
#
# Each record consists of record and portal data:
#
#   ... <record data>, <portal 1 data>, ..., <portal N data>, ...
#
# Record and portal data are similar, as if record data were a portal with
# a single row. We can imagine it as <portal 0 data>. Each portal data is
# that:
#
#   ..., <row 1 data>, ..., <row N data>, ...
#
# And each row is that:
#
#   modid recid <field 1> ... <field N>
#
# Here 'modid' and 'recid' are interegers. Each 'field' constist of
# values, one for each repetition. The map stores addresses of portals.

NEWVS = [ 101,  1, "r1f1"  , "r1f2c1"  , "r1f2c2"  ,  # record 1
          121, 21, "r1f3p1", "r1f4c1p1", "r1f4c2p1",  # portal row 1
          122, 22, "r1f3p2", "r1f4c1p2", "r1f4c2p2",  # portal row 2
          102,  2, "r2f1"  , "r2f2c1"  , "r2f2c2"  ]  # record 2

NEWMS = [0, 5, 15, 20, 20]

MockNewRec1 = MockDataHolder(NEWMS, 0, NEWVS,  0)
MockNewRec2 = MockDataHolder(NEWMS, 2, NEWVS, 15)

# ============================================================================

# To test reading the old XML API we need sample data. There are two main
# reading cases: with and without description. Having a description is crucial 
# in the old format because as it is it does not provide any information on 
# the structure of layouts. So we need a test sample that can be read 
# differently with a description. There are two things to test: a field that 
# is assigned to another portal and a repeating field that displays fewer 
# repetitions than it actually has.
#
# Second, there is a special data-related case. The data in the old format may 
# come from the web server or be exported from FileMaker itself. Since it is 
# supposed to be the same format, it is natural to require reading the 
# exported data as well. Thing is the formats are similar, but not same: if a 
# portal is empty, it will be rendered differently in the web response and in 
# the exported data. This means we need two sample responses for the same data 
# that match the two sources.
#
# A layout description has field and portal specifications. The resulting
# found set creates records, portals, and portal rows. The code that reads the 
# response data is thus spread among several classes.

class Xml:
    
    # The layout has two fields and a portal with two more fields. One field 
    # on the layout is just a field from the layout’s table with a single 
    # repetition. This is the simplest case. Another field comes from a 
    # different table but is placed on the layout as is. Without description 
    # the reader will assume it is in a portal with a single row. This does 
    # not hinder processing, but creates a non-existing portal. Third field 
    # has two repetitions and shows both. It is there to test reading a 
    # repeating field.
    #
    # Then there is a portal with two fields. One field has a single 
    # repetition and comes from the same table as the portal. Another field 
    # comes from a different table, has three repetitions but only shows two.
    # The portal has three rows. The overall number of cells is six. Since the
    # field comes from a different table, by default the reader will assume it
    # is a separate portal with three rows.
    #
    # The found set has two records. In the first record the portal has three
    # rows. In the second record the portal is empty. Empty portals are a
    # special case because they are rendered differently in data received from
    # the server and in data exported from FileMaker. In the exported data 
    # each field in the portal is represented by an empty '<COL>'. In the data
    # received from the Web all fields in the portal are represented by a 
    # single empty '<COL>'. We have two samples that show identical data but 
    # differ in that representation.

    LayDesc = pgfm.LayDesc() \
        .lay("b::bb")        \
        .rel("c", "c::cc", "d::dd") \
        .col("d::dd", 2)
        
    OldWeb = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
      <FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
        <ERRORCODE>0</ERRORCODE>
        <PRODUCT BUILD="3/16/2020" NAME="FileMaker Web Publishing Engine" 
            VERSION="18.0.4.428"/>
        <DATABASE DATEFORMAT="MM/dd/yyyy" LAYOUT="Lay" NAME="Db" 
            RECORDS="100" TIMEFORMAT="HH:mm:ss"/>
        <METADATA>
          <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="AA" TYPE="TEXT"/>
          <FIELD EMPTYOK="YES" MAXREPEAT="2" NAME="B::BB" TYPE="TEXT"/>
          <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="C::CC" TYPE="TEXT"/>
          <FIELD EMPTYOK="YES" MAXREPEAT="3" NAME="D::DD" TYPE="TEXT"/>
        </METADATA>
        <RESULTSET FOUND="10">
          <ROW MODID="2" RECORDID="1">
            <COL>
              <DATA>AA</DATA>
            </COL>
            <COL>
              <DATA>BB[1]</DATA>
              <DATA>BB[2]</DATA>
            </COL>
            <COL>
              <DATA>CC.1</DATA>
              <DATA>CC.2</DATA>
              <DATA>CC.3</DATA>
            </COL>
            <COL>
              <DATA>DD[1].1</DATA>
              <DATA>DD[2].1</DATA>
              <DATA>DD[1].2</DATA>
              <DATA>DD[2].2</DATA>
              <DATA>DD[1].3</DATA>
              <DATA>DD[2].3</DATA>
            </COL>
          </ROW>
          <ROW MODID="4" RECORDID="3">
            <COL>
              <DATA>AAA</DATA>
            </COL>
            <COL>
              <DATA>BBB[1]</DATA>
              <DATA>BBB[2]</DATA>
            </COL>
            <COL /> <!-- empty portal, one 'COL' -->
          </ROW>
        </RESULTSET>
      </FMPXMLRESULT>"""

    OldExp = b"""<?xml version ="1.0" encoding="UTF-8" standalone="no" ?>
      <FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
        <ERRORCODE>0</ERRORCODE>
        <PRODUCT BUILD="3/16/2020" NAME="FileMaker Web Publishing Engine" 
            VERSION="18.0.4.428"/>
        <DATABASE DATEFORMAT="MM/dd/yyyy" LAYOUT="Lay" NAME="Db" 
            RECORDS="100" TIMEFORMAT="HH:mm:ss"/>
        <METADATA>
          <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="AA" TYPE="TEXT"/>
          <FIELD EMPTYOK="YES" MAXREPEAT="2" NAME="B::BB" TYPE="TEXT"/>
          <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="C::CC" TYPE="TEXT"/>
          <FIELD EMPTYOK="YES" MAXREPEAT="2" NAME="D::DD" TYPE="TEXT"/>
        </METADATA>
        <RESULTSET FOUND="10">
          <ROW MODID="2" RECORDID="1">
            <COL>
              <DATA>AA</DATA>
            </COL>
            <COL>
              <DATA>BB[1]</DATA>
              <DATA>BB[2]</DATA>
            </COL>
            <COL>
              <DATA>CC.1</DATA>
              <DATA>CC.2</DATA>
              <DATA>CC.3</DATA>
            </COL>
            <COL>
              <DATA>DD[1].1</DATA>
              <DATA>DD[2].1</DATA>
              <DATA>DD[1].2</DATA>
              <DATA>DD[2].2</DATA>
              <DATA>DD[1].3</DATA>
              <DATA>DD[2].3</DATA>
            </COL>
          </ROW>
          <ROW MODID="4" RECORDID="3">
            <COL>
              <DATA>AAA</DATA>
            </COL>
            <COL>
              <DATA>BBB[1]</DATA>
              <DATA>BBB[2]</DATA>
            </COL>
            <COL /> <!-- empty portal, two 'COL's -->
            <COL />
          </ROW>
        </RESULTSET>
      </FMPXMLRESULT>"""

    New = b"""<?xml version="1.0" encoding="utf-8"?>
      <fmresultset xmlns="http://www.filemaker.com/xml/fmresultset" 
          version="1.0">
        <error code="0"/>
        <product build="3/16/2020" name="FileMaker Web Publishing Engine"
            version="18.0.4.428"/>
        <datasource database="Db" date-format="MM/dd/yyyy" layout="Lay"
            table="tbl" time-format="HH:mm:ss"
            timestamp-format="MM/dd/yyyy HH:mm:ss" total-count="100"/>
        <metadata>
          <field-definition auto-enter="no" four-digit-year="no" global="no"
              max-repeat="1" name="aa" not-empty="no" numeric-only="no"
              result="text" time-of-day="no" type="normal"/>
          <field-definition auto-enter="no" four-digit-year="no" global="no"
              max-repeat="2" name="b::bb" not-empty="no" numeric-only="no"
              result="text" time-of-day="no" type="normal"/>
          <relatedset-definition table="c">
            <field-definition auto-enter="yes" four-digit-year="no" 
                global="no" max-repeat="1" name="c::cc" not-empty="yes" 
                numeric-only="no" result="text" time-of-day="no" 
                type="normal"/>
            <field-definition auto-enter="yes" four-digit-year="no" 
                global="no" max-repeat="3" name="d::dd" not-empty="yes" 
                numeric-only="no" result="text" time-of-day="no" 
                type="normal"/>
          </relatedset-definition>
        </metadata>
        <resultset count="10" fetch-size="2">
          <record mod-id="2" record-id="1">
            <field name="aa">
              <data>aa</data>
            </field>
            <field name="b::bb">
              <data>bb[1]</data>
              <data>bb[2]</data>
            </field>
            <relatedset count="3" table="c">
              <record mod-id="4" record-id="3">
                <field name="c::cc">
                  <data>cc.1</data>
                </field>
                <field name="d::dd">
                  <data>dd[1].1</data>
                  <data>dd[2].1</data>
                </field>
              </record>
              <record mod-id="6" record-id="5">
                <field name="c::cc">
                  <data>cc.2</data>
                </field>
                <field name="d::dd">
                  <data>dd[1].2</data>
                  <data>dd[2].2</data>
                </field>
              </record>
              <record mod-id="8" record-id="7">
                <field name="c::cc">
                  <data>cc.3</data>
                </field>
                <field name="d::dd">
                  <data>dd[1].3</data>
                  <data>dd[2].3</data>
                </field>
              </record>
            </relatedset>
          </record>
          <record mod-id="4" record-id="3">
            <field name="aa">
              <data>aaa</data>
            </field>
            <field name="b::bb">
              <data>bbb[1]</data>
              <data>bbb[2]</data>
            </field>
            <relatedset count="0" table="c" />
          </record>
        </resultset>
      </fmresultset>"""

    @classmethod
    def Get(cls, name):
        return lxml.etree.fromstring(getattr(cls, name))

    # We use the data to test the 'recset' method. In all tests the results 
    # are supposed to be identical, so we use a common method to verify this.

    @staticmethod
    def checkRecset(test, recset):
        test.assertIsInstance(recset, pgfm.Recset)
        test.assertEqual(len(recset), 2)

        rec1 = recset[0]
        test.assertEqual(rec1.recid(), 1)
        test.assertEqual(rec1.modid(), 2)
        test.assertEqual(rec1.col("aa"), "aa")
        test.assertEqual(rec1.col("b::bb"), ["bb[1]", "bb[2]"])
        test.assertEqual(rec1.col("c::cc"), "cc.1")
        test.assertEqual(rec1.col("d::dd"), ["dd[1].1", "dd[2].1"])

        rel1 = rec1.rel("c")
        test.assertEqual(len(rel1), 3)

        row1 = rel1[0]
        test.assertEqual(row1.col("cc"), "cc.1")
        test.assertEqual(row1.col("d::dd"), ["dd[1].1", "dd[2].1"])
        row2 = rel1[1]
        test.assertEqual(row2.col("cc"), "cc.2")
        test.assertEqual(row2.col("d::dd"), ["dd[1].2", "dd[2].2"])
        row3 = rel1[2]
        test.assertEqual(row3.col("cc"), "cc.3")
        test.assertEqual(row3.col("d::dd"), ["dd[1].3", "dd[2].3"])

        rec2 = recset[1]
        test.assertEqual(rec2.recid(), 3)
        test.assertEqual(rec2.modid(), 4)
        test.assertEqual(rec2.col("aa"), "aaa")
        test.assertEqual(rec2.col("b::bb"), ["bbb[1]", "bbb[2]"])
 
        rel2 = rec2.rel("c")
        test.assertEqual(len(rel2), 0)

