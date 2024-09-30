import React, { useState } from "react";
import Register from "./components/Register";
import Login from "./components/Login";
import Chat from "./components/Chat";

function App() {
  const [token, setToken] = useState(null);

  return (
    <div className="App">
      <h1>TeleChat</h1>
      {!token ? (
        <>
          <Register />
          <Login setToken={setToken} />
        </>
      ) : (
        <Chat token={token} />
      )}
    </div>
  );
}

export default App;