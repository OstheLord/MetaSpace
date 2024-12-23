import React, { useState } from 'react';

const CreateRoomForm = () => {
  const [roomName, setRoomName] = useState('');
  const [roomDescription, setRoomDescription] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!roomName || !roomDescription) {
      alert('Both room name and description are required!');
      return;
    }

    console.log('Submitting', { roomName, roomDescription });

    setRoomName('');
    setRoomDescription('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="roomName">Room Name:</label>
        <input
          type="text"
          id="roomName"
          value={roomName}
          onChange={(e) => setRoomName(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="roomDescription">Room Description:</label>
        <textarea
          id="roomDescription"
          value={roomDescription}
          onChange={(e) => setRoomDescription(e.target.value)}
        ></textarea>
      </div>
      <div>
        <button type="submit">Create Room</button>
      </div>
    </form>
  );
};

export default CreateRoomForm;