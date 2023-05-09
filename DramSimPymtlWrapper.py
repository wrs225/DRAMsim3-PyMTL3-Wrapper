from pymtl3 import *

from .DRAMsimWrapper.memory_system import *

from pymtl3.stdlib import stream
from pymtl3.extra.pypy.fast_bytearray_funcs import (
    read_bytearray_bits,
    write_bytearray_bits,
)

def callback_read(i):
    pass

def callback_write(i):
    pass




class DramSimPymtlWrapper( Component ):

    
    #DRAM CLK is 1333MHz, let's say our system is 4000MHz
    def construct(s, RTL_CLK_PER = 3, INPUT_CONFIG = u'../DDR3_1Gb_x8_1333.ini', OUTPUT_CONFIG = u'./', mem_nwords = (1_000_000_000 // 8) // 8):
        
        s.istream= stream.ifcs.RecvIfcRTL( MemMsg )
        s.ostream = stream.ifcs.SendIfcRTL( MemMsg )

        # Define two queues with depth 1
        s.queue1 = stream.queues.NormalQueueRTL( MemMsg, 1)
        s.queue2 = stream.queues.NormalQueueRTL( MemMsg, 1)

        #assign queues to interface
        s.queue1.recv //= s.istream
        s.ostream //= s.queue2.send
        
        #Wires so I can divide the clock and see the status of DRAMsim3 stalling in simulation.
        #in_flight is needed to hold state. This module is a weird combo of hardware and software.
        s.in_flight = Wire( Bits1 )
        s.memsystem_rdy = Wire( Bits1 )
        s.rtl_clk_cycles = Wire( Bits32 ) 
        
        #Bytearray to hold values we store.
        s.mem = bytearray(mem_nwords * 8)
        
        #DRAMsim3 memory model object to get latency.
        s.drammodel = MemorySystem(INPUT_CONFIG,OUTPUT_CONFIG,callback_read,callback_write)

        #Combinational block
        @update
        def increment():
            

            s.queue2.recv.msg.w @= s.queue1.send.msg.w 
            s.queue2.recv.msg.addr @= s.queue1.send.msg.addr

            if s.in_flight:
                s.queue2.recv.val @= Bits1(1)
                s.queue1.send.rdy @= Bits1(1) 
            else:
                s.queue2.recv.val @= Bits1(0)
                s.queue1.send.rdy @= Bits1(0)
            
            #function call in combinational block is sus to me. 
            if s.queue1.send.msg.w and s.in_flight:
                s.queue2.recv.msg.msg @= s.queue1.send.msg.msg
                write_bytearray_bits(s.mem, s.queue1.send.msg.addr, 8, s.queue1.send.msg.msg)
            else:
                s.queue2.recv.msg.msg @= read_bytearray_bits(s.mem, s.queue1.send.msg.addr, 8)

            
        #Clocked block. DRAM clock division & adding transactions to DRAM model
        @update_ff
        def block():
            if(s.reset):
                s.rtl_clk_cycles <<= Bits32(0)
            else:
                if(s.rtl_clk_cycles == RTL_CLK_PER):
                    s.drammodel.ClockTick()
                    s.rtl_clk_cycles <<= Bits32(0)
                else:
                    s.rtl_clk_cycles <<= s.rtl_clk_cycles + Bits32(1)
                    
            s.memsystem_rdy <<= s.drammodel.WillAcceptTransaction(s.queue1.send.msg.addr * 64, bool(s.queue1.send.msg.w))
            if (not s.in_flight) and s.queue1.send.val and s.queue2.recv.rdy and s.drammodel.WillAcceptTransaction(s.queue1.send.msg.addr * 64, bool(s.queue1.send.msg.w)):
                s.in_flight <<= Bits1(1)
                s.drammodel.AddTransaction(s.queue1.send.msg.addr * 64, bool(s.queue1.send.msg.w))
            else:
                s.in_flight <<= Bits1(0)
            
            

                

                   
                    

                



        




@bitstruct
class MemMsg:
    w:    Bits1
    addr: Bits64
    msg:  Bits64



