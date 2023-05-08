%module memory_system
%include <std_string.i>
%include <typemaps.i>

%{
#include <Python.h>
%}

%typemap(in) uint64_t {
    $1 = (uint64_t) PyInt_AsLong($input);
}


%typemap(in) std::function<void(uint64_t)> {
    // Check that the argument is a callable Python object
    if (!PyCallable_Check($input)) {
        PyErr_SetString(PyExc_TypeError, "Expected a callable object");
        return NULL;
    }

    // Define a lambda function that calls the Python function
    auto lambda = [pyfunc = PyObject_GetAttrString($input, "__call__")] (uint64_t arg) {
        PyObject_CallFunction(pyfunc, "K", arg);
    };

    $1 = lambda;
}



%{
    #define SWIG_FILE_WITH_INIT
    #include "../DRAMsim3/src/configuration.h"
    #include "../DRAMsim3/src/memory_system.h"

    

%}

%include "../DRAMsim3/src/memory_system.h"
