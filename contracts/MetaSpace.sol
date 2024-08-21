pragma solidity ^0.8.0;

contract VirtualRoomManager {
    address public owner;
    uint256 public roomIdCounter = 1;

    struct Room {
        uint256 id;
        string name;
        address[] members;
    }

    mapping(uint256 => Room) public rooms;
    mapping(address => uint256[]) public userRooms;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }

    modifier onlyRoomMembers(uint256 roomId) {
        require(isRoomMember(roomId, msg.sender), "Only room members can perform this action");
        _;
    }

    event RoomCreated(uint256 roomId, string roomName);
    event MemberAdded(uint256 roomId, address newMember);
    event MemberRemoved(uint256 roomId, address member);

    constructor() {
        owner = msg.sender;
    }
    
    function createRoom(string memory name) public {
        Room storage newRoom = rooms[roomIdCounter];
        newRoom.id = roomIdCounter;
        newRoom.name = name;
        newRoom.members.push(msg.sender);
        
        userRooms[msg.sender].push(roomIdCounter);
        
        emit RoomCreated(roomIdCounter, name);
        roomIdCounter++;
    }

    function addMember(uint256 roomId, address newMember) public onlyRoomMembers(roomId) {
        require(!isRoomMember(roomId, newMember), "User is already a member");
        
        rooms[roomId].members.push(newMember);
        userRooms[newMember].push(roomId);

        emit MemberAdded(roomId, newMember);
    }

    function removeMember(uint256 roomId, address member) public onlyRoomMembers(roomId) {
        _removeFromArray(rooms[roomId].members, member);
        _removeFromArray(userRooms[member], roomId);

        emit MemberRemoved(roomId, member);
    }

    function getRoomDetails(uint256 roomId) public view returns (Room memory) {
        return rooms[roomId];
    }

    function getUserRooms(address user) public view returns (uint256[] memory) {
        return userRooms[user];
    }

    function isRoomMember(uint256 roomId, address user) public view returns (bool) {
        address[] memory members = rooms[roomId].members;
        for (uint256 i = 0; i < members.length; i++) {
            if (members[i] == user) {
                return true;
            }
        }
        return false;
    }

    function _removeFromArray(address[] storage array, address valueToRemove) private {
        for (uint256 i = 0; i < array.length; i++) {
            if (array[i] == valueToRemove) {
                array[i] = array[array.length - 1];
                array.pop();
                break;
            }
        }
    }

    function _removeFromArray(uint256[] storage array, uint256 valueToRemove) private {
        for (uint256 i = 0; i < array.length; i++) {
            if (array[i] == valueToRemove) {
                array[i] = array[array.length - 1];
                array.pop();
                break;
            }
        }
    }
}