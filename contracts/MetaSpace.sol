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
        rooms[roomIdCounter] = Room(roomIdCounter, name, new address[](0));
        // Here owner implicitly becomes a member by creating the room.
        rooms[roomIdCounter].members.push(msg.sender);
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
        for (uint256 i = 0; i < rooms[roomId].members.length; i++) {
            if (rooms[roomId].members[i] == member) {
                rooms[roomId].members[i] = rooms[roomId].members[rooms[roomId].members.length - 1];
                rooms[roomId].members.pop();
                break;
            }
        }
        // Assuming we might want to clean up the userRooms mapping.
        removeUserRoom(member, roomId);

        emit MemberRemoved(roomId, member);
    }

    function getRoomDetails(uint256 roomId) public view returns (Room memory) {
        return rooms[roomId];
    }

    function getUserRooms(address user) public view returns (uint256[] memory) {
        return userRooms[user];
    }

    function isRoomMember(uint256 roomId, address user) public view returns (bool) {
        for (uint256 i = 0; i < rooms[roomId].members.length; i++) {
            if (rooms[roomId].members[i] == user) {
                return true;
            }
        }
        return false;
    }

    function removeUserRoom(address user, uint256 roomId) private {
        uint256[] storage userRoomIds = userRooms[user];
        for (uint256 i = 0; i < userRoomIds.length; i++) {
            if (userRoomIds[i] == roomId) {
                userRoomIds[i] = userRoomIds[userRoomIds.length - 1];
                userRoomIds.pop();
                break;
            }
        }
    }
}