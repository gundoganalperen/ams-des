//
// This file is part of an OMNeT++/OMNEST simulation example.
//
// Copyright (C) 1992-2008 Andras Varga
//
// This file is distributed WITHOUT ANY WARRANTY. See the file
// `license' for details on this and other legal matters.
//

//
// A computer in the ALOHAnet network.
//

simple Host
{
    parameters:

        @signal[state](type="long");
        @statistic[radioState](source="state";title="Radio state";enum="IDLE=0, TRANSMIT=1";record=vector);
        
        double txRate @unit(bps);         // transmission rate
        double radioDelay @unit(s);       // propagation delay of radio link
        volatile int pkLenBits @unit(b);  // packet length in bits
          
        double load; 					  // inverse of iaTime, in pkts per slot
                
        double slotTime @unit(s);         // zero means no slots (pure Aloha)        
        double maxReTx;					  // max retransmission counter
        double maxBackOff;				  // max backoff counter
        @display("i=device/pc_s");
    gates:
        input in @directIn;
}

