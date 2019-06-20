//
// This file is part of an OMNeT++/OMNEST simulation example.
//
// Copyright (C) 1992-2008 Andras Varga
//
// This file is distributed WITHOUT ANY WARRANTY. See the file
// `license' for details on this and other legal matters.
//


// The Aloha network consists of hosts which talk to the central "server" via
// the Aloha or Slotted Aloha protocol
// 

network Aloha
{
    parameters:
        // TODO Task 2.3.1: Add missing parameters 
        int numHosts;
        double txRate @unit(bps);
        double slotTime @unit(ms);
        double fullLoad;      
        // End of TODO
        @display("bgi=maps/germany,s;bgb=413,471");
    submodules:
        // TODO Task 2.3.1: Create submodules
		server: Server
		{
		 	txRate = txRate;
			slotTime = slotTime;   
		}
		host[numHosts]: Host
		{
			txRate = txRate;
			slotTime = slotTime;
			load = fullLoad/numHosts;
		}
        // End of TODO
}

