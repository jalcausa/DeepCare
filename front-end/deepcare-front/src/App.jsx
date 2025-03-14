import { useState } from 'react'
import './App.css'

function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Aquí iría la llamada a tu backend con fetch o axios.
    // Por ahora simulamos la respuesta:
    const simulatedResponse = `Simulated response: ${input}`;
    setResponse(simulatedResponse);
    setInput("");
  };

  return (
    <div className="chat-container">
      <h1>Chatbot</h1>
      <div className="chat-box">
        {response && <div className="chat-response">{response}</div>}
      </div>
      <form onSubmit={handleSubmit} className="chat-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Escribe tu mensaje..."
        />
        <button type="submit">Enviar</button>
      </form>
    </div>
  );
}

export default App;
