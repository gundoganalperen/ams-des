//
// This file is part of an OMNeT++/OMNEST simulation example.
//
// Copyright (C) 1992-2008 Andras Varga
//
// This file is distributed WITHOUT ANY WARRANTY. See the file
// `license' for details on this and other legal matters.
//


#include <AirFrame_m.h>
#include <omnetpp/cdisplaystring.h>
#include <omnetpp/cenvir.h>
#include <omnetpp/cgate.h>
#include <omnetpp/checkandcast.h>
#include <omnetpp/clog.h>
#include <omnetpp/cmessage.h>
#include <omnetpp/cobjectfactory.h>
#include <omnetpp/cpacket.h>
#include <omnetpp/cpar.h>
#include <omnetpp/csimulation.h>
#include <omnetpp/ctimestampedvalue.h>
#include <omnetpp/cwatch.h>
#include <omnetpp/regmacros.h>
#include <omnetpp/simkerneldefs.h>
#include <omnetpp/simtime.h>
#include <omnetpp/simtime_t.h>
#include <Server.h>
#include <cstdio>
#include <iostream>


namespace aloha {

Define_Module(Server);


Server::Server()
{
    endRxEvent = NULL;
    pkRxInProgress = NULL;
}

Server::~Server()
{
    cancelAndDelete(endRxEvent);
}

void Server::initialize()
{
    endRxEvent = new omnetpp::cMessage("end-reception");

    changeChannelState(FREE);

    gate("in")->setDeliverOnReceptionStart(true);

    setSimParameters();

    currentCollisionNumFrames = 0;
    receiveCounter = 0;
    WATCH(currentCollisionNumFrames);

    receiveSignal = registerSignal("receive");
    emit(receiveSignal, 0L);

}


void Server::handleMessage(omnetpp::cMessage *msg)
{
    if (msg==endRxEvent)
    {
        /**
         * transmission successfully finished
         */
        EV << "reception finished\n";
        changeChannelState(FREE);

        // update statistics
        omnetpp::simtime_t dt = omnetpp::simTime() - recvStartTime;
        if (currentCollisionNumFrames==0)
        {
            // start of reception at recvStartTime
            omnetpp::cTimestampedValue tmp(recvStartTime, 1l);
            emit(receiveSignal, &tmp);
            // end of reception now
            emit(receiveSignal, 0l);

            sendAck();

        }
        else
        {
            // start of collision at recvStartTime
            omnetpp::cTimestampedValue tmp(recvStartTime, currentCollisionNumFrames);

        }

        currentCollisionNumFrames = 0;
        receiveCounter = 0;

        // update network graphics
        if (omnetpp::getEnvir()->isGUI())
        {
            getDisplayString().setTagArg("i2",0,"x_off");
            getDisplayString().setTagArg("t",0,"");
        }

        cancelAndDelete(pkRxInProgress);

    }
    else
    {
        /**
         * received a new packet
         */
        omnetpp::cPacket *pkt = omnetpp::check_and_cast<omnetpp::cPacket *>(msg);

        ASSERT(pkt->isReceptionStart());
        omnetpp::simtime_t endReceptionTime = omnetpp::simTime() + pkt->getDuration();

        if (channelState==FREE)
        {
            /**
             * no collision (yet)
             */
            EV << "started receiving\n";
            recvStartTime = omnetpp::simTime();
            changeChannelState(BUSY);
            scheduleAt(endReceptionTime, endRxEvent);

            if (omnetpp::getEnvir()->isGUI())
            {
                getDisplayString().setTagArg("i2",0,"x_yellow");
                getDisplayString().setTagArg("t",0,"RECEIVE");
                getDisplayString().setTagArg("t",2,"#808000");
            }
            pkRxInProgress = pkt;
        }
        else
        {
            /**
             * collision occured
             */
            EV << "another frame arrived while receiving -- collision!\n";

            if (currentCollisionNumFrames==0)
                currentCollisionNumFrames = 2;
            else
                currentCollisionNumFrames++;

            if (endReceptionTime > endRxEvent->getArrivalTime())
            {
                cancelEvent(endRxEvent);
                scheduleAt(endReceptionTime, endRxEvent);
            }

            // update network graphics
            if (omnetpp::getEnvir()->isGUI())
            {
                getDisplayString().setTagArg("i2",0,"x_red");
                getDisplayString().setTagArg("t",0,"COLLISION");
                getDisplayString().setTagArg("t",2,"#800000");
                char buf[32];
                sprintf(buf, "Collision! (%ld frames)", currentCollisionNumFrames);
                bubble(buf);
            }

            cancelAndDelete(pkt);
        }
        changeChannelState(BUSY);
    }
}

void Server::finish()
{
}

void Server::sendAck()
{

    if (pkRxInProgress==NULL)
        error("no packet is being received...");

    /* --- TODO Task 3.1.3 --- */
    //Commented code should be used as a hint
    AirFrame *pkt = omnetpp::check_and_cast<AirFrame *>(pkRxInProgress);
    AirFrame *ack = new AirFrame();
    ack->setSenderId(pkt->getSenderId());
    ack->setPktNum(pkt->getPktNum());
    ack->setIsAck(true);


    //send direct ack
    ack->setBitLength(ackLenBits->longValue());
    int senderId = pkt->getSenderId();
    omnetpp::cModule *sender = omnetpp::cSimulation::getActiveSimulation()->getModule(senderId);
    omnetpp::simtime_t duration = ack->getBitLength() / txRate;
    sendDirect(ack, radioDelay, duration, sender->gate("in"));

    /* --- statistic --- */
    // start of sending: now
    emit(receiveSignal, 1l);
    // end of sending:
    omnetpp::simtime_t ackSendEndTime = omnetpp::simTime() + duration;
    omnetpp::cTimestampedValue tmp(ackSendEndTime, 0l);
    emit(receiveSignal, &tmp);

    /* --- end of TODO --- */
}

void Server::setSimParameters(){
    txRate = par("txRate");
    radioDelay = par("radioDelay");
    ackLenBits = &par("ackLenBits");
}

void Server::changeChannelState(ChannelState newState){
    channelState = newState;
}


}; //namespace
