# mishmash io

*mishmash io* is a distributed and scalable database that allows you to easily implement smart, predictive features in your app.

Find out more on [mishmash.io](https://mishmash.io)

# About this package

This is the *mishmash io* client library for Python. Use it to connect, store / fetch data and to submit your algorithms for distributed execution.

## Installing

### Using Mishmash io in Heroku with jwt authentication plugin please install

```bash
$ pip install mishmash-io-client["jwt"]
```

* Usage 

    To be able to work with mishmash client you need to provide the following configuration as environment variables or as json file :
    * for mishmash-io-auth-jwt plugin 
        * MISHMASHIO_SERVERS - list of mishmash servers endpoints
        * MISHMASHIO_APP_ID - id of the app using mishmash client
        * MISHMASHIO_AUTH_SERVER - the identity provider server endpoint
        * MISHMASHIO_AUTH_PRIVATE_KEY - Private key used for authentication with the identity provider
    * for mishmash-io-client
        * MISHMASHIO_AUTH_METHOD - must be set to "jwt"
        * MISHMASHIO_USE_SSL - True if you want to use ssl connection

### Using Mishmash in Azure cloud please install

```bash
$ pip install mishmash-io-client["azure"]
```

### Using Mishmash in Aws cloud please install

```bash
$ pip install mishmash-io-client["aws"]
```

### Using Mishmash in Google cloud please install

```bash
$ pip install mishmash-io-client["google"]
```


## Initializing the client

Import and create a new instance of Mishmash:

```python
from Mishmash import Mishmash
mishmash = Mishmash()
```

(make sure the lib can find its config)

The mishmash variable now holds the 'mishmash of all data' for the given application. Everything stored in **mishmash io** is now accessible through that variable.

## What is a mishmash of data?

A 'mishmash' is a special type of object that represents all or parts of the application data. It is, usually, a *container*, a *collection*, a *list* (a collection that has order) and a *set* (a collection where operators like 'union', 'intersection', etc can be applied).

A mishmash can also represent a single Number, bool, string or other type of value.

We call it a 'mishmash', because it just 'holds' data structures of arbitrary complexity - objects, lists, etc; types - mishmashes can 'hold' at the same time, for example - user profile objects and lists of their videos, posts, comments and so on. In other words - they 'hold' all the input that is needed for a particular application code to operate on. 

It's the responsibility of this application code to properly interpret each element and its meaning for the application; other objects in its context; and so on. With this in mind - mishmashes give the developer, an easy way, with little code - to describe input and apply complex logic on it.

## What a mishmash isn't

A 'mishmash' is not a table, has no rows, no columns, no cells. It has no specific data format, schema or structure on its own.

It is application variables, stored.

## Using mishmashes

A mishmash can be 'built' from literals, variables, code and other mishmashes. It can be assigned values and data; it can be deleted, updated, added to and deleted from. Code can be applied to mishmashes too.

Mishmash objects are basically descriptors of data and not the actual data. Operations (accessing, indexing, 'union', etc) applied on a mishmash usually return another mishmash (another descriptor), and do not transfer data. This is called 'building a mishmash' - building the descriptor for data that will be needed by some application code later.

Fetching data or results actually happens only when specifically requested (usually by the interpreter), for example - when a value is needed for a local computation, an iteration over the mishmash is requested in local code. These are often referred to as 'terminal operations' - building stops and transferring of data begins. More about terminal operations (and local vs remote code) below.

Mutating the data (for example - storing new data, deleting existing data, etc) is done through assignments, additions, etc to a mishmash that has been built.

## Building a mishmash

All mishmashes are built from existing mishmashes or from the 'all data mishmash' (shown at the begining). As any building operation on a mishmash always returns a new mishmash - you can build one in several steps, iteratively or directly.

Three major rules apply on all building operations on a given mishmash:
1. Naming (or indexing) makes a more specific mishmash, e.g. when 'naming' *videos* on the *user* mishmash, like in *user.videos* - the returned mishmash is more specific - 'holds' the *videos* now. Similarly, doing *user.videos[3]* is even more specific.
2. Enumerating (or listing) produces a broader mishmash - *user['video', 'music']* will return a mishmash of all music and videos. Enumerating is usually done by the commas (',') in your code.
3. "Code does" - applying code, by specifying a lambda, or a function or method - performs the action specified in the code on the mishmash that it is applied to. And it does that remotely - on the **mishmash io** cluster (see below for more about 'local code' and 'remote code')

These three rules can be mixed, combined and nested many times - *my_mishmash[(age: [18:], department: 'software development')][func_has_birthday](func_throw_party)*.

**Important:**
All three operations are done either as function call arguments - *my_mishmash(<operations>)* or as item access (a *bracket notation*) - *my_mishmash[<operations>]*. Naming can also be done by accessing a local attribute (a *dot notation*) on a mishmash: *my_mishmash.videos*.

### Naming and indexing

Just like accessing an attribute of an object by its name (or identifier) returns one of the specific values contained in that object, or accessing the element of a list located at a given index returns that one value among all others in the list - in the same way, 'naming' or 'indexing' a mishmash returns a mishmash that is describing a more specific subset of the initial data.

In Python, this is done by using:
- *dot notation* - like *my_mishmash.age*; 
- single *int, float, bool, None, etc* or other simple type - *my_mishmash[4]* or *my_mishmash(4)*; 
- *date, datetime* and similar;
- *str* or *unicode* - *my_mishmash['age']* or *my_mishmash('age')*;
- *bytes, bytearray, memoryview*

Or by using types that naturally contain names:
- *namedtuple*
- *mapping* objects, like *dict* - {'age': 42, 'department': 'software development'}, dict(age: 42, department: 'software development')
- function call arguments with names: *my_mishmash(age=42)*

And some of the sequence types that are often used as list indexes:
- *range*
- *slice*

Finally, objects of other complex classes:
- another mishmash
- user-defined classes (see below how these are treated)
- Python code - Callables - lambdas, functions, methods, generators, etc. (see below)

### Enumerating

A 'broader' mishmash - one that combines many 'deeper' mishmashes together into a whole, is created by enumerating multiple items. Or in other words - by supplying sequences or collections with no specific naming, mapping or other association between items.

Simplest ways to create broader mishmashes in Python are:
- multiple function call arguments - *my_mishmash('age', 'software development', my_other_mishmash)*
- *list* or *tuple* - *my_mishmash[('software development', 'quality assurance')]*
- *set* - *my_mishmash({'software_development', 'quality assurance'})*
- other, user-defined *iterable* classes (see below how user-defined classes are handled)

**Note:** Callable code - like generators for example - are not considered as 'enumerating' parameters, they're handled as code - transferred to the cluster and optimized. This is because executable code can be doing much more than just enumerating. For this reason, it's considered on its own. (See below)

### Adding code

Usually you do not want to download all the data you have 'selected' with mishmash object.
For that reason mishmash gives a way to process selected data on the server side and get only the end results from processing. 

If you have a built mishmash you can submit a function or callable code to the mishmash server which defines an operation
over selected data. That piece of code will be optimized and run in parallel on the mishmash server instead of running locally 

TODO add text for server side optimization 


### More ways to build a mishmash

Check out [mishmash.io](https://mishmash.io) for more recent version of this document.

#### Set operators

You can use bitwise set operators & and | over mishmash object

## Looping on a mishmash

Given that a mishmash variable always represents a mishmash of data (or a set) - 
looping on it should have the effect of 'pull those elements from the server and use them'.

## Mutating a mishmash

You can 'mutate' given mishmash - send local data or python code to the server
change or store and store them for future usage

## Computing with a mishmash

Check out [mishmash.io](https://mishmash.io) for more recent version of this document.

### Computing locally

Check out [mishmash.io](https://mishmash.io) for more recent version of this document.

### Computing remotely

Check out [mishmash.io](https://mishmash.io) for more recent version of this document.

## More 

Check out [mishmash.io](https://mishmash.io) for more recent version of this document.

### Custom classes

Check out [mishmash.io](https://mishmash.io) for more recent version of this document.

### Serializing a mishmash for storage or transfer

Check out [mishmash.io](https://mishmash.io) for more recent version of this document.
