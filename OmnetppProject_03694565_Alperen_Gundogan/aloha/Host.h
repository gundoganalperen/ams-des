//
// This file is part of an OMNeT++/OMNEST simulation example.
//
// Copyright (C) 1992-2008 Andras Varga
//
// This file is distributed WITHOUT ANY WARRANTY. See the file
// `license' for details on this and other legal matters.
//

#ifndef __ALOHA_HOST_H_
#define __ALOHA_HOST_H_

#include <omnetpp.h>
#include "AirFrame_m.h"

namespace aloha {

/**
 * Aloha host; see NED file for more info.
 */
class Host : public omnetpp::cSimpleModule
{
  private:
    bool enableStateStats = false;

    int hostId;
    // parameters
    omnetpp::simtime_t radioDelay;
    double txRate;
    //omnetpp::cPar *iaTime;
    double load;
    omnetpp::cPar *pkLenBits;

    omnetpp::simtime_t slotTime;

    // state variables, event pointers etc
    omnetpp::cModule *server;
    omnetpp::cMessage *endTxEvent;

    omnetpp::cMessage *newRequestTimer;

    typedef enum HostState {
        NEW_REQUEST=0,
        TRANSMIT=1,
        BACKLOGGED=2} HostState;

    HostState state;

    omnetpp::simsignal_t stateSignal;
    int pkCounter;

    AirFrame *pktInProgress;

    omnetpp::cMessage *retryTxTimer;
    int reTxCount;
    int maxReTx;
    int maxBackOff;


  public:
    Host();
    virtual ~Host();

  protected:
    /**
     * Initialization of the Host ned module
     */
    virtual void initialize();

    /**
     * Message reception callback
     */
    virtual void handleMessage(omnetpp::cMessage *msg);

    omnetpp::simtime_t getNextTransmissionTime();

    /**
     * Create a user packet
     */
    AirFrame * createPacket();

    /**
     * Get back-off time value
     */
    omnetpp::simtime_t getBackOffTime();

    /**
     * Check whether the received acknowledgement is correct
     */
    bool checkAck(omnetpp::cMessage * msg);

    /**
     * Change the state machine
     */
    void changeState(HostState newState);

    /**
     * Retrieve simulation parameters
     */
    void setSimParameters();
    void sendNewPacket();
    void retransmitPacket();
    void processAck(omnetpp::cMessage * msg);

  private:
    double getNextArrivalTime();

};

}; //namespace

#endif

