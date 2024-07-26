# base64
from base64        import b64encode     as Base64Encode
    # The 'codecs' module can encode bytes as Base64 too, but it always adds a
    # newline character. We need Base64 for the Basic authentification and
    # that newline interferes with the format we must use for an HTTP header.

# codecs
from codecs        import encode        as Encode, \
                          decode        as Decode
# copy
from copy          import copy          as Copy

# datetime
from datetime      import date          as DatetimeDate
from datetime      import time          as DatetimeTime
from datetime      import timedelta     as DatetimeDelta
from datetime      import datetime      as DatetimeDatetime

# io
from io            import                  StringIO

# itertools
from itertools     import product       as IterProduct

# json
from json          import dumps         as JsonDumps, \
                          loads         as JsonLoads

# lxml
from lxml.etree    import fromstring    as LxmlFromstring
from lxml.etree    import tostring      as LxmlTostring
from lxml.etree    import XPath         as LxmlXpath

# math
from math          import trunc         as MathTrunc

# os
from os            import getenv        as OsGetenv

# requests
from requests      import request       as ReqReq

# urllib
from urllib.parse  import quote_plus    as UrlEncode

# warnings
import                                     warnings


# ============================================================================

class Api:

    @classmethod
    def layInf(cls, data, layDesc=None):
        "Read a layout specification."
        # -> cls: subclass.
        # -> data: parsed data, API-specific.
        # -> layDesc: layout description, LayDesc or None.
        # <- layout specification, LaySpec.
        layKey = cls.layKey(data)
        layCls = cls.layCls()
        if layDesc:
            laySlot = layDesc.laySlot(layCls)
            if laySlot.key == layKey:
                lay = laySlot.lay
            else:
                laySlot.key = layKey
                lay = layCls(data, layDesc)
                laySlot.lay = lay
        else:
            try:
                lay = cls.Lays[layKey]
            except KeyError:
                lay = layCls(data, layDesc)
                cls.Lays[layKey] = lay
        return lay

    # Layout cache.
    Lays = {}

    @classmethod
    def recset(cls, data, layDesc=None):
        "Read a found set."
        # -> data: parsed data, API-specific.
        # -> layDesc: layout description, LayDesc or None.
        # <- found set, Rset.
        return cls.layInf(data, layDesc).recset(data)

# ----------------------------------------------------------------------------

class ApiXml(Api):

    # FileMaker XML namespace URIs and prefixes.
    NS = {
      "F" : "http://www.filemaker.com/fmpxmlresult"   ,
      "L" : "http://www.filemaker.com/fmpxmllayout"   ,
      "f" : "http://www.filemaker.com/xml/fmresultset",
    }

    @staticmethod
    def Xp(expr):
        "Create an XPath."
        # -> expr: XPath expression, str, with 'NS' prefixes.
        # <- compiled XPath, 'lxml' object.
        return LxmlXpath(expr, namespaces=ApiXml.NS)

    @staticmethod
    def Jc(pfx, name):
        "Create a QName in James Clark’s format."
        # -> pfx: namespace prefix, str, matchin 'NS'.
        # -> name: local name, str.
        # <- QName in James Clark’s format, str, '{nsUri}localName'.
        return "{%s}%s" % (ApiXml.NS[pfx], name)

    @staticmethod
    def read(data):
        "Read raw response data."
        # -> data: response data, bytes.
        # <- result of reading, XML, 'lxml' object.
        return LxmlFromstring(data)

    @classmethod
    def error(cls, xml):
        "Get the error number and text."
        # -> cls: subclass of ApiXml.
        # -> xml: XML, 'lxml' object.
        # <- error number and text, (int, None).
        return int(*cls.XpError(xml)), None

# ----------------------------------------------------------------------------

class ApiXmlRset(ApiXml):

    @classmethod
    def rtyp(cls, xml):
        "Guess the result type by data."
        # -> cls: subclass of 'ApiXmlRset'.
        # -> xml: XML, 'lxml' object.
        # <- result type, one of 'ResType' attrs.
        layName, = cls.XpLayName(xml)
        if not layName:
            fields = cls.XpFnams(xml)
            if len(fields) != 1:
                raise ErrApiXmlRsetRtypFields(len(fields))
            fieldName = fields[0]
            if fieldName == "DATABASE_NAME":
                res = "srvDbs"
            elif fieldName == "LAYOUT_NAME":
                res = "dbLays"
            elif fieldName == "SCRIPT_NAME":
                res = "dbScrs"
            else:
                raise ErrApiXmlRsetRtypFieldName(fieldName)
        else:
            numRecs = cls.XpNumRecs(xml)
            if int(numRecs):
                res = "recset"
            else:
                res = "layInf"
        return res

    @classmethod
    def layKey(cls, xml):
        "Compute the layout key."
        # -> cls: subclass of 'ApiXmlRset'.
        # -> xml: XML, 'lxml' object.
        # <- layout key, bytes.
        return LxmlTostring(*cls.XpLayKey(xml))

    @classmethod
    def srvDbs(cls, xml):
        "Read database names."
        # -> cls: subclass of 'ApiXmlRset'.
        # -> xml: XML, 'lxml' object.
        # <- database names, (Name*).
        return tuple((Name(v) for v in cls.XpNames(xml)))

    @classmethod
    def dbLays(cls, xml):
        "Read layout names."
        # -> cls: subclass of 'ApiXmlRset'.
        # -> xml: XML, 'lxml' object.
        # <- layout names, (Name|Sep).
        res = []
        for text in cls.XpNames(xml):
            if text == "-":
                res.append(Sep)
            else:
                res.append(Name(text))
        return res

    @classmethod
    def dbScrs(cls, xml):
        "Read script names."
        # -> cls: subclass of 'ApiXmlRset'.
        # -> xml: XML, 'lxml' object.
        # <- script names, (Name|Folder|Sep).
        res = []
        ctx = res
        # TODO ...
        for text in cls.XpNames(xml):
            if text == "-":
                res.append(Sep)
            else:
                res.append(Name(text))
        return res

# ----------------------------------------------------------------------------

class ErrApiXmlRsetRtypFields(Exception):
    def __str__(self):
        lenFields, = self.args
        return "Unexpected XML result: empty layout name and number of " \
                "fields is not 1 (%d)." % lenFields

# ----------------------------------------------------------------------------

class ErrApiXmlRsetRtypFieldName(Exception):
    def __str__(self):
        fieldName, = self.args
        return "Unexpected XML result: empty layout name, single field, but " \
                "unknown name '%s' (expected 'DATABASE_', 'LAYOUT_' or " \
                "'SCRIPT_NAMES'." % fieldName

# ----------------------------------------------------------------------------

class ApiXmlOld(ApiXmlRset):

    Ver       = "FMPXMLRESULT"
    Tag       = ApiXml.Jc("F", Ver)
    XpError   = ApiXml.Xp("/F:FMPXMLRESULT/F:ERRORCODE/text()")
    XpLayName = ApiXml.Xp("/F:FMPXMLRESULT/F:DATABASE/@LAYOUT")
    XpFnams   = ApiXml.Xp("/F:FMPXMLRESULT/F:METADATA/F:FIELD/@NAME")
    XpNumRecs = ApiXml.Xp("count(/F:FMPXMLRESULT/F:RESULTSET/F:ROW)")
    XpLayKey  = ApiXml.Xp("/F:FMPXMLRESULT/F:METADATA")
    XpNames   = ApiXml.Xp("/F:FMPXMLRESULT/F:RESULTSET/F:ROW/F:COL/F:DATA/"
                          "text()")

    @staticmethod
    def layCls():
        "Get the layout specification class."
        # <- layout specification, subclass of 'LaySpec'.
        return LaySpecXapiOld

# ----------------------------------------------------------------------------

class ApiXmlNew(ApiXmlRset):

    Ver       = "fmresultset"
    Tag       = ApiXml.Jc("f", Ver)
    XpError   = ApiXml.Xp("/f:fmresultset/f:error/@code")
    XpLayName = ApiXml.Xp("/f:fmresultset/f:datasource/@layout")
    XpFnams   = ApiXml.Xp("/f:fmresultset/f:metadata/f:field-definition/"
                          "@name")
    XpNumRecs = ApiXml.Xp("number(/f:fmresultset/f:resultset/@fetch-size)")
    XpLayKey  = ApiXml.Xp("/f:fmresultset/f:metadata")
    XpNames   = ApiXml.Xp("/f:fmresultset/f:resultset/f:record/f:field/"
                          "f:data/text()")

    @staticmethod
    def layCls():
        "Get the layout specification class."
        # <- layout specification, subclass of 'LaySpec'.
        return LaySpecXapiNew

# ----------------------------------------------------------------------------

class ApiXmlLay(ApiXml):

    Ver       = "FMPXMLLAYOUT"
    Tag       = ApiXml.Jc("L", Ver)
    XpError   = ApiXml.Xp("/L:FMPXMLLAYOUT/L:ERRORCODE/text()")

    @staticmethod
    def rtyp(xml):
        "Determine the result type."
        # -> xml: XML, 'lxml' object, ignored.
        # <- result type, one of 'ResType' attrs.
        return "layFmt"

    @staticmethod
    def layFmt(xml):
        "Read the layout format details."
        # -> xml: XML, 'lxml' object.
        # <- layout format, LayFmt.
        pass # TODO

# ----------------------------------------------------------------------------

class ApiData:

    @staticmethod
    def read(data):
        "Read raw response data."
        # -> data: response data, bytes.
        # <- result of reading, XML, 'lxml' object.
        return JsonLoads(data)

# ----------------------------------------------------------------------------

class ApiData1(ApiData):

    Ver = "v1"

# ----------------------------------------------------------------------------

class ApiData2(ApiData):

    Ver = "v2"

# ----------------------------------------------------------------------------

class ApiDataLatest(ApiData):

    Ver = "vLatest"

# ----------------------------------------------------------------------------
# The default API for now is old XML. When the Data API support is ready, it
# will be switched to Data API as the most feature-complete.

defaultApi = ApiXmlNew

# ============================================================================

# NOTE: for now the code merely creates a lowercase version of the value. For
# FileMaker file, layout, and field names this seems to be enough. But for
# text field values the proper comparison matching the way they are compared
# in FileMaker may be way more advanced.

def Xfrm(val):
    "Produce a case-insensitive comparison value."
    # -> val: string, str.
    # <- value for comparison, str.
    return val.lower()

# ============================================================================
# In many classes I use 'cmp' as a comparison method. This mix-in uses it to
# provide the common Python syntactic sugar for comparison.

class Cmp:
    # A mix-in to give a class with 'cmp()' Python comparison methods.

    # Python syntactic sugar

    def __eq__(this, that):
        return this.cmp(that) ==  0
    def __ne__(this, that):
        return this.cmp(that) !=  0
    def __lt__(this, that):
        return this.cmp(that) == -1
    def __le__(this, that):
        return this.cmp(that) != +1
    def __gt__(this, that):
        return this.cmp(that) == +1
    def __ge__(this, that):
        return this.cmp(that) != -1

# ----------------------------------------------------------------------------
# Names of FileMaker objects such as files, layouts, scripts, and so on are
# not case-sensitive. To represent them we use a special subclass of 'str'
# that ignores case on comparison.

class Name(Cmp, str):
    "Name of a FileMaker file, layout, script, etc. Case-insensitive."

    def __new__(cls, obj):
        # -> obj: name value, str or Name.
        # <- name, Name.
        if isinstance(obj, cls):
            r = obj
        elif isinstance(obj, str):
            if obj == "":
                # Must return the 'emptyName' constant that may not exist.
                try:
                    r = globals()["emptyName"]
                except KeyError:
                    # The constant does not exist yet.
                    r = super().__new__(cls, obj)
                    r.key = obj
            else:
                r = super().__new__(cls, obj)
                r.key = Xfrm(obj)
        else:
            # Unsuitable object.
            raise ErrNameNew(cls, obj)
        return r

    __slots__ = "key"

    # key: comparison key.

    def __repr__(self):
        # <- <Name 'val'>
        b = StringIO()
        b.write("<")
        b.write(__name__)
        b.write(".")
        b.write(type(self).__name__)
        b.write(" '")
        b.write(self)
        b.write("'>")
        return b.getvalue()

    def __hash__(self):
        return hash(self.key)

    def cmp(this, that):
        "Compare two names."
        # -> this: current name, Name.
        # -> that: other object, Name or str.
        # <- result, -1, 0, +1.
        if this is that:
            r = 0
        else:
            that = type(this)(that)
            if this.key < that.key:
                r = -1
            elif this.key > that.key:
                r = +1
            else:
                r = 0
        return r

# ----------------------------------------------------------------------------

class ErrNameNew(Exception):
    def __str__(self):
        cls, obj = self.args
        return "Cannot create an instance of '%s' from an '%s'." % \
                (cls.__name__, type(obj).__name__)

# ----------------------------------------------------------------------------

emptyName = Name("")

# ----------------------------------------------------------------------------
# A field name is a variant of 'Name'. It is also case-insensitive and has one
# or two parts. One of the parts is the name of the field itself. It always
# exists. Another part is the name of the table. It may or may not exist. If
# it exists, it is prepended to the name and separated by '::', for example:
#
#   table::field
#
# We use the table name in two situations. First, when we read a layout in the
# old XML format we by default assume that every field from a different table
# is in a portal to this table. Here we need to read the field name string and
# extract the table name, if any. Second, when we read field specifications
# or values from a portal context we allow the user to omit the table name if
# it is the same as the portal’s. In this case we need to add a table name if
# it does not exist.

class ColName(Name):

    # When creating a new name we allow to specify the default table. The
    # default table is only used if the name does not have its own table.

    def __new__(cls, val, defaultTbl=None):
        # -> val: field name, str or ColName, not empty.
        # -> defaultTbl: default table name, str or Name.
        if "::" in val or defaultTbl is None:
            # The name has a table or no default table is given: use as is.
            if isinstance(val, ColName):
                # Reuse the instance.
                r = val
            else:
                # Create a new instance.
                r = super().__new__(cls, val)
        else:
            # The name has no table and there is a default table: combine.
            val = defaultTbl + "::" + val
            r = super().__new__(cls, val)
        return r

    @property
    def tbl(self):
        "Table name, Name, read-only."
        # <- table name, Name.
        if "::" in self:
            r = Name(self.split("::", 1)[0])
        else:
            r = emptyName
        return r

# ----------------------------------------------------------------------------

class Val(Cmp, str):

    def __new__(cls, val):
        if isinstance(val, Val):
            # reuse the object
            r = val
        elif val is None or isinstance(val, str) and val == "":
            try:
                r = globals()["emptyVal"]
            except KeyError:
                r = super().__new__(Val, "")
        elif cls is Val:
            # Create an instance of the best matching type.
            if isinstance(val, str):
                r = Text.FromStr(val)
            elif isinstance(val, (int, float)):
                r = Number.FromNum(val)
            elif isinstance(val, DatetimeDatetime): # must be before 'date'.
                r = Timestamp.FromPyDatetime(val)
            elif isinstance(val, DatetimeDate):
                r = Date.FromPyDate(val)
            elif isinstance(val, DatetimeTime):
                r = Time.FromPyTime(val)
            elif isinstance(val, DatetimeDelta):
                r = Time.FromPyDelta(val)
            elif isinstance(val, (dict, list, tuple)):
                # Attempt to convert to JSON.
                r = Text.FromStr(JsonDumps(val))
            else:
                # Cannot convert this to a FileMaker type.
                raise ErrValNewType(val)
        else:
            r = super().__new__(cls, val)
        return r

    def __repr__(self):
        # <- <module.cls val>
        b = StringIO()
        b.write("<")
        b.write(__name__)
        b.write(".")
        b.write(type(self).__name__)
        b.write(" '")
        b.write(self)
        b.write("'>")
        return b.getvalue()

    def cmp(this, that):
        "(Compare two instances.)"
        # -> that: another Val-compatible object.
        # <- comparsion result, -1, 0, 1.

        # Convert 'that' to a Val.
        that = type(this)(that)
        # FileMaker places empty values before non-empty ones.
        if this is emptyVal:
            if that is emptyVal:
                r = 0
            else:
                r = -1 # this is less
        else:
            if that is emptyVal:
                r = +1 # this is greater
            else:
                # Type specific comparison; requires identical types.
                if type(this) != type(that):
                    raise NotImplementedError
                # 'cmpEx' is defined in subclasses.
                r = this.cmpEx(that)
        return r

    def toStr(self):
        "(Convert to string.)"
        # <- self
        return self

# ----------------------------------------------------------------------------

class ErrValNewType(Exception):
    def __str__(self):
        val, = self.args
        return "Cannot create a FileMaker value from '%s'." \
                % type(val).__name__

# ----------------------------------------------------------------------------
# The constant to represent an empty value of any type.

emptyVal = Val(None)

# ----------------------------------------------------------------------------

class Text(Val):
    "FileMaker field type text."

    @classmethod
    def FromStr(cls, val):
        "Create an instance from a Python string."
        # -> obj: Python object, str.
        # <- instance of Text.
        r = super().__new__(cls, val)
        if isinstance(r, cls):
            r.key = Xfrm(val)
        return r

    def __new__(cls, val):
        # -> val: object, str, None, Text.
        if isinstance(val, cls):
            r = val
        elif isinstance(val, str):
            r = cls.FromStr(val)
        elif val is None:
            r = emptyVal
        else:
            # Unsuitable object.
            raise ErrTextNew(val)
        return r

    __slots__ = "key"

    # key: the value to use for hash.

    def __hash__(self):
        return hash(self.key)

    def cmpEx(this, that):
        "Compare two non-empty text instances."
        # -> that: another Text, non-empty.
        # <- comparison result, -1, 0, 1.
        if this.key < that.key:
            r = -1
        elif this.key > that.key:
            r = +1
        else:
            r = 0
        return r

# ----------------------------------------------------------------------------

class ErrTextNew(Exception):
    def __str__(self):
        val, = self.args
        return "Cannot create a Text from an instance of '%s'. Use a str " \
                "a Text, or None." % (type(val).__name__)

# ----------------------------------------------------------------------------

class Number(Val):
    "FileMaker number value."

    @classmethod
    def FromNum(cls, val):
        "Create a number from a safe Python number."
        # -> val: Python number, int or float.
        # <- number, Number.
        r = cls(str(val))
        r.val = val
        return r

    @classmethod
    def FromStr(cls, val):
        "Create a number from a safe string."
        # -> val: Python string.
        # <- number, Number.
        r = super().__new__(cls, val)
        if isinstance(r, cls):
            if "." in val:
                c = float
            else:
                c = int
            r.val = c(val)
        return r

    def __new__(cls, val):
        if isinstance(val, cls):
            r = val
        elif isinstance(val, str):
            r = cls.FromStr(val)
        elif isinstance(val, (int, float)):
            r = cls.FromNum(val)
        elif val is None:
            r = emptyVal
        else:
            # Unsuitable object.
            raise ErrNumberNew(val)
        return r

    __slots__ = "val"

    # val: value, int or float.

    def __hash__(self):
        return hash(self.val)

    def cmpEx(this, that):
        "Compare two non-empty Number instances."
        # -> that: another Number, non-empty.
        # <- comparison result, -1, 0, 1.
        if this.val < that.val:
            r = -1
        elif this.val > that.val:
            r = +1
        else:
            r = 0
        return r

    def toNum(self):
        "Get the value as a number."
        # <- value as a number, int or float.
        return self.val

# ----------------------------------------------------------------------------

class ErrNumberNew(Exception):
    def __str__(self):
        val, = self.args
        return "Cannot create a Number from an instance of '%s'. Use a str " \
                "('', '1', '2.3'), an int, a float, a Number, or None." \
                % (type(val).__name__)

# ----------------------------------------------------------------------------

class Date(Val):

    @staticmethod
    def Fmt(y, m, d):
        "Format a date according to FileMaker rules."
        # -> y, m, d: year, month, date values, int.
        # <- date as string, str.

        # FileMaker uses leading zeros only for the year.
        return "%d/%d/%.4d" % (m, d, y)

    @classmethod
    def FromInt(cls, val):
        "Create a Date from a safe ordinal."
        # -> val: value, int, trusted to be a valid date ordinal.
        # <- date instance, Date.
        t = DatetimeDate.fromordinal(val)
        r = super().__new__(cls, cls.Fmt(t.month, t.day, t.year))
        r.val = val
        return r

    FromNum = FromInt

    @classmethod
    def FromPyDate(cls, date):
        "Create an instance from a safe Python date."
        # -> date: Python date, datetime.date, trusted to be safe.
        # <- instance of Date.
        r = super().__new__(cls, cls.Fmt(date.year, date.month, date.day))
        r.val = date.toordinal()
        return r

    @classmethod
    def FromStr(cls, val):
        "Create a Date from a safe string."
        # -> val: value, str, trusted to be a valid 'M/D/Y' or empty.
        # <- date instance, Date.
        r = super().__new__(cls, val)
        if isinstance(r, cls):
            m, d, y = map(int, val.split("/"))
            r.val = DatetimeDate(y, m, d).toordinal()
        return r

    @classmethod
    def FromYmd(cls, Y, M, D):
        "Create an instance from safe year, month, and day components."
        # -> Y, M, D: date components, int, trusted to be valid.
        # <- instance of Date.
        # TODO: check range?
        r = super().__new__(cls, cls.Fmt(Y, M, D))
        r.val = DatetimeDate(Y, M, D).toordinal()
        return r

    def __new__(cls, *args):
        if len(args) == 1:
            val, = args
            if isinstance(val, cls):
                r = val
            elif isinstance(val, str):
                r = cls.FromStr(val)
            elif isinstance(val, int):
                r = cls.FromInt(val)
            elif isinstance(val, DatetimeDate):
                r = cls.FromPyDate(val)
            elif val is None:
                r = emptyVal
            else:
                # Unsuitable object.
                raise ErrDateNew(args)
        elif len(args) == 3:
            r = cls.FromYmd(*args)
        else:
            # Unsuitable object.
            raise ErrDateNew(args)
        return r

    __slots__ = "val"

    # val: value, int.

    def __hash__(self):
        return hash(self.val)

    def cmpEx(self, other):
        "Compare two non-empty date instances."
        # -> other: another Date.
        # <- comparison result, -1, 0, 1.
        if self.val < other.val:
            r = -1
        elif self.val > other.val:
            r = +1
        else:
            r =  0
        return r

    def toInt(self):
        "Get the date as a day number in the proleptic Gregorian calendar."
        # <- number, int.
        return self.val

    toNum = toInt

    def toPyDate(self):
        "Get the date as a Python date."
        # <- Python date, datetime.date.
        return DatetimeDate.fromordinal(self.val)

    def toYmd(self):
        "Get the date as year, month, and day."
        d = self.toPyDate()
        return d.year, d.month, d.day

# ----------------------------------------------------------------------------

class ErrDateNew(Exception):
    def __str__(self):
        args, = self.args
        if len(args) == 1:
            r = "Wrong argument type '%s'. Expected 'int', 'str', " \
                    "'datetime.date'." % type(args[0]).__name__
        else:
            r = "Wrong number of arguments: %d. Expected a single 'int', " \
                    "'str', 'datetime.date', or three 'int' for year, " \
                    "month, and day." % len(args)
        return r

# ----------------------------------------------------------------------------

class Time(Val):
    "FileMaker time value type."

    @staticmethod
    def HmsToStr(h, m, s):
        "Format the time as a string."
        # -> h, m, s: hour, minute (int), seconds (int or float).
        # <- formatted time, str.

        # FileMaker uses leading zeros for minutes and seconds.
        return "%d:%02d:%02g" % (h, m, s)

    @staticmethod
    def HmsToNum(h, m, s):
        "Convert hour, minute, and second components into a number."
        # -> h, m, s: hour, minute (int), seconds (int or float).
        # <- numeric value, int.
        return round(((h * 60 + m) * 60 + s) * 1000000)

    @staticmethod
    def NumToHms(v):
        "Convert numeric value into hours, minutes, and seconds."
        # -> v: numeric value, int or float.
        # <- h, m, s: hours, minutes (int) and seconds (int or float).
        h = MathTrunc( v                                   / 3600000000)
        m = MathTrunc((v - h * 3600000000                ) / 60000000  )
        s =           (v - h * 3600000000 - m * 60000000 ) / 1000000
        return h, m, s

    # ------------------------------------------------------------------------

    @classmethod
    def FromHms(cls, h, m, s):
        "Create an instance of time from hours, minutes, and seconds."
        # -> h, m, s: time components, int, int, float
        # <- instance of Time.
        r = super().__new__(cls, cls.HmsToStr(h, m, s))
        r.val = cls.HmsToNum(h, m, s)
        return r

    @classmethod
    def FromNum(cls, v):
        "Create an instance of time from number of seconds."
        # -> val: number of seconds, int or float.
        # <- instance of Time.
        v = round(v * 1000000)
        r = super().__new__(cls, cls.HmsToStr(*cls.NumToHms(v)))
        r.val = v
        return r

    @classmethod
    def FromStr(cls, v):
        "Create an instance from a safe string ('H:M:S.s')."
        # -> val: value, str, 'H:M:S.s'.
        # <- time instance, Time.
        r = super().__new__(cls, v)
        if isinstance(r, cls):
            h, m, s = v.split(":")
            r.val = cls.HmsToNum(int(h), int(m), float(s))
        return r

    @classmethod
    def FromPyTime(cls, t):
        "Create an instance of a Time from a Python time."
        # -> time: Python time, datetime.time.
        # <- instance of Time.
        return cls.FromHms(t.hour, t.minute, t.second +
                t.microsecond / 1000000)

    @classmethod
    def FromPyDelta(cls, t):
        "Create an instance of a Time from a Python timedelta."
        # -> time: Python time, datetime.time.
        # <- instance of Time.
        return cls.FromNum(t.days * 86400 + t.seconds +
                t.microseconds / 1000000)

    def __new__(cls, *args):
        if len(args) == 1:
            val, = args
            if isinstance(val, cls):
                r = val
            elif isinstance(val, str):
                r = cls.FromStr(val)
            elif isinstance(val, (int, float)):
                r = cls.FromNum(val)
            elif isinstance(val, DatetimeTime):
                r = cls.FromPyTime(val)
            elif isinstance(val, DatetimeDelta):
                r = cls.FromPyDelta(val)
            elif val is None:
                r = emptyVal
            else:
                raise ErrTimeNew(args)
        elif len(args) == 3:
            r = cls.FromHms(*args)
        else:
            raise ErrTimeNew(args)
        return r

    __slots__ = "val"

    # val: value as a number of seconds, int or float.

    def __hash__(self):
        return hash(self.val)

    def cmpEx(this, that):
        "Compare two non-empty time values."
        # -> other: another Time.
        # <- comparison result, -1, 0, 1.
        if this.val < that.val:
            r = -1
        elif this.val > that.val:
            r = +1
        else:
            r =  0
        return r

    def toHms(self):
        "Get hours, minutes, and seconds of itself."
        # <- h, m, s: hours, minutes, seconds, int, int, float.
        return self.NumToHms(self.val)

    def toNum(self):
        "Get the time value value a number of seconds."
        # <- number, int or float.
        return self.val / 1000000

    def toPyTime(self):
        "Get the value as Python time."
        # <- Python time, datetime.time.
        h, m, s = self.toHms()
        return DatetimeTime(h, m, int(s), round(s % 1 * 1000000))

    def toPyDelta(self):
        "Get the value as Python timedelta."
        # <- Python timedelta, datetime.timedelta.
        h, m, s = self.toHms()
        return DatetimeDelta(hours=h, minutes=m, seconds=s)

# ----------------------------------------------------------------------------

class ErrTimeNew(Exception):
    def __str__(self):
        args, = self.args
        if len(args) == 1:
            r = "Wrong argument type '%s'. Expected 'int', 'float', 'str', " \
                    "'datetime.date', 'datetime.timedelta'." \
                    % type(args[0]).__name__
        else:
            r = "Wrong number of arguments: %d. Expected a single 'int', " \
                    "'str', 'datetime.date', or three 'int' for hours, " \
                    "minutes, and seconds." % len(args)
        return r

# ----------------------------------------------------------------------------

class Timestamp(Val):

    @classmethod
    def FromDateTime(cls, d, t):
        "Create a Timestamp from safe (non-empty) date and time."
        # -> d, t: date and time, Date, Time.
        # <- instance of Timestamp.
        d = Date(d)
        t = Time(t)
        if not isinstance(d, Date) or not isinstance(t, Time):
            # Unsuitable date or time.
            raise ErrTimestampFromDateTime(d, t)
        r = super().__new__(cls, d + " " + t)
        r.date = d
        r.time = t
        return r

    @classmethod
    def FromPyDatetime(cls, v):
        "Create a Timestamp from a Python datetime."
        # -> v: Python datetime value, datetime.datetime.
        # <- instance of Timestamp.
        d = Date.FromPyDate(v.date())
        t = Time.FromPyTime(v.time())
        return cls.FromDateTime(d, t)

    @classmethod
    def FromStr(cls, val):
        "Create an instance of Timestamp from a safe string."
        # -> val: value, str.
        # <- timestamp instance, Timestamp.
        if val == "":
            r = emptyVal
        else:
            r = super().__new__(cls, val)
            d, t = val.split(" ")
            r.date = Date.FromStr(d)
            r.time = Time.FromStr(t)
        return r

    def __new__(cls, *args):
        # -> args: None, str, Timestamp, Python datetime or date and time.
        # <- Timestamp or emptyVal
        if len(args) == 1:
            val, = args
            if isinstance(val, str):
                r = cls.FromStr(val)
            elif isinstance(val, DatetimeDatetime):
                r = cls.FromPyDatetime(val)
            elif val is None:
                r = emptyVal
            else:
                # Unsuitable object.
                raise ErrTimestampNew(args)
        elif len(args) == 2:
            r = cls.FromDateTime(*args)
        elif len(args) == 6:
            date = Date.FromYmd(*args[0:3])
            time = Time.FromHms(*args[3:6])
            r = cls.FromDateTime(date, time)
        else:
            # Unsuitable number of arguments.
            raise ErrTimestampNew(args)
        return r

    __slots__ = "date", "time"

    # date: date component, Date.
    # time: time component, Time.

    def __hash__(self):
        return hash((self.date, self.time))

    def cmpEx(this, that):
        "Compare two non-empty timestamp instances."
        # -> other: another Timestamp, not empty.
        # <- comparison result, -1, 0, 1.
        r = this.date.cmp(that.date)
        if r == 0:
            r = this.time.cmp(that.time)
        return r

    def toDateTime(self):
        "Get Timestamp as Date and Time."
        # <- date and time values, Date, Time.
        return self.date, self.time

    def toPyDatetime(self):
        "Get Timestamp as Date and Time."
        # <- Python datetime value, datetime.datetime.
        Y, M, D = self.date.toYmd()
        h, m, s = self.time.toHms()
        return DatetimeDatetime(Y, M, D, h, m, int(s), int(s % 1 * 1000000))

# ----------------------------------------------------------------------------

class ErrTimestampFromDateTime(Exception):
    def __str__(self):
        d, t = self.args
        return "Failed to convert '%s' and '%s' into valid non-empty date " \
                "and time." % (type(d).__name__, type(t).__name__)

class ErrTimestampNew(Exception):
    def __str__(self):
        args, = self.args
        if len(args) == 1:
            r = "Wrong argument type '%s'. Expected 'str', " \
                    "'datetime.datetime'." % type(args[0]).__name__
        else:
            r = "Wrong number of arguments: %d. Expected a single 'str', " \
                    "'datetime.datetime', or separate date and time." \
                    % len(args)
        return r

# ----------------------------------------------------------------------------

class Container(Val):

    @classmethod
    def FromStr(cls, val):
        return super().__new__(cls, val)

    def __new__(cls, val):
        if isinstance(val, cls):
            r = val
        elif isinstance(val, str):
            r = cls.FromStr(val)
        elif val is None:
            r = emptyVal
        else:
            # Unsuitable object.
            raise ErrContainerNew(val)
        return r

# ----------------------------------------------------------------------------

class ErrContainerNew(Exception):
    def __str__(self):
        val, = self.args
        return "Cannot create a container from '%s'." % type(val).__name__

# ============================================================================
# A folder is a result of reading a list of scripts.

class Folder(list):

    __slots__ = "name"

    # name: folder name, Name.

    def __init__(self, name):
        # -> name: folder name, str.
        self.name = Name(name)

# ============================================================================
# An HTTP request is a simple data structure to handle an HTTP request.

class HttpReq:
    "An HTTP request."

    __slots__ = "verb", "path", "data", "_headers"

    # verb : the HTTP verb, str, e.g. 'GET'.
    # path : the URL to request (without the authority), str.
    # data : the data to send, str, bytes or None.
    # _headers : request headers, (str:str).

    def __init__(self, verb, path, data=None, mime=None):
        # verb : the HTTP verb, str, e.g. 'GET'.
        # path : the URL to request (without the authority), str.
        # data : the data to send, str, bytes or None.
        # mime : data type, str or None.
        self.verb = verb
        self.path = path
        self._headers = {}
        if data is None:
            if mime:
                # Got content type without content.
                raise ErrHttpReqMime(mime)
            self.data = None
        else:
            if isinstance(data, bytes):
                self.data = data
            elif isinstance(data, str):
                try:
                    # Encode the string as Latin-1.
                    self.data = data.encode("latin-1")
                except UnicodeEncodeError:
                    # Got a string data that cannot be encoded as Latin-1.
                    raise ErrHttpReqStr()
            else:
                # Data is neither 'bytes' nor 'str'.
                raise ErrHttpReqData(type(data))
            if mime:
                self._headers["content-type"] = mime

    def send(self, srv, auth=None):
        "Send itself to the server."
        # -> srv: server, Srv.
        # -> auth: authentification object, User, Session, or None.
        # <- response, HttpResp.
        hdrs = Copy(self._headers)
        if auth:
            # Only use authorization in transit, do not store.
            hdrs["authorization"] = auth.auth
        # 'ReqReq' is 'requests.request'.
        r = ReqReq(self.verb, srv.url + self.path, headers=hdrs,
                data=self.data, verify=srv.verifySsl)
        return HttpResp(self, srv, auth, r.status_code, r.headers, r.content)

# ----------------------------------------------------------------------------

class ErrHttpReqData(Exception):
    def __str__(self):
        cls, = self.args
        return "HttpReq: Cannot use an instance of '%s' as 'data'." \
                % cls.__name__

class ErrHttpReqStr(Exception):
    def __str__(self):
        return "HttpReq: Failed to encode the received 'data' string as " \
                "Latin 1."

class ErrHttpReqMime(Exception):
    def __str__(self):
        mime, = self.args
        return "HttpReq: Got the 'mime' parameter ('%s') without 'data'." \
                % mime

# ============================================================================
# A response to an HTTP request.

class HttpResp:
    "A response to an HTTP response."

    __slots__ = "req", "srv", "auth", "code", "hdrs", "data", "error"

    # req  : the request, HttpReq.
    # srv  : the server, Srv.
    # auth : the authentification object, None, User, or Session.
    # code : the response code, int, for example, 200.
    # hdrs : the response headers, dict.
    # data : the response data, bytes or None.
    # error: the error object, ErrHttpResp/None.

    def __init__(self, req, srv, auth, code, headers, data):
        self.req = req
        self.srv = srv
        self.auth = auth
        self.code = code
        self.hdrs = headers
        self.data = data
        if code >= 400:
            error = ErrHttpResp(self)
        else:
            error = None
        self.error = error

    def header(self, key):
        "Get a header."
        # -> key: header name, str.
        # <- header value, str.
        return self.hdrs[key]

# ----------------------------------------------------------------------------

class ErrHttpResp(Exception):
    def __str__(self):
        resp, = self.args
        return "%r: error %d." % (resp, resp.code)

# ============================================================================
# A FileMaker server.

class Srv:
    "A FileMaker server."

    __slots__ = "url", "user", "api", "verifySsl"

    # url: site URL, str.
    # user: default user, User or None.
    # api : default API preference, Api.
    # verifySsl: whether to verify the server identity, bool.

    def __init__(self, url, user=None, api=None, verifySsl=True):
        self.url = url.rstrip("/") # discard trailing '/' if any.
        self.user = user
        self.api = api
        self.verifySsl = verifySsl

    def __repr__(self):
        b = StringIO()
        b.write("<")
        b.write(__name__)
        b.write(".")
        b.write(type(self).__name__)
        b.write(" url '")
        b.write(self.url)
        b.write("', user [")
        if self.user:
            b.write("+")
        else:
            b.write("-")
        b.write("], api [")
        if self.api:
            b.write("+")
        else:
            b.write("-")
        b.write("], verifySsl ")
        b.write(str(self.verifySsl))
        b.write(">")
        return b.getvalue()

    def session(self, file, user=None, api=None):
        "Create a session."
        # -> file: file name, str.
        # -> user: user, User or None.
        # -> api: default API for the session, Api or None.
        # <- session, Session.
        user = user or self.user or defaultUser
        if not user:
            raise ErrSrvSession()
        return Session(self, file, user, api)

    def send(self, req, user=None, api=None):
        "Send a request to the server and return the response."
        # -> req: request, subclass of Req.
        # -> user: user, User or None.
        # -> api: API, Api or None.
        # <- response, RespSrv.
        return req.send(self, user, None, api)

class ErrSrvSession(Exception):
    def __str__(self):
        return "Found no user to create a session."

# ============================================================================
# Rcmd is a generic container for a single request command.

class Rcmd:

    __slots__ = "key", "val"

    # key: command key, one of Rkey instances.
    # val: command value, as appropriate, (obj*).

    def __init__(self, key, val):
        self.key = key
        self.val = val

# ============================================================================

class Rkey(int):
    "A key that describes a command type."

    # Next value.
    Next = 1

    def __new__(cls, name):
        "Create an Rkey."
        # <- instance of Rkey with unique value suitable for a bitset.
        res = super().__new__(cls, cls.Next)
        cls.Next = cls.Next << 1
        res.name = name
        return res

    # name: key name, str.

# A fixed number of Rkeys for request commands.

COL   = Rkey("col"  )
DB    = Rkey("db"   )
LAY1  = Rkey("lay1" )
LAY2  = Rkey("lay2" )
MAX   = Rkey("max"  )
MODID = Rkey("modid")
OMIT  = Rkey("omit" )
PAR1  = Rkey("par1" )
PAR2  = Rkey("par2" )
PAR3  = Rkey("par3" )
RECID = Rkey("recid")
REQ   = Rkey("req"  )
SCR1  = Rkey("scr1" )
SCR2  = Rkey("scr2" )
SCR3  = Rkey("scr3" )
SKIP  = Rkey("skip" )
SORT  = Rkey("sort" )

# The 'Rkey' class is no longer necessary.
del Rkey

# ============================================================================
# A request is a message we send to a FileMaker server to get a response.
# There are several request types implemented as subclasses of 'Rec'. Most
# requests can be sent to any API and the interface of requests is not
# specific to an API. Just before sending a request is rendered in a format
# for the target API.

class Req:

    # A request may not require any fields.
    Exp = 0

    # Most requests use the default authentification.
    Auth = "mand"

    # Most requests return a found set.
    rtyp = "recset"

    __slots__ = "base", "file", "_exp", "_set", "_cmds", "_xapi", \
            "_dapi", "_lock"

    # base : base request, same subclass of Req or None.
    # file : file name, Name or None.
    # _exp : expected commands, int (bitset of Rkey.code).
    # _set : set commands, int (bitset of Rkey.code).
    # _cmds: request commands, [Rcmd].
    # _xapi: request for XML API, RfmtXapi or None.
    # _dapi: request for Data API, RfmtDapi or None.
    # _lock: whether the request is locked, bool.

    def __init__(self, base=None):
        if not base:
            self.base = None
            self._exp = self.Exp
            self._set = 0
            self.file = None
        else:
            if type(base) is not type(self):
                # The base request must be of the same type.
                raise ErrReqInit(type(self), base)
            # Automatically lock the base request.
            base.lock()
            self.base = base
            # Copy shared properties.
            self._exp = base._exp
            self._set = base._set
            self.file = base.file
        # Initialize private properties.
        self._cmds = []
        self._xapi = None
        self._dapi = None
        self._lock = False

    def lock(self):
        "Lock the request."
        # <- self
        self._lock = True
        return self

    def copy(self):
        "Create a derived request."
        # <- derived request, same subclass of Req.
        return type(self)(self)

    def exp(self, *keys):
        "Mark the passed keys as required."
        # -> keys: required keys, Rkey+.
        # <- self.
        for key in keys:
            self._exp |= key
        return self

    def edit(self):
        "Ensure the request is editable."
        # <- self.
        if self._lock:
            # The request is locked.
            raise ErrReqEdit(self)
        return self

    def set(self, key, req, let, *val):
        "Add a command."
        # -> key: command key, one of Rkeys.
        # -> req: times the command is required (ONE, NONE).
        # -> let: times the command can be added (ONE, ANY).
        # -> val: command value, as appropriate, opaque (0 to 2 objects).
        # <- self.
        if let is ONE:
            # The request allows at most one such command.
            if self.isSet(key):
                # The request already has this command.
                raise ErrReqSet(self, key)
        # Mark the command as set.
        self._set |=  key
        if req is ONE:
            # The request requires this command. Mark as no longer required.
            self._exp &= ~key
        self._cmds.append(Rcmd(key, val))
        return self

    def isSet(self, key):
        "Test if a key is set."
        # -> key: the key to test, Rkey.
        # <- whether the key is set, boolean.
        return (self._set & key)

    def unset(self, key):
        "Mark the key as not set."
        # -> key: the key to mark as not set, Rkey.
        # <- self.
        self._set &= ~key
        return self

    def ownCmds(self):
        "Iterate over commands of this request only."
        # <- iterator over commands of this request.
        yield from self._cmds

    def allCmds(self):
        "Iterator over commands of this request and its bases."
        # <- iterator over all commands.
        yield from reversed(self._cmds)
        if self.base:
            yield from self.base.allCmds()

    def rfmt(self, api):
        "Get the request in the specified format."
        # -> api: leaf Api subclass, such as ApiXmlOld.
        # <- request in appropriate format, RfmtXapi or RfmtDapi.
        if issubclass(api, ApiXml):
            if not self._xapi:
                if not hasattr(self, "Xapi"):
                    # The request cannot be sent to XML API.
                    raise ErrReqRfmtReqApi(self, api)
                self._xapi = RfmtXapi(self)
            r = self._xapi
        elif issubclass(api, ApiData):
            if not self._dapi:
                if not hasattr(self, "Dapi"):
                    # The request cannot be sent to Data API.
                    raise ErrReqRfmtReqApi(self, api)
                self._dapi = RfmtDapi(self)
            r = self._dapi
        else:
            # Unknown API.
            raise ErrReqRfmtApi()
        return r

    def send(self, srv, user, session, api):
        "Send a request to the server. Internal method."
        # -> srv: server, Srv or None.
        # -> user: user, User or None.
        # -> session: session, Session or None.
        # -> api: api, Api or None.
        if self._exp:
            # Some required fields are not yet set.
            raise ErrReqSendExp(self)
        srv = session.srv if session else srv
        if api:
            # See if the handler is compatible. Do not override.
            if issubclass(api, ApiData) and  not hasattr(self, "Dapi")    \
            or issubclass(api, ApiXml ) and (not hasattr(self, "Xapi")    \
                  or type(self) is     ReqLayFmt and api is not ApiXmlLay \
                  or type(self) is not ReqLayFmt and api is     ApiXmlLay):
                # Cannot send this request to this API.
                raise ErrReqSendApi(self, api)
        else:
            # Determine the handler.
            prts = [ApiXml  if hasattr(self, "Xapi") else None, 
                    ApiData if hasattr(self, "Dapi") else None]
            apis = [session.api if session else None, srv.api, defaultApi]
            for prt, api in IterProduct(prts, apis):
                if api and prt and issubclass(api, prt):
                    # found a suitable handler 
                    if prt is ApiXml:
                        # XML handlers are not universal.
                        if type(self) is ReqLayFmt:
                            # Requires a specific handler.
                            api = ApiXmlLay
                        elif api is ApiXmlLay:
                            # Not suitable for other requests.
                            warnings.warn("Misuse of ApiXmlLay: do "
                                    "not set it as default.")
                            api = ApiXmlNew 
                    # Stop search.
                    break
            else:
                # Not found; assuming 'defaultApi' is always set this means
                # that none of found apis match the required protocol. In this
                # case the required protocol is the first and only protocol.
                if prts[0] is ApiXml:
                    # Default for XML calls.
                    api = ApiXmlNew
                else:
                    # Default for Data calls.
                    api = ApiDataLatest
        if self.Auth == "none":
            # No authentification is necessary.
            auth = None
        else:
            # May require authentification.
            if not user:
                user = session.user if session else srv.user or defaultUser
            if self.Auth == "cond":
                # Basic authentification, may be optional.
                auth = user
            elif not user:
                # No user (and no session) but authentification is mandatory.
                raise ErrReqSendAuth(self)
            elif issubclass(api, ApiXml):
                # XML API uses basic authentification.
                auth = user
            else:
                # Data API uses session authentification.
                # Not yet handled
                raise ErrReqSendData(self)
        return RespSrv(self, api, self.rfmt(api).httpReq(api).send(srv, auth))

# ----------------------------------------------------------------------------
# Constants to specify whether a command is required or can only be set once.

ONE  = object()  # used in 'req' or 'let'.
NONE = object()  # used in 'req'; also in Auth.
ANY  = object()  # used in 'let'

# ----------------------------------------------------------------------------

class ErrReqInit(Exception):
    def __str__(self):
        selfType, base = self.args
        return "Cannot use a request of one type as a base request for " \
                "another (request '%s', base '%s')." \
                % (selfType.__name__, type(base).__name__)

class ErrReqEdit(Exception):
    def __str__(self):
        req = self.args
        return "Cannot change this instance of '%s' because it has been " \
                "locked." % type(req).__name__

class ErrReqSet(Exception):
    def __str__(self):
        req, key = self.args
        return "Request '%s': cannot set '%s' because it has been set " \
                "already." % (type(req).__name__, key.name)

class ErrReqSendExp(Exception):
    def __str__(self):
        req, = self.args
        b = StringIO()
        b.write("Cannot prepare a request in the final format because some "
                "required attributes are not set, specifically: ")
        sep = False
        for key in (COL, DB, LAY1, RECID, REQ, SCR1, SCR2, SCR2):
            if key & req._exp:
                if sep:
                    b.write(", ")
                b.write("'")
                b.write(key.name)
                b.write("'")
                sep = True
        b.write(".")
        return b.getvalue()

class ErrReqSendApi(Exception):
    def __str__(self):
        req, api = self.args
        return "Cannot send '%s' to '%s'." % (type(req).__name__, 
                api.__name__)

class ErrReqSendAuth(Exception):
    def __str__(self):
        req, = self.args
        return "Request '%s' needs authentification, but no data is given " \
                "(expected User or Session)." % type(req).__name__

class ErrReqSendData(Exception):
    def __str__(self):
        req, = self.args
        return "Cannot yet send '%s' to Data API: in development." % \
                type(req).__name__

class ErrReqRfmtReqApi(Exception):
    def __str__(self):
        req, api = self.args
        return "Cannot send '%s' to '%s'." % (type(req).__name__,
                api.__name__)

class ErrReqRfmtApi(Exception):
    def __str__(self):
        return "Unknown API; expected a leaf subclass of '%s' or '%s'." % \
                (ApiXml.__name__, ApiData.__name__)

# ----------------------------------------------------------------------------

class ReqDb(Req):
    "A mixin for 'db' command."

    def db(self, val):
        "Add a 'db' command."
        # -> val: file name, str.
        # <- self.
        self.edit().set(DB, ONE, ONE, val)
        # Cache the file name to be able to create a session.
        self.file = Name(val) # will be compared.
        return self

# ----------------------------------------------------------------------------

class ReqLay(ReqDb):
    "A mixin for 'db' and 'lay' commands."

    def lay1(self, val):
        "Set the entry layout."
        # -> val: layout name, str.
        # <- self
        return self.edit().set(LAY1, ONE, ONE, val)

    # Synonym for 'lay1'.
    lay = lay1

# ----------------------------------------------------------------------------

class ReqCol(Req):
    "A mixing for 'col' command when adding or updating a record."

    def col(self, req, col, val):
        "Common method to set a record field."
        # req: type-specific 'req' value (ONE, NONE).
        # col: FileMaker field name, str.
        # val: FileMaker field value, Val-convertible.
        self.edit()
        col = Name(col)
        for cmd in self.allCmds():
            if cmd.key is COL and cmd.val[0] == col:
                # The field has been set.
                raise ErrReqColCol(self, col)
        return self.set(COL, req, ANY, col, Val(val))

class ErrReqColCol(Exception):
    def __str__(self):
        req, col, = self.args
        return "%s: Cannot set the same field twice (field '%s')" % \
                (type(req).__name__, col)

# ----------------------------------------------------------------------------

class ReqRid(Req):
    "A mixin for 'recid' command."

    def recid(self, val):
        "Set the internal record ID."
        # -> val: internal record ID, int.
        # <- self.
        return self.edit().set(RECID, ONE, ONE, val)

# ----------------------------------------------------------------------------

class ReqMid(Req):
    "A mixin for 'modid' command."

    def modid(self, val):
        "Set the internal record version."
        # -> val: internal version, int.
        # <- self
        return self.edit().set(MODID, NONE, ONE, val)

# ----------------------------------------------------------------------------

class ReqFset(Req):
    "A mixin for 'max', 'skip', and 'sort' commands."

    def max(self, val):
        "Set the fetch limit."
        # -> val: maximal number of records to fetch, int.
        # <- self.
        return self.edit().set(MAX, NONE, ONE, val)

    def skip(self, val):
        "Set the fetch offset."
        # -> val: fetch offset, int
        # <- self.
        return self.edit().set(SKIP, NONE, ONE, val)

    def sort(self, col, val):
        "Add a sort step."
        # -> col: FileMaker field name, str.
        # -> val: sort order, str; 'asc', 'desc' or valuelist name.
        return self.edit().set(SORT, NONE, ANY, col, val)

# ----------------------------------------------------------------------------

class ReqScr3(Req):
    "A mixin for 'par3' and 'scr3' commands."

    def setPar(self, parKey, scrKey, vals):
        "Add a script parameter."
        # -> parKey: parameter key (PAR1, PAR2, PAR3).
        # -> scrKey: corresponding script key (SCR1, SCR2, SCR3).
        # -> vals: parameter value, tuple of Val-convertibles.
        # <- self.

        # A script may take any value that can be converted to 'Val'. (Values
        # that are already instances of 'Val' subclasses are passed as is.) A
        # script may also take multiple values. When this happens we convert
        # each value into a 'Val' (which is a subclass of 'str') and then
        # concatenate the resulting strings with the CR character ('\r'),
        # which is the default newline character in FileMaker.
        self.edit().set(parKey, NONE, ONE, "\r".join((Val(v) for v in vals)))
        # Having a parameter implies we need the corresponding script.
        if not self.isSet(scrKey):
            self.exp(scrKey)
        return self

    def par3(self, *args):
        "Set the parameter for the third script (main)."
        # -> args: parameter data, Val-compatible.
        # <- self.
        return self.setPar(PAR3, SCR3, args)

    # Synonym for 'par3'.
    par = par3

    def setScr(self, key, val):
        "Add a script."
        # -> key: script key (SCR1, SCR2, SCR3).
        # -> val: script name, str.
        # <- self.
        return self.edit().set(key, ONE, ONE, val)

    def scr3(self, val):
        "Set the first script."
        # -> val: script name, str.
        # <- self.
        return self.setScr(SCR3, val)

    # Synonym for 'scr3'.
    scr = scr3

# ----------------------------------------------------------------------------

class ReqCmn(ReqScr3, ReqFset):
    "A mixin for 'par1..3', 'scr1..3', 'max', 'skip' and 'sort' commands."

    def lay2(self, val):
        "Set the exit layout."
        # -> val: layout name, str.
        # <- self.
        return self.edit().set(LAY2, NONE, ONE, val)

    def par1(self, *args):
        "Set the parameter for the first script (prefind)."
        # -> args: parameter data, Val-compatible.
        # <- self.
        return self.setPar(PAR1, SCR1, args)

    def par2(self, *args):
        "Set the parameter for the second script (presort)."
        # -> args: parameter data, Val-compatible.
        # <- self.
        return self.setPar(PAR2, SCR2, args)

    def scr1(self, val):
        "Set the first script."
        # -> val: script name, str.
        # <- self.
        return self.setScr(SCR1, val)

    def scr2(self, val):
        "Set the second script."
        # -> val: script name, str.
        # <- self.
        return self.setScr(SCR2, val)

# ----------------------------------------------------------------------------
# Request subclasses.

class ReqSrvInf(Req):
    "Request to get general information about a server."

    Auth = "none"
    Dapi = "GET", "productInfo"
    rtyp = "srvInf"

# ----------------------------------------------------------------------------

class ReqSrvDbs(Req):
    "Request to list server files."

    Auth = "cond"
    Xapi = "-dbnames"
    Dapi = "GET", "databases"
    rtyp = "srvDbs"

# ----------------------------------------------------------------------------

class ReqDbLays(ReqDb):
    "Request to list file layouts."

    Xapi = "-layoutnames"
    Dapi = "GET", "databases/{db}/layouts"
    rtyp = "dbLays"
    Exp = DB

# ----------------------------------------------------------------------------

class ReqDbScrs(ReqDb):
    "Request to list file scripts."

    Xapi = "-scriptnames"
    Dapi = "GET", "databases/{db}/scripts"
    rtyp = "dbScrs"
    Exp = DB

# ----------------------------------------------------------------------------

class ReqLayAll(ReqLay, ReqCmn):
    "Request to view all records on a layout."

    Xapi = "-findall"
    Dapi = "GET", "databases/{db}/layouts/{lay}/records"
    Exp = DB | LAY1

# ----------------------------------------------------------------------------

class ReqLayAny(ReqLay, ReqCmn):
    "Request to do something starting with no record or a random record."

    Xapi = "-findany"
    # Not available in Data API. See also 'ReqLayScr'.
    Exp = DB | LAY1

# ----------------------------------------------------------------------------

class ReqLayOne(ReqLay, ReqRid, ReqCmn):
    "Request to view a single record."

    Xapi = "-find"
    Dapi = "GET", "databases/{db}/layouts/{lay}/records/{rec}"
    Exp = DB | LAY1 | RECID

# ----------------------------------------------------------------------------

class ReqLayScr(ReqLay, ReqScr3, ReqFset):
    "Request to run a script."

    # The XML API does not really have a request to run a script, but it is an
    # important request type, so we piggyback '-findany' to imitate it. Since
    # it is a synthesized request, we limit its commands artificially:allow
    # only one script (final, #3), make it required, allow only the entry
    # layout, allow found set shaping.

    Xapi = "-findany"
    Dapi = "GET", "databases/{db}/layouts/{lay}/scripts/{scr}"
    Exp = DB | LAY1 | SCR3

# ----------------------------------------------------------------------------

class ReqLaySel(ReqLay, ReqCmn):

    Xapi = "-findquery"
    Dapi = "POST", "databases/{db}/layouts/{lay}/_find"
    Exp = DB | LAY1 | REQ

    # The 'col' command in find request is unique.
    def col(self, col, val):
        "Set a field value when searching for records."
        # -> col, val: field name and value.
        # <- self.
        self.edit()
        col = Name(col)
        if self.isSet(COL):
            # At least one field has been set; check.
            for cmd in self.allCmds():
                if cmd.key is COL and cmd.val[0] == col:
                    # The field has been set for this request.
                    raise ErrReqLaySelCol(col)
                elif cmd.key is REQ:
                    # Checked all fields in the current request.
                    break
        elif not self.isSet(REQ):
            # Automatically add a find request.
            self.set(REQ, ONE, ANY)
        return self.set(COL, ONE, ANY, col, Val(val))

    def omit(self):
        "Mark the current find request as omit request."
        if not self.edit().isSet(REQ):
            # No request has been added; automatically add one.
            self.set(REQ, ONE, ANY)
        return self.set(OMIT, NONE, ONE)

    def req(self):
        "Add a new find request."
        # <- self.
        self.edit()
        if self.isSet(REQ) and not self.isSet(COL):
            # The previous request has no fields.
            raise ErrReqLaySelReq()
        return self.set(REQ, ONE, ANY).unset(OMIT).exp(COL)

class ErrReqLaySelCol(Exception):
    def __str__(self):
        col, = self.args
        return "Cannot set the same field twice in the same find request " \
                "(field '%s')" % col

class ErrReqLaySelReq(Exception):
    def __str__(self):
        return "Cannot add a find request because the previous find request "\
                "has no fields."

# ----------------------------------------------------------------------------

class ReqLayNew(ReqLay, ReqCol, ReqCmn):
    "Request to add a record."

    Xapi = "-new"
    Dapi = "POST", "databases/{db}/layouts/{lay}/records"
    Exp = DB | LAY1

    def col(self, col, val):
        "Set a field value when inserting a record."
        # -> col, val: FileMaker field name and value.
        # <- self.
        return super().col(NONE, col, val)

# ----------------------------------------------------------------------------

class ReqRecDup(ReqLay, ReqRid, ReqMid, ReqCmn):
    "Request to duplicate a record."

    Xapi = "-dup"
    Dapi = "POST", "databases/{db}/layouts/{lay}/records/{rec}"
    Exp = DB | LAY1 | RECID

# ----------------------------------------------------------------------------

class ReqRecUpd(ReqLay, ReqCol, ReqRid, ReqMid, ReqCmn):
    "Request to edit a record."

    Xapi = "-edit"
    Dapi = "PATCH", "databases/{db}/layouts/{lay}/records/{rec}"
    Exp = DB | LAY1 | RECID | COL

    def col(self, col, val):
        "Set a field value when updating a record."
        # -> col, val: FileMaker field name and value.
        # <- self.
        return super().col(ONE, col, val)

# ----------------------------------------------------------------------------

class ReqRecDel(ReqLay, ReqRid, ReqMid, ReqCmn):
    "Request to delete a record."

    Xapi = "-delete"
    Dapi = "DELETE", "databases/{db}/layouts/{lay}/records/{rec}"
    Exp = DB | LAY1 | RECID

# ----------------------------------------------------------------------------

class ReqLayInf(ReqLay):
    "Request to view layout information."

    Xapi = "-view"
    Dapi = "GET", "databases/{db}/layouts/{lay}"
    rtyp = "layInf"
    Exp = DB | LAY1

# ----------------------------------------------------------------------------

class ReqLayFmt(ReqLay, ReqRid):
    "Request to read layout formatting details."

    Xapi = "-view"
    Dapi = "GET", "databases/{db}/layouts/{lay}"
    rtyp = "layFmt"
    Exp = DB | LAY1

# ============================================================================
# Request in a specific format.

class Rfmt:

    __slots__ = "_req"

    # _req: request, Req.

    def __init__(self, req):
        # -> req: request, subclass of Req.
        self._req = req.lock()

# ----------------------------------------------------------------------------
# Request in the XML format.

# XML API requests are form submissions (x-www-form-urlencoded). Data are sent
# as key-value pairs, for example '-skip=10'. There is also a single-key
# command that identifies the request type, e.g. '-find'. Most commands are
# fully set in a single step. The '-findquery' command, however, is a picture
# of find reqests like 'q1;(q2,q3);!q4'. Here each 'q' refers to a single
# criterion (field and search pattern) and the overall structure identifies
# individual requests and find/omit state. There is also a format-specific
# limit on the number of sort steps: 9.

class RfmtXapi(Rfmt):

    __slots__ = "_fkey", "_qreq", "_qcol", "_omit", "_qnxt", "_slen", "_data"

    # _fkey: form keys.
    # _qreq: find request pictures, [str], e.g. ['(q1)', '!(q2, q3)'].
    # _qcol: fields for the current find request, [str], e.g. ['q4', 'q5'].
    # _omit: whether the current find request is to be omitted, bool.
    # _qnxt: next find request field number, int.
    # _slen: number of sort commands, int.
    # _data: rendered form data.

    def __init__(self, req):
        super().__init__(req)
        if not req.base:
            self._fkey = [req.Xapi]
            self._qreq = []
            self._qcol = []
            self._omit = False
            self._qnxt = 1
            self._slen = 0
        else:
            base = req.base.rfmt(ApiXml)
            self._fkey = Copy(base._fkey)
            self._qreq = Copy(base._qreq)
            self._qcol = Copy(base._qcol)
            self._omit = base._omit
            self._qnxt = base._qnxt
            self._slen = base._slen
        for cmd in req.ownCmds():
            getattr(self, cmd.key.name)(*cmd.val)
        self._fkey[:] = ["&".join(self._fkey)]
        if not (self._qreq or self._qcol):
            qval = []
        else:
            qval = ["-query=" + ";".join(self._qreq + self.qreq())]
        self._data = "&".join(self._fkey + qval)

    # A general method to add a key.

    def addKey(self, *pcs):
        "Add a key."
        # -> pcs: key pieces, str+.
        self._fkey.append("".join(pcs))

    def qreq(self):
        "Get a picture of the current request."
        # <- picture of the current request, [str?], e.g. ['!(q3,q4)'].
        b = StringIO()
        if self._qcol:
            if self._omit:
                b.write("!")
            b.write("(")
            b.write(",".join(self._qcol))
            b.write(")")
        return [b.getvalue()]

    # ------------------------------------------------------------------------

    # All commands below:
    # -> cmd: request command of the corresponding type, Cmd.

    def col(self, col, val):
        "Format the 'col' command."
        # -> col, val: FileMaker field name and value.
        if type(self._req) is ReqLaySel:
            # Select.
            qcol = "q" + str(self._qnxt)
            self._qnxt += 1
            self._qcol.append(qcol)
            self.addKey("-", qcol, "="      , UrlEncode(col))
            self.addKey("-", qcol, ".value=", UrlEncode(val))
        else:
            # Insert or update.
            self.addKey(UrlEncode(col), "=", UrlEncode(val))

    def db(self, name):
        self.addKey("-db=", UrlEncode(name))

    def lay1(self, name):
        self.addKey("-lay=", UrlEncode(name))

    def lay2(self, name):
        self.addKey("-lay.response=", UrlEncode(name))

    def max(self, val):
        self.addKey("-max=", str(val))

    def modid(self, val):
        self.addKey("-modid=", str(val))

    def omit(self):
        self._omit = True

    def par1(self, val):
        self.addKey("-script.prefind.param=", UrlEncode(val))

    def par2(self, val):
        self.addKey("-script.presort.param=", UrlEncode(val))

    def par3(self, val):
        self.addKey("-script.param=", UrlEncode(val))

    def recid(self, val):
        self.addKey("-recid=", str(val))

    def req(self):
        if self._qcol:
            self._qreq.extend(self.qreq())
            self._qcol.clear()
            self._omit = False

    def scr1(self, name):
        self.addKey("-script.prefind=", UrlEncode(name))

    def scr2(self, name):
        self.addKey("-script.presort=", UrlEncode(name))

    def scr3(self, name):
        self.addKey("-script=", UrlEncode(name))

    def skip(self, val):
        self.addKey("-skip=", str(val))

    def sort(self, col, dir):
        if self._slen == 9:
            # An XAPI request can have at most 9 sort commands.
            raise ErrRfmtXapiSort()
        self._slen += 1
        snum = str(self._slen)
        self.addKey("-sortfield.", snum, "=", UrlEncode(col))
        self.addKey("-sortorder.", snum, "=", UrlEncode(dir))

    # ------------------------------------------------------------------------

    def httpReq(self, api):
        "Create an HTTP request."
        # -> api: API, a subclass of ApiXml.
        # <- HTTP request, HttpREq
        uri = "/fmi/xml/" + api.Ver + ".xml"
        return HttpReq("POST", uri, self._data, "x-www-form-urlencoded")

class ErrRfmtXapiSort(Exception):
    def __str__(self):
        return "Requests to the XML API can have at most 9 sort steps."

# ----------------------------------------------------------------------------
# Request in the data format.

class RfmtDapi(Rfmt):

    __slots__ = "_verb", "_path", "_data"

    # _verb: HTTP verb.
    # _path: partial resource path.
    # _data: request data.

    def __init__(self, req):
        super().__init__(req)
        verb, path = req.Dapi
        self._verb = verb
        self._path = [path]
        self._data = None

    def httpReq(self, diff):
        "Create an HTTP request."
        # -> diff: the Data API difference, str: 'v1', 'v2' or 'vLatest'.
        uri = "/fmi/data/" + diff + "/" + "".join(self._path)
        data = self._data
        if data:
            mime = "application/json"
        else:
            mime = None
        return HttpReq(self._verb, uri, data, mime)

    def httpReq(self, api):
        "Create an HTTP request."
        # -> api: API, a subclass of ApiXml.
        # <- HTTP request, HttpREq
        uri = "/fmi/data/" + api.Ver + "/" + "".join(self._path)
        data = self._data
        if data:
            mime = "application/json"
        else:
            mime = None
        return HttpReq(self._verb, uri, data, mime)


# ============================================================================
# A session is an object to store the authentification token when calling the
# Data API.

class Session:

    __slots__ = "srv", "file", "user", "dflApi", "curApi", "token", "authHdr"

    # srv    : server, Srv.
    # file   : file name, Name.
    # user   : user, User or None.
    # dflApi : default API, Api or None.
    # curApi : active API, Api or None.
    # token  : session token, str.
    # authHdr: value for the 'authorization' header.

    def __init__(self, srv, file, user, api=None):
        # -> srv: server, Srv.
        # -> file: file name, str.
        # -> user: user, User.
        # -> api: default API, Api or None.
        self.srv = srv
        self.file = Name(file)
        self.user = user
        self.dflApi = api
        self.curApi = None
        self.token = None
        self.authHdr = None

    def __enter__(self):
        if not self.token:
            self.login()

    def __exit__(self, cls, val, trc):
        try:
            self.logout()
        except Exception as e:
            # Do not raise this exception but issue a warning.
            warnings.warn("Error when logging out a session: %s" % e)

    def __del__(self):
        self.logout()

    def login(self, api=None):
        "Log in."
        # -> api: API to use or None.
        # <- self.
        if api:
            # Got an explicit API.
            if not issubclass(api, ApiData):
                # Sessions only exist in Data API.
                raise ErrSessionLoginApi(self, api)
        else:
            # Got no API; search.
            for api in (self.api, self.srv.api, defaultApi):
                if api and issubclass(api, ApiData):
                    # Found a Data API; use.
                    break
            else:
                # Found no data API; use the default.
                api = ApiDataLatest
        # Terminate the current session, if any (no-op if not logged in).
        self.logout()
        url = "/fmi/data/%s/databases/%s/sessions" % (api.Ver, self.file)
        httpReq = HttpReq("POST", url, "{}", "application/json")
        httpResp = httpReq.send(self.srv, self.user)
        if httpResp.error:
            raise httpResp.error
        self.curApi = api
        self.token = httpResp.header("x-fm-data-access-token")
        self.authHdr = "bearer %s" % self.token
        return self

    def logout(self):
        "Log out."
        # <- self.
        if self.token:
            url = "/fmi/data/%s/databases/%s/sessions/%s" % \
                    (self.curApi.Ver, self.file, self.token)
            httpResp = HttpReq("DELETE", url).send(self.srv, self)
            self.curApi = None
            self.token = None
            self.authHdr = None
            if httpResp.error:
                raise httpResp.error
        return self

    @property
    def api(self):
        "Current or default API."
        # <- api, Api or None.
        return self.curApi or self.dflApi

    @property
    def auth(self):
        "The value for the 'authorization' header."
        # <- header value, str.
        if not self.token:
            self.login()
        return self.authHdr

    def send(self, req, api=None):
        "Send a request using the session and return the response."
        # -> req: request, subclass of Req.
        # -> api: API, Api or None.
        # <- response, RespSrv.
        return req.send(None, None, self, api)

# ----------------------------------------------------------------------------

class ErrSessionLoginApi(Exception):
    def __str__(self):
        session, api = self.args
        return "%r: the '%s' API does not require login." % \
                (session, api.__name__)

class ErrSessionLoginUser(Exception):
    def __str__(self):
        session, = self.args
        return "%r: failed to login because found no user." % session

# ============================================================================
# LayDesc is a layout description that stores information not provided by
# FileMaker responses. If we read a response (usually a set of records) using
# a LayDesc, the created layout specifications (LaySpec) are cached in the
# LayDesc.

class LayDesc:

    __slots__ = "_cnamToRnam", "_rnams", "_cnamToReps", "_slots"
    
    # _cnamToRnam : map from field name to portal table name, {Name:Name}.
    # _rnams : table names, {Name}.
    # _cnamToReps : map from field name to number of repetitions, {Name:int}.
    # _slots : layout slots, {class:LaySlot}.
    
    def __init__(self):
        self._cnamToRnam = {}
        self._rnams = set()
        self._cnamToReps = {}
        self._slots = {}

    def col(self, colName, reps):
        "Set the number of repetitions."
        # -> colName: field name, str.
        # -> reps: number of repetitions, int.
        # <- self.
        colName = ColName(colName)
        try:
            setReps = self._cnamToReps[colName]
        except KeyError:
            self._cnamToReps[colName] = reps
        else:
            if setReps != reps:
                # The column already has a different number of repetitions.
                raise ErrLayDescCol(colName, reps, setReps)
        return self

    def rel(self, relName, *colNames):
        "Bind fields to a portal."
        # -> relName: portal table name, str.
        # -> colNames: portal field names, str+.
        # <- self.
        relName = Name(relName)
        colNames = [ColName(colName, relName) for colName in colNames]
        for colName in colNames:
            try:
                setRelName = self._cnamToRnam[colName]
            except KeyError:
                pass
            else:
                if setRelName != relName:
                    # The column already belongs to a different portal.
                    raise ErrLayDescRel(colName, relName, setRelName)
        for colName in colNames:
            self._cnamToRnam[colName] = relName
            # Do not add remember empty names.
            if relName:
                self._rnams.add(relName)
        return self

    def lay(self, *colNames):
        "Bind fields to a layout."
        # -> colNames: layout field names, str+.
        # <- self.
        return self.rel(emptyName, *colNames) 

    def relName(self, colName):
        "Portal table name for this field, empty when on layout."
        # -> colName: field name, ColName.
        # <- portal table name, Name or None.
        return self._cnamToRnam.get(Name(colName))

    def colReps(self, colName):
        "Number of displayed repetitions for this field."
        # -> colName: field name, ColName.
        # <- number of repetitions, int or None.
        return self._cnamToReps.get(Name(colName))

    def laySlot(self, cls):
        "Get a layout slot for this class."
        # -> cls: the layout class, subclass of Lay, e.g. LayOld.
        # -> key: the slot key, bytes.
        # <- layout slot, LaySlot.
        try:
            r = self._slots[cls]
        except KeyError:
            r = self._slots[cls] = LaySlot()
        return r

    def relNames(self):
        "Return an iterator over portal table names."
        # <- an iterator over portal table names, Name.
        yield from self._rnams

# ----------------------------------------------------------------------------

class ErrLayDescCol(Exception):
    def __str__(self):
        colName, reps, setReps = self.args
        return "Cannot set the number of repetitions of '%s' to '%d' " \
                "because it has already been set to '%d'." % (colName, reps,
                setReps)

class ErrLayDescRel(Exception):
    def __str__(self):
        colName, relName, setRelName = self.args
        buf = StringIO()
        buf.write("Cannot bind the field '")
        buf.write(colName)
        buf.write("' to the ")
        if relName:
            buf.write("portal '")
            buf.write(relName)
            buf.write("'")
        else:
            buf.write("layout")
        buf.write("because it is already bound to the ")
        if setRelName:
            buf.write("portal '")
            buf.write(setRelName)
            buf.write("'")
        else:
            buf.write("layout")
        buf.write(".")
        return buf.getvalue()

# ============================================================================
# A slot to cache a layout specification in a layout description.

class LaySlot:

    __slots__ = "key", "lay"

    # key: key that identifies the layout, None, then bytes.
    # lay: cached layout specification, None, then LaySpec.

    def __init__(self):
        self.key = None
        self.lay = None

# ============================================================================

class Resp:

    __slots__ = "req", "api"

    # req: the request that produced the response, subclass of Req or None.
    # api: the API that returned the response, Api or None.

    def __init__(self, req=None, api=None):
        self.req = req
        self.api = api

    def read(self, *hints):
        # -> hints: reading hints, such as LayDesc.
        # <- response, ErrFm, [Name|Folder?|Sep?], LaySpec, Recset.
        if self.error:
            raise self.error
        if self.api: # this means we have 'req' as well.
            # Use the known API and request
            api = self.api
            req = self.req
            data = api.read(self.data)
        else:
            # Cannot determine the request, but can guess the API.
            req = None
            for api in (ApiXml, ApiData):
                try:
                    data = api.read(self.data)
                    break
                except:
                    continue
            else:
                # Neither XML nor JSON.
                raise ErrRespRead()
            if api is ApiXml:
                # XML; determine the specific API.
                tag = data.tag
                for api in (ApiXmlOld, ApiXmlNew, ApiXmlLay):
                    if api.Tag == tag:
                        break
                else:
                    # Unknown XML.
                    raise ErrRespReadXml(tag)
            else:
                # Data API is not yet supported.
                raise ErrRespReadDataApi()
        # Determine the error.
        enum, estr = api.error(data)
        if enum:
            # An error occurred.
            res = ErrFm(enum, estr)
        else:
            # No error; determine the result type.
            if req:
                # Each request knows the result type.
                rtyp = req.rtyp
            else:
                # No request; guess the approximate result type.
                rtyp = api.rtyp(data)
            # Read the response as that type.
            res = getattr(api, rtyp)(data, *hints)
        return res

class ErrRespRead(Exception):
    def __str__(self):
        return "Failed to read response data as XML or JSON."

class ErrRespReadXml(Exception):
    def __str__(self):
        tag, = self.args
        return "Unknown XML grammar '%s'." % tag

class ErrRespReadDataApi(Exception):
    def __str__(self):
        return "(In progress) Cannot yet read Data API responses."

# ----------------------------------------------------------------------------

class RespDisk(Resp):
    "A response read from a file."

    __slots__ = "data", "error"

    def __init__(self, file):
        # -> file: the file to read the data from, Python file.
        super().__init__()
        try:
            data = file.read()
        except Exception as e:
            error = e
            data = b""
        else:
            if not isinstance(data, bytes):
                # The file has to be binary.
                raise ErrRespDisk(data)
            error = None
        self.data = data
        self.error = error

class ErrRespDisk(Exception):

    def __str__(self):
        data, = self.args
        return "Expected to read bytes, got '%s'." % type(data)

# ----------------------------------------------------------------------------

class RespSrv(Resp):
    "A response received from FileMaker server."

    __slots__ = "httpResp"

    # httpResp: the underlying HTTP response, HttpResp.

    def __init__(self, req, api, httpResp):
        # -> req: request, subclass of Req.
        # -> api: API that serviced that request, Api.
        # -> httpResp: the underlying HTTP response, HttpResp.
        super().__init__(req, api)
        self.httpResp = httpResp

    @property
    def data(self):
        "Response data."
        # <- response data, bytes.
        return self.httpResp.data

    @property
    def error(self):
        "Transfer error."
        # <- response error, Exception or None..
        return self.httpResp.error

# ============================================================================

class ErrFm(Exception):

    TEXT = {
        -1: 'Unknown error',
         0: 'No error',
         1: 'User canceled action',
         2: 'Memory error',
         3: 'Command is unavailable (for example, wrong operating system or '
            'mode)',
         4: 'Command is unknown',
         5: 'Command is invalid (for example, a Set Field script step does '
            'not have a calculation specified)',
         6: 'File is read-only',
         7: 'Running out of memory',
         9: 'Insufficient privileges',
        10: 'Requested data is missing',
        11: 'Name is not valid',
        12: 'Name already exists',
        13: 'File or object is in use',
        14: 'Out of range',
        15: 'Can’t divide by zero',
        16: 'Operation failed; request retry (for example, a user query)',
        17: 'Attempt to convert foreign character set to UTF-16 failed',
        18: 'Client must provide account information to proceed',
        19: 'String contains characters other than A-Z, a-z, 0-9 (ASCII)',
        20: 'Command/operation canceled by triggered script',
        21: 'Request not supported (for example, when creating a hard link '
            'on a file system that does not support hard links)',

       100: 'File is missing',
       101: 'Record is missing',
       102: 'Field is missing',
       103: 'Relationship is missing',
       104: 'Script is missing',
       105: 'Layout is missing',
       106: 'Table is missing',
       107: 'Index is missing',
       108: 'Value list is missing',
       109: 'Privilege set is missing',
       110: 'Related tables are missing',
       111: 'Field repetition is invalid',
       112: 'Window is missing',
       113: 'Function is missing',
       114: 'File reference is missing',
       115: 'Menu set is missing',
       116: 'Layout object is missing',
       117: 'Data source is missing',
       118: 'Theme is missing',
       130: 'Files are damaged or missing and must be reinstalled',
       131: 'Language pack files are missing',

       200: 'Record access is denied',
       201: 'Field cannot be modified',
       202: 'Field access is denied',
       203: 'No records in file to print, or password doesn’t allow print '
            'access',
       204: 'No access to field(s) in sort order',
       205: 'User does not have access privileges to create new records; '
            'import will overwrite existing data',
       206: 'User does not have password change privileges, or file is not '
            'modifiable',
       207: 'User does not have privileges to change database schema, or '
            'file is not modifiable',
       208: 'Password does not contain enough characters',
       209: 'New password must be different from existing one',
       210: 'User account is inactive',
       211: 'Password has expired',
       212: 'Invalid user account or password',
       214: 'Too many login attempts',
       215: 'Administrator privileges cannot be duplicated',
       216: 'Guest account cannot be duplicated',
       217: 'User does not have sufficient privileges to modify '
            'administrator account',
       218: 'Password and verify password do not match',
       219: 'Cannot open file; must be licensed user; contact team manager',

       300: 'File is locked or in use',
       301: 'Record is in use by another user',
       302: 'Table is in use by another user',
       303: 'Database schema is in use by another user',
       304: 'Layout is in use by another user',
       306: 'Record modification ID does not match',
       307: 'Transaction could not be locked because of a communication '
            'error with the host',
       308: 'Theme is locked and in use by another user',

       400: 'Find criteria are empty',
       401: 'No records match the request',
       402: 'Selected field is not a match field for a lookup',
       404: 'Sort order is invalid',
       405: 'Number of records specified exceeds number of records that can '
            'be omitted',
       406: 'Replace/reserialize criteria are invalid',
       407: 'One or both match fields are missing (invalid relationship)',
       408: 'Specified field has inappropriate data type for this operation',
       409: 'Import order is invalid',
       410: 'Export order is invalid',
       412: 'Wrong version of FileMaker Pro used to recover file',
       413: 'Specified field has inappropriate field type',
       414: 'Layout cannot display the result',
       415: 'One or more required related records are not available',
       416: 'A primary key is required from the data source table',
       417: 'File is not a supported data source',
       418: 'Internal failure in INSERT operation into a field',

       500: 'Date value does not meet validation entry options',
       501: 'Time value does not meet validation entry options',
       502: 'Number value does not meet validation entry options',
       503: 'Value in field is not within the range specified in validation '
            'entry options',
       504: 'Value in field is not unique, as required in validation entry '
            'options',
       505: 'Value in field is not an existing value in the file, as '
            'required in validation entry options',
       506: 'Value in field is not listed in the value list specified in '
            'validation entry option',
       507: 'Value in field failed calculation test of validation entry '
            'option',
       508: 'Invalid value entered in Find mode',
       509: 'Field requires a valid value',
       510: 'Related value is empty or unavailable',
       511: 'Value in field exceeds maximum field size',
       512: 'Record was already modified by another user',
       513: 'No validation was specified but data cannot fit into the field',

       600: 'Print error has occurred',
       601: 'Combined header and footer exceed one page',
       602: 'Body doesn’t fit on a page for current column setup',
       603: 'Print connection lost',

       700: 'File is of the wrong file type for import',
       706: 'EPS file has no preview image',
       707: 'Graphic translator cannot be found',
       708: 'Can’t import the file, or need color monitor support to import '
            'file',
       711: 'Import translator cannot be found',
       714: 'Password privileges do not allow the operation',
       715: 'Specified Excel worksheet or named range is missing',
       716: 'A SQL query using DELETE, INSERT, or UPDATE is not allowed for '
            'ODBC import',
       717: 'There is not enough XML/XSL information to proceed with the '
            'import or export',
       718: 'Error in parsing XML file (from Xerces)',
       719: 'Error in transforming XML using XSL (from Xalan)',
       720: 'Error when exporting; intended format does not support '
            'repeating fields',
       721: 'Unknown error occurred in the parser or the transformer',
       722: 'Cannot import data into a file that has no fields',
       723: 'You do not have permission to add records to or modify records '
            'in the target table',
       724: 'You do not have permission to add records to the target table',
       725: 'You do not have permission to modify records in the target '
            'table',
       726: 'Source file has more records than the target table; not all '
            'records were imported',
       727: 'Target table has more records than the source file; not all '
            'records were updated',
       729: 'Errors occurred during import; records could not be imported',
       730: 'Unsupported Excel version; convert file to the current Excel '
            'format and try again',
       731: 'File you are importing from contains no data',
       732: 'This file cannot be inserted because it contains other files',
       733: 'A table cannot be imported into itself',
       734: 'This file type cannot be displayed as a picture',
       735: 'This file type cannot be displayed as a picture; it will be '
            'inserted and displayed as a file',
       736: 'Too much data to export to this format; data will be truncated',
       738: 'The theme you are importing already exists',

       800: 'Unable to create file on disk',
       801: 'Unable to create temporary file on System disk',
       802: 'Unable to open file',
       803: 'File is single-user, or host cannot be found',
       804: 'File cannot be opened as read-only in its current state',
       805: 'File is damaged; use Recover command',
       806: 'File cannot be opened with this version of a FileMaker client',
       807: 'File is not a FileMaker Pro file or is severely damaged',
       808: 'Cannot open file because access privileges are damaged',
       809: 'Disk/volume is full',
       810: 'Disk/volume is locked',
       811: 'Temporary file cannot be opened as FileMaker Pro file',
       812: 'Exceeded host’s capacity',
       813: 'Record synchronization error on network',
       814: 'File(s) cannot be opened because maximum number is open',
       815: 'Couldn’t open lookup file',
       816: 'Unable to convert file',
       817: 'Unable to open file because it does not belong to this solution',
       819: 'Cannot save a local copy of a remote file',
       820: 'File is being closed',
       821: 'Host forced a disconnect',
       822: 'FileMaker Pro files not found; reinstall missing files',
       823: 'Cannot set file to single-user; guests are connected',
       824: 'File is damaged or not a FileMaker Pro file',
       825: 'File is not authorized to reference the protected file',
       826: 'File path specified is not a valid file path',
       827: 'File was not created because the source contained no data or is '
            'a reference',
       850: 'Path is not valid for the operating system',
       851: 'Cannot delete an external file from disk',
       852: 'Cannot write a file to the external storage',
       853: 'One or more containers failed to transfer',
       870: 'Cannot modify file because another user is modifying it',
       871: 'Error occurred loading Core ML model',
       872: 'Core ML model was not loaded because it contained an '
            'unsupported input or output parameter',
       900: 'General spelling engine error',
       901: 'Main spelling dictionary not installed',
       903: 'Command cannot be used in a shared file',
       905: 'Command requires a field to be active',
       906: 'Current file is not shared; command can be used only if the '
            'file is shared',
       920: 'Cannot initialize the spelling engine',
       921: 'User dictionary cannot be loaded for editing',
       922: 'User dictionary cannot be found',
       923: 'User dictionary is read-only',
       951: 'An unexpected error occurred (*)',
       952: 'Invalid FileMaker Data API token (*)',
       953: 'Exceeded limit on data the FileMaker Data API and OData can '
            'transmit (*)',
       954: 'Unsupported XML grammar (*)',
       955: 'No database name (*)',
       956: 'Maximum number of database or Admin API sessions exceeded (*)',
       957: 'Conflicting commands (*)',
       958: 'Parameter missing (*)',
       959: 'Custom Web Publishing technology is disabled',
       960: 'Parameter is invalid',

      1200: 'Generic calculation error',
      1201: 'Too few parameters in the function',
      1202: 'Too many parameters in the function',
      1203: 'Unexpected end of calculation',
      1204: 'Number, text constant, field name, or “(” expected',
      1205: 'Comment is not terminated with “*/”',
      1206: 'Text constant must end with a quotation mark',
      1207: 'Unbalanced parenthesis',
      1208: 'Operator missing, function not found, or “(” not expected',
      1209: 'Name (such as field name or layout name) is missing',
      1210: 'Plug-in function or script step has already been registered',
      1211: 'List usage is not allowed in this function',
      1212: 'An operator (for example, +, -, *) is expected here',
      1213: 'This variable has already been defined in the Let function',
      1214: 'A function parameter contains an expression where a field is '
            'required',
      1215: 'This parameter is an invalid Get function parameter',
      1216: 'Only summary fields are allowed as first argument in GetSummary',
      1217: 'Break field is invalid',
      1218: 'Cannot evaluate the number',
      1219: 'A field cannot be used in its own formula',
      1220: 'Field type must be normal or calculated',
      1221: 'Data type must be number, date, time, or timestamp',
      1222: 'Calculation cannot be stored',
      1223: 'Function referred to is not yet implemented',
      1224: 'Function referred to does not exist',
      1225: 'Function referred to is not supported in this context',

      1300: 'The specified name can’t be used',
      1301: 'A parameter of the imported or pasted function has the same '
            'name as a function in the file',

      1400: 'ODBC client driver initialization failed; make sure ODBC client '
            'drivers are properly installed',
      1401: 'Failed to allocate environment (ODBC)',
      1402: 'Failed to free environment (ODBC)',
      1403: 'Failed to disconnect (ODBC)',
      1404: 'Failed to allocate connection (ODBC)',
      1405: 'Failed to free connection (ODBC)',
      1406: 'Failed check for SQL API (ODBC)',
      1407: 'Failed to allocate statement (ODBC)',
      1408: 'Extended error (ODBC)',
      1409: 'Error (ODBC)',
      1413: 'Failed communication link (ODBC)',
      1414: 'SQL statement is too long',
      1415: 'Connection is being disconnected (ODBC)',
      1450: 'Action requires PHP privilege extension (*)',
      1451: 'Action requires that current file be remote',

      1501: 'SMTP authentication failed',
      1502: 'Connection refused by SMTP server',
      1503: 'Error with SSL',
      1504: 'SMTP server requires the connection to be encrypted',
      1505: 'Specified authentication is not supported by SMTP server',
      1506: 'Email message(s) could not be sent successfully',
      1507: 'Unable to log in to the SMTP server',
      1550: 'Cannot load the plug-in, or the plug-in is not a valid plug-in',
      1551: 'Cannot install the plug-in; cannot delete an existing plug-in '
            'or write to the folder or disk',

      1626: 'Protocol is not supported',
      1627: 'Authentication failed',
      1628: 'There was an error with SSL',
      1629: 'Connection timed out; the timeout value is 60 seconds',
      1630: 'URL format is incorrect',
      1631: 'Connection failed',
      1632: 'The certificate has expired',
      1633: 'The certificate is self-signed',
      1634: 'A certificate verification error occurred',
      1635: 'Connection is unencrypted',

      # These errors are returned by the web publishing engine or the REST API.
      1700: 'Resource doesn’t exist',
      1701: 'Host is currently unable to receive requests',
      1702: 'Authentication information wasn’t provided in the correct '
            'format; verify the value of the Authorization header',
      1703: 'Invalid username or password, or JSON Web Token',
      1704: 'Resource doesn’t support the specified HTTP verb',
      1705: 'Required HTTP header wasn’t specified',
      1706: 'Parameter isn’t supported',
      1707: 'Required parameter wasn’t specified in the request',
      1708: 'Parameter value is invalid',
      1709: 'Operation is invalid for the resource’s current status',
      1710: 'JSON input isn’t syntactically valid',
      1711: 'Host’s license has expired',
      1712: 'Private key file already exists; remove it and run the command '
            'again',
      1713: 'The API request is not supported for this operating system',
      1714: 'External group name is invalid',
      1715: 'External server account sign-in is not enabled',
    }

    __slots__ = "code", "text"

    # code: error code, int.
    # text: error text, str or None.

    def __init__(self, code, text=None):
        self.code = code
        self.text = text

    def __str__(self):
        r = self.text
        if not r:
            code = self.code
            try:
                text = self.TEXT[code]
            except KeyError:
                r = "Unknown FileMaker error, code %d." % code
            else:
                r = "FileMaker error %d: %s." % (code, text)
        return r

    # Trying to access any attribute except real ones raises the exception.
    def __getattr__(self, name):
        try:
            r = super().__getattr__(name)
        except AttributeError:
            raise self
        return r

    # The '__getattr__' above not work for iterators; add explicit.
    def __iter__(self):
        raise self

# ===========================================================================
# A source of column specifications (layout or portal specification).

class ColSpecSrc:

    def colSpec(self, *names):
        "Get a field specifications."
        # -> names: field names, (str+).
        # <- field specifications, single or list.
        if len(names) == 1:
            r = self._colSpec(names[0])
        else:
            r = self._colSpecs(names)
        return r

    # ------------------------------------------------------------------------

    # _colSpec (subclass)

    def _colSpecs(self, names):
        "Get a list of field specifications."
        # -> names: field names, (str+).
        # <- field specifications, [ColSpec].
        return [self._colSpec(name) for name in names]

    def _valsByColNames(self, item, names):
        "Get field values by field names."
        # -> item: record or portal row, Rec or Row.
        # -> names: field names, (str+).
        # <- field values, single or list.
        return self._valsByColSpecs(item, self._colSpecs(names))

    # _valsByColSpecs (subclass)

# ----------------------------------------------------------------------------
# Layout specification.

class LaySpec(ColSpecSrc):

    __slots__ = "fnam", "lnam", "tnam", "dpic", "ipic", "mpic", "_cols", \
            "_rels"

    # fnam: file name, Name.
    # lnam: layout name, Name.
    # tnam: table name, Name (may be empty).
    # dpic: date format, str.
    # ipic: time format, str.
    # mpic: timestamp format, str.
    # _cols: field specifications by name, {Name:ColSpec}.
    # _rels: portal specifications by name, {Name:RelSpec}.

    def __init__(self, fnam, lnam, dpic, ipic, tnam="", mpic=None):
        # -> fnam: file name, str.
        # -> lnam: layout name, str.
        # -> dpic: date format, str.
        # -> ipic: time format, str.
        # -> tnam: table name, str.
        # -> mpic: timestamp format, str or None.
        self.fnam = Name(fnam)
        self.lnam = Name(lnam)
        self.dpic = dpic
        self.ipic = ipic
        self.tnam = Name(tnam)
        if mpic is None:
            mpic = dpic + " " + ipic
        self.mpic = mpic
        self._cols = {}
        self._rels = {}

    # ------------------------------------------------------------------------

    def relSpec(self, name):
        "Get a portal specification."
        # -> name: portal table name, str.
        # <- portal specification, RelSpecOld.
        return self._rels[Name(name)]

    # ------------------------------------------------------------------------

    def _colSpec(self, name):
        "Get a single field specification."
        # -> name: field name, str.
        # <- field specification, ColSpec.
        return self._cols[Name(name)]

    def _rel(self, rec, name):
        "Get a portal."
        # -> rec: record, Rec.
        # -> name: portal table name, str.
        # <- portal, Rel.
        return self._rels[Name(name)]._rel(rec)

    def _valsByColSpecs(self, rec, specs):
        "Get field values by field specifications."
        # -> rec: record, Rec.
        # -> names: field names, (str+).
        # <- field values, single or list.
        if len(specs) == 1:
            r = specs[0].recCol(rec)
        else:
            r = [spec.recCol(rec) for spec in specs]
        return r

# ----------------------------------------------------------------------------
# Layout specification, old XML format.

class LaySpecXapiOld(LaySpec):

    # XPath to extract the layout description.
    _XpMelt = ApiXml.Xp("/F:FMPXMLRESULT/F:METADATA")

    # ------------------------------------------------------------------------

    __slots__ = "_mblk", "_clst"

    # _mblk: size of the record group in map, int.
    # _clst: list of field specifications in internal order.

    # _cols: LaySpec.
    # _rels: LaySpec.

    def __init__(self, data, layDesc=None):
        # -> data: data, XML, layout or found set.
        # -> layDesc: layout description, LayDesc.
        delt, = self._XpDelt(data)
        super().__init__(delt.get("NAME"      ),
                         delt.get("LAYOUT"    ),
                         delt.get("DATEFORMAT"),
                         delt.get("TIMEFORMAT"))
        self._mblk = 1
        if layDesc:
            for rnam in layDesc.relNames():
                self._rels[rnam] = RelSpecOld(self, rnam)
        for felt in self._XpFelt(data):
            cnam = ColName(felt.get("NAME"))
            if layDesc:
                rnam = layDesc.relName(cnam)
                reps = layDesc.colReps(cnam)
            else:
                rnam = None
                reps = None
            if rnam is None: # not set, as opposed to empty string (layout).
                rnam = cnam.tbl
            if not reps:
                reps = int(felt.get("MAXREPEAT"))
            if rnam:
                try:
                    relSpec = self._rels[rnam]
                except KeyError:
                    relSpec = RelSpecOld(self, rnam)
                    self._rels[rnam] = relSpec
            else:
                relSpec = None
            tstr = felt.get("TYPE")
            colSpec = ColSpecOld(cnam, tstr, reps, relSpec, self._mblk)
            self._cols[cnam] = colSpec
            self._mblk += 1
        self._clst = list(self._cols.values())

    _XpDelt = ApiXml.Xp("/F:FMPXMLRESULT/F:DATABASE")
    _XpFelt = ApiXml.Xp("/F:FMPXMLRESULT/F:METADATA/F:FIELD")

    # ------------------------------------------------------------------------

    def recset(self, data):
        "Read a set of records."
        # -> data: XML backend object (lxml), checked for errors.
        # <- set of records, Recset.
        delt, = self._XpDelt(data)
        total = int(delt.get("RECORDS"))
        selt, = self._XpSelt(data)
        found = int(selt.get("FOUND"))
        relts = self._XpRelt(selt)
        count = len(relts)
        clist = self._clst
        v = self._XpVals(selt)
        m = [0] * (count * self._mblk + 1)
        vi = 0
        mi = 1
        exp = None # exported or served; None = unknown.
        for relt in relts:
            v[vi] = int(v[vi]); vi += 1 # modid
            v[vi] = int(v[vi]); vi += 1 # recid
            m[mi] = vi; mi += 1
            celts = self._XpCelt(relt)
            ci = 0
            for celt in celts:
                cn = self._XpClen(celt)
                cs = 1
                if cn:
                    # Non-empty column; convert.
                    vn = vi + cn
                    vt = clist[ci].type
                    while vi < vn:
                        v[vi] = vt(v[vi].text); vi += 1
                elif exp is not True:
                    # Empty column and not exported or unknown. It may happen
                    # that this 'COL' represents all fields in this portal.
                    # See how many columns are defined for the portal.
                    cr = clist[ci].relSpec._ccnt
                    if cr != 1:
                        # Multiple columns; can tell if exported or not.
                        if exp is None:
                            exp = (len(celts) == len(clist))
                        if not exp:
                            # This 'COL' represents all portal columns.
                            cs = cr
                cn = ci + cs
                while ci < cn:
                    m[mi] = vi; mi += 1; ci += 1
        return Recset(self, total, found, count, m, v)

    _XpEstr = ApiXml.Xp("/F:FMPXMLRESULT/F:ERRORCODE/text()")
    _XpSelt = ApiXml.Xp("/F:FMPXMLRESULT/F:RESULTSET")
    _XpRelt = ApiXml.Xp("F:ROW")
    _XpCelt = ApiXml.Xp("F:COL")
    _XpClen = ApiXml.Xp("count(F:DATA)")
    _XpVals = ApiXml.Xp("F:ROW/@MODID"
                      " | F:ROW/@RECORDID"
                      " | F:ROW/F:COL/F:DATA")

    def _item(self, recset, pos):
        "Get a record."
        # -> recset: set of records, Recset.
        # -> pos: record position, int, count from 0.
        # <- record, Rec.
        ms, vs = recset._data
        mi = pos * self._mblk
        return Rec(self, ms, vs, mi)

    def _recid(self, rec):
        "Get the internal record ID."
        # -> rec: record, Rec.
        # <- internal record ID, int.
        ms, vs, mi = rec.data
        return vs[ms[mi] + 1]

    def _modid(self, rec):
        "Get the internal record version."
        # -> rec: record, Rec.
        # <- internal record version, int.
        ms, vs, mi = rec.data
        return vs[ms[mi]]

# ----------------------------------------------------------------------------
# Layout specification, new format.

class LaySpecXapiNew(LaySpec):

    # _mblk: size of the record group in map, int.
    # _conv: conversion classes, [int/Val].
    # _vblk: size of the record value group, in.
    # _rlst: list of portal specifications, [RelSpecNew].

    def __init__(self, data, layDesc=None):
        delt, = self._XpDelt(data)
        super().__init__(delt.get("database"        ),
                         delt.get("layout"          ),
                         delt.get("date-format"     ),
                         delt.get("time-format"     ),
                         delt.get("table"           ),
                         delt.get("timestamp-format"))
        self._mblk = 1
        self._conv = []
        self._addConv(int, 2)
        self._vblk = 2
        melt, = self._XpMelt(data)
        for felt in self._XpFdef(melt):
            colSpec = self._addFelt(felt, layDesc, None, self._vblk)
            self._vblk += colSpec.reps
        for relt in self._XpRdef(melt):
            rnam = Name(relt.get("table"))
            relSpec = RelSpecNew(self, rnam, self._mblk)
            self._rels[rnam] = relSpec
            self._mblk += 1
            self._addConv(int, 2)
            for felt in self._XpFdef(relt):
                colSpec = self._addFelt(felt, layDesc, relSpec, relSpec._vblk)
                relSpec._vblk += colSpec.reps
        self._rlst = tuple(self._rels.values())

    _XpDelt = ApiXml.Xp("/f:fmresultset/f:datasource")
    _XpMelt = ApiXml.Xp("/f:fmresultset/f:metadata")
    _XpFdef = ApiXml.Xp("f:field-definition")
    _XpRdef = ApiXml.Xp("f:relatedset-definition")

    def _addConv(self, type, cnt):
        "Add a conversion function."
        # -> type: class, int or Val subclass (Text, etc.).
        # -> cnt: number of cells to convert, int.
        self._conv.extend([type] * cnt)

    def _addFelt(self, felt, layDesc, relSpec, voff):
        "Add a field specification."
        # -> felt: field definition, backend XML (lxml).
        # -> layDesc: layout description, LayDesc or None.
        # -> relSpec: portal specification, RelSpecNew or None.
        # -> voff: portal block offset, int.
        # <- field specification, ColSpecNew
        cnam = Name(felt.get("name"))
        tstr = felt.get("result")
        if layDesc:
            reps = layDesc.colReps(cnam)
        else:
            reps = None
        if not reps:
            reps = int(felt.get("max-repeat"))
        colSpec = ColSpecNew(cnam, tstr, reps, relSpec, voff)
        self._cols[cnam] = colSpec
        self._addConv(colSpec.type, colSpec.reps)
        return colSpec

    # ------------------------------------------------------------------------

    _XpEstr = ApiXml.Xp("/f:fmresultset/f:error/@code")

    def recset(self, data):
        "Read a set of records."
        # -> data: XML backend object (lxml), checked for errors.
        # <- set of records, Recset.
        srcElem, = self._XpSrc(data)
        total = int(srcElem.get("total-count"))
        resElem, = self._XpRes(data)
        found = int(resElem.get("count"))
        recElems = self._XpRec(resElem)
        count = len(recElems)
        vs = self._XpVal(resElem)
        vi = 0
        ms = [0] * (count * self._mblk + 1)
        mi = 1
        co = self._conv
        relSpecs = self._rlst
        rn = len(relSpecs)
        # Loop over records.
        for recElem in recElems:
            # Convert record metadata and fields.
            vs[vi] = int(vs[vi]); vi += 1 # modid
            vs[vi] = int(vs[vi]); vi += 1 # recid
            ci = 2
            cn = self._vblk
            while ci < cn:
                vs[vi] = co[ci](vs[vi].text)
                vi += 1
                ci += 1
            ms[mi] = vi
            mi += 1
            relElems = self._XpRel(recElem)
            ri = 0
            while ri < rn:
                relElem = relElems[ri]
                relSpec = relSpecs[ri]
                rci = cn
                cn += relSpec._vblk
                for rowElem in self._XpRec(relElem):
                    vs[vi] = int(vs[vi]); vi += 1 # modid
                    vs[vi] = int(vs[vi]); vi += 1 # recid
                    ci = rci + 2
                    while ci < cn:
                        vs[vi] = co[ci](vs[vi].text)
                        vi += 1
                        ci += 1
                ms[mi] = vi
                mi += 1
                ri += 1
        return Recset(self, total, found, count, ms, vs)

    _XpSrc = ApiXml.Xp("/f:fmresultset/f:datasource")
    _XpRes = ApiXml.Xp("/f:fmresultset/f:resultset")
    _XpVal = ApiXml.Xp("f:record/@mod-id"
                      "| f:record/@record-id"
                      "| f:record/f:field/f:data"
                      "| f:record/f:relatedset/f:record/@mod-id"
                      "| f:record/f:relatedset/f:record/@record-id"
                      "| f:record/f:relatedset/f:record/f:field/f:data")
    _XpRec = ApiXml.Xp("f:record")
    _XpRel = ApiXml.Xp("f:relatedset")


    def _item(self, recset, pos):
        "Get a record."
        # -> recset: set of records, Recset.
        # -> pos: record position, int, count from 0.
        # <- record, rec.
        ms, vs = recset._data
        mi = pos * self._mblk
        return Rec(self, ms, mi, vs, ms[mi])

    def _modid(self, rec):
        "Get the internal record version."
        # -> row: portal row, Row.
        # <- internal record version, int.
        ms, mi, vs, vi = rec.data
        return vs[vi]

    def _recid(self, rec):
        "Get the internal record ID."
        # -> row: portal row, Row.
        # <- internal record ID, int.
        ms, mi, vs, vi = rec.data
        return vs[vi + 1]

# ----------------------------------------------------------------------------
# Portal specification.

class RelSpec(ColSpecSrc):

    __slots__ = "laySpec", "name"

    # laySpec: layout specification, LaySpec.
    # name: portal table name, Name.

    def __init__(self, laySpec, name):
        self.laySpec = laySpec
        self.name = Name(name)

    def _colSpec(self, name):
        "Get a single field specification."
        # -> name: field name, str.
        # <- field specification, ColSpec.
        name = ColName(name, self.name)
        spec = self.laySpec.colSpec(name)
        if spec.relSpec is not self:
            # The field is in another portal.
            raise ErrRelSpecCol(self, name)
        return spec

    def _valsByColSpecs(self, row, specs):
        "Get field values by field specifications."
        # -> row: portal row, Row.
        # -> names: field names, (str+).
        # <- field values, single or list.
        if len(specs) == 1:
            r = specs[0].rowCol(row)
        else:
            r = [spec.rowCol(row) for spec in specs]
        return r

# ----------------------------------------------------------------------------

class ErrRelSpecCol(Exception):
    def __str__(self):
        relSpec, colName = self.args
        return "File '%s', layout '%s', portal to '%s': field '%s' is not " \
                "in the portal." % (relSpec.laySpec.fnam,
                relSpec.laySpec.lnam, relSpec.name, colName)

# ----------------------------------------------------------------------------
# Portal specification for the old format.

class RelSpecOld(RelSpec):

    __slots__ = "col", "_ccnt"

    # col: sample column, ColSpecOld.
    # _ccnt: number of fields in the portal.
    
    def __init__(self, laySpec, name):
        super().__init__(laySpec, name)
        self.col = None
        self._ccnt = 0

    def addColSpec(self, colSpec):
        "Add a field specification."
        # -> colSpec: field specification, ColSpec.
        # <- self.
        if not self.col:
            self.col = colSpec
        self._ccnt += 1

    def _rel(self, rec):
        "Make a portal."
        # -> rec: record, Rec.
        # <- portal, Rel.
        ms, vs, mi = rec.data
        if self.col:
            rc = self.col.rc(ms, mi)
        else:
            rc = 0
        return Rel(self, rc, ms, vs, mi)

    def _item(self, rel, pos):
        "Make a portal row."
        # -> rel: portal, Rel.
        # -> pos: row position, int, count from 0.
        # <- portal row, Row.
        ms, vs, mi = rel._data
        return Row(self, ms, vs, mi, pos)

    def _recid(self, row):
        "Get the internal record ID."
        # -> row: portal row, Row.
        # <- internal record ID, int (always error).
        raise ErrRelSpecOldMeta()

    def _modid(self, row):
        "Get the internal record version."
        # -> row: portal row, Row.
        # <- internal record version, int (always error).
        raise ErrRelSpecOldMeta()

# ----------------------------------------------------------------------------

class ErrRelSpecOldMeta(Exception):
    def __str__(self):
        return "The old XML format does not provide 'recid' and 'modid' " \
                "data for portal rows."

# ----------------------------------------------------------------------------
# Portal specification, new format.

class RelSpecNew(RelSpec):

    __slots__ = "_moff", "_vblk"

    # _moff: offset in the record group, int.
    # _vblk: portal group size, int.

    def __init__(self, laySpec, name, moff):
        # -> laySpec: layout specification, LaySpecNew.
        # -> name: portal table name, Name.
        # -> moff: offset in the record group, int.
        super().__init__(laySpec, name)
        self._moff = moff
        self._vblk = 2 # 2 cells of metadata.

    def _rel(self, rec):
        "Make a portal."
        # -> rec: record, Rec.
        # <- portal, Rel.
        ms, mi, vs, vi = rec.data
        mr = mi + self._moff
        rc = (ms[mr + 1] - ms[mr]) // self._vblk
        return Rel(self, rc, vs, ms[mr])

    def _item(self, rel, pos):
        "Make a portal row."
        # -> rel: portal, Rel.
        # -> pos: row position, int, count from 0.
        # <- portal row, Row.
        vs, vi = rel._data
        return Row(self, vs, vi + self._vblk * pos)

    def _recid(self, row):
        "Get the internal record ID."
        # -> row: portal row, Row.
        # <- internal record ID, int.
        vs, vi = row.data
        return vs[vi + 1]

    def _modid(self, row):
        "Get the internal record version."
        # -> row: portal row, Row.
        # <- internal record version, int.
        vs, vi = row.data
        return vs[vi]

# ============================================================================
# A column specification, abstract.

class ColSpec:

    Types = {
        "text"      : Text     ,
        "number"    : Number   ,
        "date"      : Date     ,
        "time"      : Time     ,
        "timestamp" : Timestamp,
        "container" : Container,
    }

    __slots__ = "name", "type", "reps", "relSpec"

    # name: field name, ColName.
    # type: field type, Val subtype.
    # reps: number of repetitions, int.
    # relSpec: portal specification, RelSpec or None.

    def __init__(self, name, tstr, reps, relSpec):
        self.name = Name(name)
        self.type = self.Types[tstr]
        self.reps = reps
        self.relSpec = relSpec

    def col(self, vs, vi):
        "Get a value of a field."
        # -> vs: values, [Val].
        # -> vi: index of the first cell, int.
        # <- value, Val or [Val].
        vn = self.reps
        if vn == 1:
            r = vs[vi]
        else:
            r = vs[vi : vi + vn]
        return r

# ----------------------------------------------------------------------------
# A column specification for use with the old format.

class ColSpecOld(ColSpec):

    __slots__ = "moff"

    # moff: offset in the record group.

    def __init__(self, name, tstr, reps, relSpec, moff):
        # -> name, tstr, reps, relSpec: common, see ColSpec.
        # -> moff: offset in the record group.
        super().__init__(name, tstr.lower(), reps, relSpec)
        if relSpec:
            relSpec.addColSpec(self)
        self.moff = moff

    def recCol(self, rec):
        "Get a value of a field in a record."
        # -> ms: value map, [int].
        # -> vs: values, [Val].
        # -> mi: start of the record group in 'ms', int.
        # <- value, Val or [Val].
        ms, vs, mi = rec.data
        return self.col(vs, ms[mi + self.moff])

    def rowCol(self, row):
        "Get a value of a field in a portal row."
        # -> ms: value map, [int].
        # -> vs: values, [Val].
        # -> mi: start of the record group in 'ms', int.
        # -> ri: portal row index, int, count from 0.
        # <- value, Val or [Val].
        ms, vs, mi, ri = row.data
        return self.col(vs, ms[mi + self.moff] + self.reps * ri)

    def rc(self, ms, mi):
        "Count rows in this column’s portal."
        # -> rec: record, Rec.
        # <- number of rows, int.
        ma = mi + self.moff
        return (ms[ma + 1] - ms[ma]) // self.reps

# ----------------------------------------------------------------------------
# A column specification for use with the new format.

class ColSpecNew(ColSpec):

    __slots__ = "voff"

    # voff: offset in the portal group.

    def __init__(self, name, tstr, reps, relSpec, voff):
        # -> name, tstr, reps, relSpec: common, see ColSpec.
        # -> voff: offset in the portal group.
        super().__init__(name, tstr, reps, relSpec)
        self.voff = voff

    def recCol(self, rec):
        "Get a value of a field in a record."
        # -> rec: record, Rec.
        # <- single field value, Val or [Val].
        ms, mi, vs, vi = rec.data
        if self.relSpec:
            # The field is in a portal; find the start of the portal.
            vi = ms[mi + self.relSpec._moff]
        return self.col(vs, vi + self.voff)

    def rowCol(self, row):
        "Get a value of a field in a portal row."
        # -> row: portal row, Row.
        # <- single field value, Val or [Val].
        vs, vi = row.data
        return self.col(vs, vi + self.voff)

# ============================================================================
# A found set of records or a portal.

class Recsetlike:

    __slots__ = "spec", "count", "_data"

    # spec: specification, LaySpec or RelSpec.
    # count: total number of delivered records, int.
    # _data: data, format-specific.

    def __init__(self, spec, count, *data):
        # -> spec: specification, LaySpec or RelSpec.
        # -> count: total number of delivered records, int.
        # -> data: data, format-specific.
        self.spec = spec
        self.count = count
        self._data = data

    def item(self, pos=0):
        "Get an item at this position."
        # -> pos: item index, int, count from 0.
        # <- item, Rec or Row.
        if pos < 0:
            pos = self.count + pos
        if pos < 0 or pos >= self.count:
            raise IndexError(pos)
        return self.spec._item(self, pos)

    def __len__(self):
        # <- number of items, int.
        return self.count

    def __getitem__(self, pos):
        # <- item, Rec or Row.
        return self.item(pos)

    def __iter__(self):
        # <- iterator over items.
        i = 0
        while i < self.count:
            yield self.item(i)
            i += 1

    def __reversed__(self):
        # <- iterator over rows in reversed order.
        i = self.count
        while i:
            i -= 1
            yield self.item(i)

# ----------------------------------------------------------------------------
# A set of records.

class Recset(Recsetlike):

    __slots__ = "total", "found"

    # total: total number of records in the layout table, int.
    # found: total number of found records, int.

    def __init__(self, laySpec, total, found, count, *data):
        # laySpec: layout specification, LaySpec.
        # total: total number of records in the layout table, int.
        # found: total number of found records, int.
        # count: total number of delivered records, int.
        # _data: data specific to the format.
        super().__init__(laySpec, count, *data)
        self.total = total
        self.found = found

# ----------------------------------------------------------------------------
# A portal.

class Rel(Recsetlike):

    pass

# ============================================================================
# A record or a portal row.

class Reclike:

    __slots__ = "spec", "data"

    # spec: layout specification, LaySpec.
    # data: record data, format-specific.

    def __init__(self, laySpec, *data):
        self.spec = laySpec
        self.data = data

    def recid(self):
        "Get the internal record ID."
        # <- internal record ID, int.
        return self.spec._recid(self)

    def modid(self):
        "Get the internal record version."
        # <- internal record version, int.
        return self.spec._modid(self)

    def col(self, *names):
        "Get values of the the specified fields."
        # -> names: field names, str+.
        # <- field values, single or list.
        return self.spec._valsByColNames(self, names)

# ----------------------------------------------------------------------------
# A record.

class Rec(Reclike):

    def rel(self, name):
        "Get the specified portal."
        # -> name: portal table name, str.
        # <- portal, Rel.
        return self.spec._rel(self, name)

# ----------------------------------------------------------------------------
# A portal row.

class Row(Reclike):

    pass

# ============================================================================
# A selector is an object to preselect and reuse a set of field specifications
# to read field data.

class Sel:

    __slots__ = "names", "_spec", "_cols"

    # names: field names, str+.
    # _spec: source specification, LaySpec or RelSpec, initially None.
    # _cols: field specifications, [ColSpec], initially None.

    def __init__(self, *names):
        # -> names: field names, str+.
        self.names = names
        self._spec = None
        self._cols = None

    def __call__(self, src):
        # -> src: data source, Rec or Row.
        # <- field values, single or list.
        spec = src.spec
        if not self._spec or self._spec is not spec:
            self._cols = spec._colSpecs(self.names)
            self._spec = spec
        return spec._valsByColSpecs(src, self._cols)

# ============================================================================
# Sep is a separator used in lists of layouts and scripts.

class Sep:
    "A separator for lists of layouts and scripts."
    pass

# ============================================================================
# A record that stores the user name and the password. A starting point for an
# authentification.

class User:
    "FileMaker user name and password."

    __slots__ = "name", "auth"

    # name: user name, str.
    # auth: the value for the 'authorization' header, str.

    def __init__(self, username, password):
        self.name = username
        t = Encode(username + ":" + password, "utf8")
        t = Base64Encode(t)
        t = Decode(t, "ascii")
        self.auth = "basic " + t

# ============================================================================
# The module may be given some initial data through environment variables:

PGFM_USR = OsGetenv("PGFM_USR") # username
PGFM_PWD = OsGetenv("PGFM_PWD") # password
PGFM_URL = OsGetenv("PGFM_URL") # server URL
PGFM_DB  = OsGetenv("PGFM_DB")  # database

if PGFM_USR and PGFM_PWD:
    defaultUser = User(PGFM_USR, PGFM_PWD)
else:
    defaultUser = None

if PGFM_URL:
    defaultSrv = Srv(PGFM_URL)
else:
    defaultSrv = None

if PGFM_DB:
    defaultDbName = Name(PGFM_DB)
else:
    defaultDbName = None

# ============================================================================
