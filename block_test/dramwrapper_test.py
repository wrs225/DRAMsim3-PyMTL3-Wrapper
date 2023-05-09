#=========================================================================
# dramwrapper_test
#=========================================================================

import pytest
import random

random.seed(0xdeadbeef)

from pymtl3 import *
from pymtl3.stdlib import stream
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from DRAMSimPYMTLWrapper.DramSimPymtlWrapper import *
from fxpmath import Fxp
import numpy as np
import math


#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------


class TestHarness( Component ):

  def construct(s, memmodel):

    # Instantiate models

    s.src      = stream.SourceRTL( MemMsg )
    s.sink     = stream.SinkRTL  ( MemMsg )
    s.memmodel = memmodel

    # Connect

    s.src.send         //= s.memmodel.istream
    s.memmodel.ostream //= s.sink.recv

  def done( s ):
    return s.src.done() and s.sink.done()


#----------------------------------------------------------------------
# Test Case Table
#----------------------------------------------------------------------

def simple():
  return [MemMsg(1,0,1), MemMsg(1,0,1),MemMsg(1,1,1), MemMsg(1,1,1),MemMsg(1,2,1), MemMsg(1,2,1),MemMsg(1,3,1), MemMsg(1,3,1)]

def random_writes():
  arr = []
  for i in range(100):
    randaddr = random.randint(0,10000000)
    transaction = MemMsg(1,randaddr,i)
    arr.append(transaction)
    arr.append(transaction)
  return arr

def read_write():
  return [MemMsg(1,0,1), MemMsg(1,0,1),MemMsg(0,0,0), MemMsg(0,0,1)]

def random_read_writes():
  addr_dict = {}
  arr = []
  randaddr = random.randint(0,1000000)
  transaction = MemMsg(1, randaddr, 0)
  arr.append(transaction)
  addr_dict[randaddr] = 0
  transaction = MemMsg(1, randaddr, 0)
  arr.append(transaction)

  for i in range(1,500):
    writeread = random.randint(0,1)
    if(writeread == 1):
      randaddr = random.randint(0,1000000)
      transaction = MemMsg(writeread, randaddr, i)
      arr.append(transaction)
      addr_dict[randaddr] = i
      transaction = MemMsg(writeread, randaddr, i)
      arr.append(transaction)
    else:
      randaddr = random.randint(0,len(addr_dict.keys())- 1)
      print(randaddr)
      transaction = MemMsg(writeread, list(addr_dict.keys())[randaddr], i)
      arr.append(transaction)
      transaction = MemMsg(writeread, list(addr_dict.keys())[randaddr], addr_dict[list(addr_dict.keys())[randaddr]])
      arr.append(transaction)
  return arr

    
    
  

test_case_table = mk_test_case_table([
  (                              "msgs                                       src_delay sink_delay"),
  [ "simple",                     simple,                                    0,        0          ],
  [ "random_write",               random_writes,                             0,        0          ],
  [ "read_write",                 read_write,                                0,        0          ],
  [ "random_read_writes",         random_read_writes,                        0,        0          ]

])

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( test_params, cmdline_opts ):


  th = TestHarness( DramSimPymtlWrapper() )

  msgs = test_params.msgs()

  th.set_param("top.src.construct",
    msgs=msgs[0::2],
    initial_delay=test_params.src_delay+3,
    interval_delay=test_params.src_delay )

  th.set_param("top.sink.construct",
    msgs=msgs[1::2],
    initial_delay=test_params.sink_delay+5,
    interval_delay=test_params.sink_delay )

  run_sim( th, cmdline_opts)

