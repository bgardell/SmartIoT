# **Answer Set Programming Pythonic Web Service**

This clingo web service is designed to provide Answer Set Programming over the web for IoT and Mobile applications.

The service utilizes the clingo grounder / solver for logic programs, clingo5 python module and the cherrypy web
framework.


**Dependencies**

cherrpy
clingo python module

**Term Definition usage**

The term definition file terms.json should contain the variable names and types

with the exact same format displayed in the example terms.json file.

Any terms can be defined using the TermDefinition module in the future to generate this specific output.

All terms in #show aggregates should be defined in the terms.json file prior to use.

Setting the main logic program for rules and show aggregates

**Adding terms:**

Terms can be defined by POSTing a term definition object in the same format as is defined in the terms.json example.

1. ​ **Main logic program**

The service can use a default logic program, such as test.lp, defined in the server settings to have rules defined prior
to being setup in the service.

1. ​POSTing facts to the service

The service receives facts to be added to the main grounder/solver via an HTTP POST endpoint at /addFact.

Example usage can be found in the examples directory in the repo.

_testDataIn.txt –_ Data to be POSTED to the HTTP server.



**Grounding, Solving and Receiving output**

The web service has an HTTP GET endpoint at /getOptimumModel. This will take all facts POSTed to the server and ground
them alongside the default logic program setup in the server settings. All #show aggregates in the main logic program
should have their predicates and terms defined in the terms.json file.


