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

    event ParticipantRegistered(
        address indexed participantAddress,
        string fullname,
        string eventName
    );
    event ParticipantUpdated(
        address indexed participantAddress,
        string fullname,
        string eventName
    );

    function registerParticipant(
        string memory _fullname,
        string memory _stream,
        string memory _eventName,
        string memory _email,
        string memory _phno,
        string memory _roll
    ) public {
        require(bytes(_fullname).length > 0, "Full name is required.");
        require(bytes(_stream).length > 0, "Stream is required.");
        require(bytes(_eventName).length > 0, "Event name is required.");
        require(bytes(_email).length > 0, "Email is required.");
        require(bytes(_phno).length > 0, "Phone number is required.");
        require(bytes(_roll).length > 0, "Roll number is required.");
        
        if (bytes(participants[msg.sender].fullname).length == 0) {
            participantAddresses.push(msg.sender);
            emit ParticipantRegistered(msg.sender, _fullname, _eventName);
        } else {
            emit ParticipantUpdated(msg.sender, _fullname, _eventName);
        }

        participants[msg.sender] = Participant({
            fullname: _fullname,
            stream: _stream,
            eventName: _eventName,
            email: _email,
            phno: _phno,
            roll: _roll
        });
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
