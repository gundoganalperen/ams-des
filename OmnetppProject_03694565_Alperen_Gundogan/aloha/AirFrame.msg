//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

namespace aloha;

//
// AirFrame packet, contains information about the sender
//
packet AirFrame {
    string senderName;
    // TODO Task 3.1.1: Add fields to airframe
    int pktNum;			// Storing the current number of the packet
    int senderId;		// Storing the `hostID` of the sending host
    bool isAck;			// indication whether athe packet is an acknowledgement
    // end of TODO
}
