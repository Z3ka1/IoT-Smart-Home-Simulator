import {io} from 'socket.io-client';

const socket = io('http://localhost:8000', {
    withCredentials: true,
    autoConnect: true
})

socket.on('connect', () => {
    console.log('Socket connected socket.io')
})

socket.on('disconnect', () => {
    console.log('Socket disconected')
})

socket.on('connect_error', (error) => {
    console.log('Socket connection error:', error)
})


export default socket