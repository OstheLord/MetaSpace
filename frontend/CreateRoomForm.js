import React, { useState } from 'react';

const CreateRoomForm = () => {
  const [roomName, setRoomName] = useState('');
  const [roomDescription, setRoomDescription] = useState('');
  const [validationError, setValidationError] = useState('');

  const validateRoomName = (name) => {
    if (name.length < 5) {
      return 'Room name must be at least 5 characters long.';
    }
    if (!/^[a-zA-Z0-9 ]*$/.test(name)) {
      return 'Room name must only contain alphanumeric characters and spaces.';
    }
    return '';
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const error = validateRoomName(roomName);

    if (error) {
      setValidationError(error);
      return;
    }

    if (!roomDescription) {
      alert('Room description is required!');
      return;
    }

    console.log('Submitting', { roomName, roomDescription });
    // Reset form states
    setRoomName('');
    setRoomDescription('');
    setValidationError('');
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
        {validationError && <p style={{color: 'red'}}>{validationError}</p>}
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