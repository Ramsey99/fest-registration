// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EventRegistration {
    struct Participant {
        string fullname;
        string stream;
        string eventName;
        string email;
        string phno;
        string roll;
    }

    mapping(address => Participant) public participants;
    address[] public participantAddresses;

    function registerParticipant(
        string memory _fullname,
        string memory _stream,
        string memory _eventName,
        string memory _email,
        string memory _phno,
        string memory _roll
    ) public {
        Participant memory newParticipant = Participant({
            fullname: _fullname,
            stream: _stream,
            eventName: _eventName,
            email: _email,
            phno: _phno,
            roll: _roll
        });
        participants[msg.sender] = newParticipant;
        participantAddresses.push(msg.sender);
    }

    function getParticipant(address _addr)
        public
        view
        returns (
            string memory,
            string memory,
            string memory,
            string memory,
            string memory,
            string memory
        )
    {
        Participant memory participant = participants[_addr];
        return (
            participant.fullname,
            participant.stream,
            participant.eventName,
            participant.email,
            participant.phno,
            participant.roll
        );
    }

    function getParticipantsCount() public view returns (uint256) {
        return participantAddresses.length;
    }
}
