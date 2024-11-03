import axios from 'axios';
import dotenv from 'dotenv';
dotenv.config();

const BASE_API_URL = process.env.BASE_API_URL;

async function createRoom(roomData) {
    try {
        const response = await axios.post(`${BASE_API_URL}/createRoom`, roomData);
        console.log('Room created:', response.data);
    } catch (error) {
        console.error('Error creating room:', error);
    }
}

async function addElementToRoom(roomId, elementData) {
    try {
        const response = await axios.post(`${BASE_API_URL}/rooms/${roomId}/addElement`, elementData);
        console.log('Element added to the room:', response.data);
    } catch (error) {
        console.error('Error adding element to room:', error);
    }
}

async function getRoomDetails(roomId) {
    try {
        const response = await axios.get(`${BASE_API_URL}/rooms/${roomId}`);
        console.log('Room details:', response.data);
        displayRoomDetails(response.data);
    } catch (error) {
        console.error('Error fetching room details:', error);
    }
}

function displayRoomDetails(roomDetails) {
    const roomDetailsContainer = document.querySelector('#room-details');
    roomDetailsContainer.innerHTML = `
        <h2>Room Name: ${roomDetails.name}</h2>
        <p>Room ID: ${roomDetails.id}</p>
        <div>Elements: ${roomDetails.elements.map(element => `<p>${element.name}</p>`).join('')}</div>
    `;
}

function setUpEventListeners() {
    const createRoomButton = document.querySelector('#create-room');
    createRoomButton.addEventListener('click', () => {
        const roomData = { name: 'New Room', description: 'A newly created room' };
        createRoom(roomData);
    });

    const addElementButton = document.querySelector('#add-element');
    addElementButton.addEventListener('click', () => {
        const roomId = 'room1';
        const elementData = { name: 'New Element', type: 'Furniture' };
        addElementToRoom(roomId, elementData);
    });

    const getRoomDetailsButton = document.querySelector('#get-room-details');
    getRoomDetailsButton.addEventListener('click', () => {
        const roomId = 'room1';
        getRoomDetails(roomId);
    });
}

function init() {
    setUpEventListeners();
}

init();