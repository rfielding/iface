iface
=====

Generate FSM, Sequence Diagram, and a set of header files from a short interface description

When dealing with writing code, little attention is currently paid to the fact that each
API has state, where each function in that API has preconditions that restrict the allowable
calling order for the methods in that API.  Having such well defined ordering gives us
what is called a Protocol.  

When this ordering is exactly defined such that the compiler
can reject all unforeseen uses, the API has a new layer of _defense_, by denying the attacker
a space of _undefined states_ for it.  This is very similar to the concept of _LANGSEC_,
where input must be recognized as being in the language of the API before it will be parsed.
In this view, the correct message ingest of actors must be _decideable_.  APIs are treated
similar to Communicating Sequential Processes (CSP).  Each instance of an API has state,
and they exchange messages through their input message queue. 

The basic rule is to never invoke any function until the preconditions for the invoke are met.
That means that not only are the input types satisfied, but that preconditions take
input values into account and the current state of the API.  In this view, the states in
the state machine really represent the preconditions that must be true, in combination
with expected interactions with other APIs.

Because of this, the API is modeled as message passing state machines.  Every transition
in the state machine either ingests an input message (transforming from its precondition
to its postcondition), or emits an output message (transforming from its precondition
to its postcondition).  In this way, we capture all externally observable state changes
in a state machine.  This is enough information to automatically generate:

* The header files for each module (Java-like interfaces for this POC)
* The overall communicating state machines
* Include required traces _in the interface definitions_ themselves
* Proxy the modules so that all pre and post condition checks can be moved into
  the proxy and completely out of the implementation
* Proxy the modules so that evan blank stubs can pass behavioral unit tests
* Proxy the modules so that logging can go there (logging all message passing and state
  transitions) rather than in the implementation code
* The full dependency diagram between components.  What we import is just as
  important as what we export.

We assume that if a function is _ever_ invoked before its preconditions are met, 
that it crashes after exposing a horrible security _vulnerability_.
The postconditions and explicitly handling message sending (rather than only noting
what an API will accept) are the parts that are usually missing from interface definitions.
Without them, we have to stop being explicit at defining callable functions; and
get into drawing ambiguous diagrams that are not machine checkable.


Approximations
==============

* Only given a set of C header files with weak types, we can impose interfaces between modules.
But the interfaces end up being extremely ambiguous.  

* In Object Oriented programming without DesignByContract we get partially supported Protocols
because the type systems enforce some of the preconditions for every function.  Using strong
types alone, we can come close to imposing a regular expression grammar over the allowable
sequence of calls to an API.  But we still can't reach the ideal of disallowing the call
of a function with unmet preconditions.

* With DesignByContract, we get quite a bit closer because we can ensure that no function
with unmet preconditions gets invoked, while also implying what the next state needs to be.
Without the postconditions, we can't define the state machines.  Without state machines,
we can't check the sequence diagrams.

* With Typestate (the approach taken here), the preconditions are implicitly hidden in the
state machines.  Each distinct state is not a configuration of all variables in the API,
but are externally distinguishable pre and post condition combinations. 

* DependentTypes are the ideal, where the type system itself is strong enough to specify
pre and post conditions exactly.  With dependent types, the type depends on the value of
the object.  This is the fullest power available, such that code can be proven logically
consistent.  No attempt to use dependent types is made.  But note that DesignByContract
provides a weak form of it that has many of the same advantages.

