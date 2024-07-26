``pgfm``: a Python client for FileMaker Server Web APIs
============================================================

:version: ``pgfm`` 0.7.3, July 25, 2023.
:contact: Mikhail Edoshin

The |pgfm| module is a Python client for |FileMaker|_ Server Web APIs. It aims to support all FileMaker APIs in a unified and transparent manner.

.. warning:: This is a work in progress. The current version supports the XML 
   API, both old and new formats. It does not yet fully support container 
   fields, and layout information in ``FMPXMLLAYOUT`` format and the whole 
   Data API. Another thing in progress are user and developer documentation.

Sample usage
------------

A FileMaker server at ``http://fm.example.com`` hosts a file **Sample** with toy orders:

.. figure:: https://github.com/MikhailEdoshin/pgfm/raw/main/res/figure-1.png
   :scale: 75

   The schema of the **Sample** file and a layout to fetch data.

We need to write backend code that receives a customer ID, requests all orders of that customer from FileMaker along with their most recent event, and returns them back to the caller as a JSON object with the following structure::

  { type: "customerOrders" customerId
    orders: [
      { orderId statusTime statusName
        items: [
          { productId productName price quantity } ] } ] }

To support that a FileMaker developer added a layout **Web.Orders**. The layout does a good half of the work to shape the result: it defines the fields that will be returned and arranges things so that the fields from the **Event** table show the most recent event. 

To use the layout the backend needs send a search request to this layout, get back the result, and process the data to rearrange them as required. With |Pgfm| the simplest way to achieve that would look so:

.. _snippet:

.. code:: Python

   import pgfm

   def customerOrders(customerId):
       # -> customerId: customer ID, int.
       # <- result, list, JSON-compatible.
       res = dict(type="customerOrders", customerId=customerId, orders=[])
       usr = pgfm.User("username", "********")
       srv = pgfm.Srv("https://fm.example.com/", usr)
       req = pgfm.ReqLaySel()                 \
               .db("Sample")                  \
               .lay("Web.Orders")             \
               .col("customerId", customerId) \
               .sort("Event::time", "descend")
       for rec in srv.send(req).read():
           order = dict(
               orderId    = rec.col("id"),
               statusTime = rec.col("Event::time").toPyDatetime().isoformat(),
               statusName = rec.col("Event::type"),
               items      = [])
           res.orders.append(order)
           for row in rec.rel("OrderItem"):
               order.items.append(dict(
                   productId   = row.col("productId"),
                   productName = row.col("Product::name"),
                   price       = row.col("Product::price"),
                   quantity    = row.col("quantity")))
       return res

The ``res`` is the resulting object. The ``usr`` is the account we use to send the request and ``srv`` is the FileMaker server. The ``req`` is a request: something like a form that describes the desired action. Here we are going to ask the server to search for records (``ReqLaySel``) and specify the necessary details: file, layout and search criteria.

We also specify we want to get the results sorted by the **Event::time** field. Although the layout is set up to show the last event, the sort command will sort the orders by their first event. In our case it is fine, but generally it is one of specific FileMaker things one has to intimately understand.

We send the request to the server and immediately read the response. The result is an iterable of records so we also immediately start iterating over them. If something goes wrong with an HTTP request or a FileMaker response the code will automatically raise an exception.

For each record we create a new ``dict`` (``order``) and fill it with data from the record’s fields. The module reads FileMaker field values as string-like objects that can be safely used in any string context. By default they will be formatted according to FileMaker rules: for example, a date would come out as ``M/D/Y``. They are not really strings though; they know their specific type and expose methods to correctly convert their values into other representations. In our case we want to format the timestamps according to ISO 8601, so we convert them first to a Python ``datetime`` and then format the result with ``isoformat()``.

We also add a list for order items. Then we get a portal to the **OrderItem** table, loop through its rows, for each row create another ``dict`` and immediately place it into the ``items`` list.

In the end we return the result. We used only ``list`` and ``dict`` instances and FileMaker values are strings, so the result can be safely serialized into JSON. 

License
-------

The module is available under the MIT license. The data used for the examples in the documentation are dervied from a sample database from |Contoso|_.

Usage
-----

The module uses third-party libraries ``lxml`` and ``requests``. The source code is available on GitHub_. The author, Mikhail Edoshin, can be reached there or via email: one_, another_.

.. _GitHub: https://github.com/MikhailEdoshin/pgfm/
.. _one: mikhail.edoshin@proofgeist.com
.. _another: mikhail.edoshin@mail.ru

Development
-----------

The project contains the following files::

  /
  |_ LICENSE          -- licence (MIT)
  |_ Makefile         -- Makefile; run 'make' to see help
  |_ README.rst       -- The 'README' file (this one)
  |_ pyproject.toml   -- Python package specification
  |_ requirements.txt -- Python requirements.
  |_ res\
  |  |_ figure-1.png  -- resources for 'README'
  |_ src\
  |  |_ pgfm.py       -- the module
  |_ tests\
     |_ test.py       -- tests


Use ``Makefile`` to set up the virtual environment for interactive use and tests.  The Python package is built with ``flit``.

.. References

.. |Contoso| replace:: one of Microsoft projects (licensed under MIT)
.. _Contoso: https://github.com/microsoft/Windows-appsample-customers-orders-d
             atabase

.. |FileMaker| replace:: FileMaker
.. _FileMaker: https://www.claris.com/filemaker/

.. |Pgfm| replace:: ``pgfm``

.. |Pip| replace:: ``pip``

