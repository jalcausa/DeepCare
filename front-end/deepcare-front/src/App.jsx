import { useState, useRef, useEffect } from "react";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Agregar mensaje del usuario a la lista
    const mensajeUsuario = input;
    setMessages((prev) => [...prev, { role: "user", content: mensajeUsuario }]);
    setInput("");
    setIsLoading(true);

    try {
      // Llamada al backend
      const res = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ peticion: mensajeUsuario }),
      });

      if (!res.ok) {
        throw new Error("Error en la respuesta del servidor");
      }

      const data = await res.json();

      // Verificar si la respuesta contiene un gráfico
      if (data.tipo === "grafico") {
        // Mostrar el gráfico como imagen en el chat
        setMessages((prev) => [
          ...prev,
          {
            role: "bot",
            content: (
              <img
                src={`data:image/png;base64,${data.grafico}`}
                alt="Gráfico generado"
              />
            ),
          },
        ]);
      } else if (data.tipo === "texto") {
        // Si es texto, mostrarlo normalmente
        setMessages((prev) => [
          ...prev,
          { role: "bot", content: data.texto },
        ]);
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: "Ocurrió un error al procesar tu mensaje." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <h1 className="chat-title">DeepCare</h1>
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-content">
              {typeof message.content === "string"
                ? message.content
                : message.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message bot">
            <div className="message-content">
              <div className="loading-dots">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Escribe tu mensaje..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          <svg
            stroke="currentColor"
            fill="none"
            strokeWidth="2"
            viewBox="0 0 24 24"
            height="1.2em"
            width="1.2em"
          >
            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"></path>
          </svg>
        </button>
      </form>
    </div>
  );
}

export default App;
