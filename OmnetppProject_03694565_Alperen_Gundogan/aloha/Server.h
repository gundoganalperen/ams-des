//
// This file is part of an OMNeT++/OMNEST simulation example.
//
// Copyright (C) 1992-2008 Andras Varga
//
// This file is distributed WITHOUT ANY WARRANTY. See the file
// `license' for details on this and other legal matters.
//


#ifndef __ALOHA_SERVER_H_
#define __ALOHA_SERVER_H_

#include <omnetpp.h>

namespace aloha {

/**
 * Aloha server; see NED file for more info.
 */
class Server : public omnetpp::cSimpleModule
{
  private:
    // state variables, event pointers

    typedef enum ChannelState {
        BUSY,
        FREE,
    } ChannelState;

    ChannelState channelState;
    omnetpp::cMessage *endRxEvent;

    long currentCollisionNumFrames;
    long receiveCounter;

    omnetpp::simtime_t recvStartTime;
    enum {IDLE=0, TRANSMISSION=1, COLLISION=2};
    omnetpp::simsignal_t channelStateSignal;

    //packet waiting to be acknowledged
    omnetpp::cPacket *pkRxInProgress;
    void sendAck();

    // statistics
    omnetpp::simsignal_t receiveBeginSignal;
    omnetpp::simsignal_t receiveSignal;
    omnetpp::simsignal_t collisionLengthSignal;
    omnetpp::simsignal_t collisionSignal;

    omnetpp::simtime_t radioDelay;
    double txRate;
    omnetpp::cPar *ackLenBits;


  public:
    Server();
    virtual ~Server();

  protected:
    virtual void initialize();
    virtual void handleMessage(omnetpp::cMessage *msg);
    virtual void finish();

    void setSimParameters();
    void changeChannelState(ChannelState newState);
};

}; //namespace

#endif

