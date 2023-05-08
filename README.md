# DRAMsim3-pyMTL3-Wrapper

Welcome to my DRAMsim3 pyMTL3 stream interface wrapper! This wrapper is based off of my DRAMsim3 python wrapper geneated in this repository:

```
https://github.com/wrs225/DRAMSim3-Python-Wrapper.git
```


To run tests please run the following commands
```
  mkdir build
  cd build
  pytest ../
```
Congratulations, the tests should have run. 

If you run the tests with line tracing using
```
  pytest ../ --dump-vcd
```
you will be able to clearly see variable cycle access latency using gtkwave or your favorite waveform generator.

Because pyMTL does not allow for multiple clock domains, and the DRAM may have a different clock speed as your designs, you will be required to /
add a division factor to the instantiation of the module. By default, my test uses a simple DDR3 stick with a clock speed of 1333MHz. Thus, I set the /
clock division constant to 4, so 4 simulation cycles equate to 1 DRAM clock cycle.


The module consists of an input queue, inner DRAMsim3 function calls, and an output queue. The queues are by default single element queues. /
The queues act as interfaces which stich together the DRAMsim3 library and pyMTL simulations. The memory request/response protocol is as follows:

```
  req = [ W | addr | payload ]
          1b  64b    64b
  if(W = 1)
    resp = [ 1 | addr | payload ]
  else
    resp = [ 0 | addr | data    ]
```

Have fun experimenting! This library should make it trivially easy to implement cycle-accurate DRAM into your designs. 
