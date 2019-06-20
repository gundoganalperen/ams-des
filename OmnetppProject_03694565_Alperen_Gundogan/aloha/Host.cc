//
// This file is part of an OMNeT++/OMNEST simulation example.
//
// Copyright (C) 1992-2008 Andras Varga
//
// This file is distributed WITHOUT ANY WARRANTY. See the file
// `license' for details on this and other legal matters.
//


#include "Host.h"

namespace aloha {

Define_Module(Host);


Host::Host()
{
    endTxEvent = NULL;
    pktInProgress = NULL;
    retryTxTimer = NULL;
    newRequestTimer = NULL;
}


Host::~Host()
{
    cancelAndDelete(endTxEvent);
    cancelAndDelete(retryTxTimer);
    cancelAndDelete(newRequestTimer);

}


void Host::initialize()
{
    if (enableStateStats)
        stateSignal = registerSignal("state");

    //get server object (for sending)
    server = getSimulation()->getModuleByPath("server");
    if (!server) error("server not found");

    setSimParameters();

    /* --- generate host id from module id (guaranteed to be unique within a run of a simulation) --- */
    hostId = getId();

    //schedule timers
    newRequestTimer = new omnetpp::cMessage("newRequestTimer");
    retryTxTimer = new omnetpp::cMessage("retryTxTimer");
    endTxEvent = new omnetpp::cMessage("send/endTx");

    // state manipulation
    changeState(NEW_REQUEST);
    WATCH((int&)state);

    pkCounter = 0;
    WATCH(pkCounter);

    scheduleAt(getNextTransmissionTime(), newRequestTimer);
}


void Host::handleMessage(omnetpp::cMessage *msg)
{

    if (msg->isSelfMessage()){

        if (msg==newRequestTimer){

            EV << "Generating new request..." << omnetpp::endl;

            ASSERT(state==NEW_REQUEST);

            changeState(TRANSMIT);

            sendNewPacket();

        }

        else if (msg==endTxEvent){

            ASSERT(state==TRANSMIT);

            EV << "End of transmission, going for backoff " << omnetpp::endl;

            if (reTxCount!=0) {
                /* --- TODO Task 3.1.4 --- */
                changeState(BACKLOGGED);
                cancelEvent(endTxEvent);
                scheduleAt(omnetpp::simTime(), retryTxTimer);
                /* --- end of TODO --- */
            }
            else if (reTxCount==0) {
                changeState(NEW_REQUEST);
                cancelAndDelete(pktInProgress);
                scheduleAt(getNextTransmissionTime(), newRequestTimer);
            }
        }
        /* --- TODO Task 3.1.4 --- */
        else
        {
            ASSERT(state == BACKLOGGED);
            EV << "Retransmission " << omnetpp::endl;

            changeState(TRANSMIT);
            cancelEvent(retryTxTimer);
            retransmitPacket();
        }
        /* --- end of TODO --- */

    }
    else {
        //must be ack
        processAck(msg);
    }
}


omnetpp::simtime_t Host::getNextTransmissionTime()
{

    omnetpp::simtime_t t = omnetpp::simTime() + getNextArrivalTime()*slotTime;

    // align time of next transmission to a slot boundary
    return slotTime * ceil(t.dbl()/slotTime);
}


omnetpp::simtime_t Host::getBackOffTime(){

    /* --- TODO Task 4.1.2 --- */
    int backoff = uniform(1, maxBackOff);
    return slotTime*backoff;
    /* --- End of TODO --- */
}



bool Host::checkAck(omnetpp::cMessage * msg){

    /* --- TODO Task 3.1.4 --- Implement an ACK check */
    AirFrame *pkt = omnetpp::check_and_cast<AirFrame *>(msg);
    if(pkt->getIsAck() && (pkt->getSenderId() == pktInProgress->getSenderId() && pkt->getPktNum() == pktInProgress->getPktNum()))
    {
        return true;
    }
    else
        return false;

    /* --- End of TODO --- */
}


AirFrame * Host::createPacket(){
    char pkname[40];
    sprintf(pkname,"pk-%d-#%d", hostId, pkCounter++);

    EV << "generating packet " << pkname <<omnetpp::endl;

    AirFrame * frame = new AirFrame(pkname);

    /* --- TODO Task 3.1.2 --- *//* */
    frame->setSenderId(hostId);
    frame->setPktNum(pkCounter);
    frame->setIsAck(false);
    /* *//* --- End of TODO --- */

    frame->setBitLength(pkLenBits->longValue());
    return frame;
}

void Host::changeState(HostState newState){
    state = newState;

    if (enableStateStats)
        emit(stateSignal, state);

    // update network graphics
    char const * color = "";
    char const * stateName = "";

    switch (state)
    {
    case TRANSMIT:
        color = "yellow";
        stateName = "TRANSMIT";
        break;
    case BACKLOGGED:
        color = "red";
        stateName = "BACKLOGGED";
        break;
    case NEW_REQUEST:
        color = "blue";
        stateName = "NEW_REQUEST";
        break;
    }

    if (omnetpp::getEnvir()->isGUI())
    {
        getDisplayString().setTagArg("i",1,color);
        getDisplayString().setTagArg("t",0,stateName);
    }

}

void Host::setSimParameters(){
    txRate = par("txRate");
    radioDelay = par("radioDelay");
    //iaTime = &par("iaTime");
    load = par("load");
    pkLenBits = &par("pkLenBits");
    maxReTx = par("maxReTx");
    maxBackOff = par("maxBackOff");
    slotTime = par("slotTime");
    ASSERT(slotTime>0);
    WATCH(slotTime);
}

void Host::sendNewPacket(){
    pktInProgress = createPacket();
    omnetpp::simtime_t duration = pktInProgress->getBitLength() / txRate;
    sendDirect(pktInProgress->dup(), radioDelay, duration, server->gate("in"));
    scheduleAt(omnetpp::simTime()+duration, endTxEvent);
    //in order to wait for ack
    reTxCount=maxReTx;
}

void Host::retransmitPacket(){
    omnetpp::simtime_t duration = pktInProgress->getBitLength() / txRate;
    sendDirect(pktInProgress->dup(), radioDelay, duration, server->gate("in"));
    changeState(TRANSMIT);
    scheduleAt(omnetpp::simTime()+duration, endTxEvent);
    reTxCount--;
}

void Host::processAck(omnetpp::cMessage * msg){
    EV << "Got an ack, cleaning up" << omnetpp::endl;


    if (state==NEW_REQUEST || state==TRANSMIT)
    {
        delete msg;
    }

    /* --- TODO Task 3.1.4 --- */
    // If message is received in backoff state of the Host
    else
    {
        if(checkAck(msg)) // if the received message is true.
        {
            changeState(NEW_REQUEST);
            cancelAndDelete(pktInProgress);
            scheduleAt(getNextTransmissionTime(), newRequestTimer);
        }
        else
        {
            changeState(TRANSMIT);
            // Cancel endTxEvent timer and schedule backoff Timer
            cancelEvent(endTxEvent);
            scheduleAt(getBackOffTime(), retryTxTimer);
        }
    }
    /* --- End of TODO --- */
}

double Host::getNextArrivalTime(){

    return exponential(1/load);

}


}; //namespace
