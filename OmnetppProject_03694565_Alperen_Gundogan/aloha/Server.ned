//
// This file is part of an OMNeT++/OMNEST simulation example.
//
// Copyright (C) 1992-2008 Andras Varga
//
// This file is distributed WITHOUT ANY WARRANTY. See the file
// `license' for details on this and other legal matters.
//


//
// The central computer in the ALOHAnet network.
//
simple Server
{
    parameters:
        @display("i=device/antennatower_l");
        
        @signal[receive](type="long");  // for successful receptions (non-collisions): 1 at the start of the reception, 0 at the end of the reception             
        @statistic[channelUtilization](source="timeavg(receive)"; record=last; interpolationmode=linear; title="channel utilization");
        
        double slotTime @unit(s);
        double txRate @unit(bps);         // transmission rate
        double radioDelay @unit(s);       // propagation delay of radio link
        volatile int ackLenBits @unit(b);  // packet length in bits
        
    gates:
        input in @directIn;
}

