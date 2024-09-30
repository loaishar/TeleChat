import React, { useState, useEffect } from 'react';

function Chat({ token }) {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');

    const fetchMessages = async () => {
        const response = await fetch('http://127.0.0.1:8000/chat/messages', {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });
        const data = await response.json();
        setMessages(data);
    };

    const sendMessage = async (e) => {
        e.preventDefault();
        await fetch('http://127.0.0.1:8000/chat/send', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: newMessage }),
        });
        setNewMessage('');
        fetchMessages();
    };

    useEffect(() => {
        fetchMessages();
    }, []);

    return (
        <div>
            <h2>Chat</h2>
            <ul>
                {messages.map((msg, index) => (
                    <li key={index}>{msg}</li>
                ))}
            </ul>
            <form onSubmit={sendMessage}>
                <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    required
                />
                <button type="submit">Send</button>
            </form>
        </div>
    );
}

export default Chat;
