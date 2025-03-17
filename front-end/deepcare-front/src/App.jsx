import { useState, useRef, useEffect } from "react";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem("darkMode") === "true";
  });
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [fontSize, setFontSize] = useState(() => localStorage.getItem("fontSize") || "medium");
  const [soundEnabled, setSoundEnabled] = useState(() => localStorage.getItem("soundEnabled") === "true");

  const messagesEndRef = useRef(null);

  const inputRef = useRef(null);

const adjustTextareaHeight = () => {
  if (inputRef.current) {
    inputRef.current.style.height = "auto"; 
    inputRef.current.style.height = inputRef.current.scrollHeight + "px";
  }
};

useEffect(() => {
  document.body.classList.toggle("dark-mode", darkMode);
  document.body.classList.remove("small-font", "medium-font", "large-font");
  document.body.classList.add(`${fontSize}-font`);
  localStorage.setItem("darkMode", darkMode);
  localStorage.setItem("fontSize", fontSize);
}, [darkMode, fontSize]);



  const toggleDarkMode = () => setDarkMode(!darkMode);
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: input }]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ peticion: input }),
      });

      if (!res.ok) throw new Error("Error en el servidor");

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        data.tipo === "grafico"
          ? { role: "bot", content: <img src={`data:image/png;base64,${data.grafico}`} alt="Gráfico" /> }
          : { role: "bot", content: data.texto },
      ]);
    } catch {
      setMessages((prev) => [...prev, { role: "bot", content: "Error al procesar tu mensaje." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      {/* Botón de la barra lateral */}
      <button className="sidebar-toggle" onClick={toggleSidebar}>☰</button>

      {/* Barra lateral */}
      <div className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <button className="close-sidebar" onClick={toggleSidebar}>✖</button>
        <button onClick={toggleDarkMode}>🌙 {darkMode ? "Modo Claro" : "Modo Oscuro"}</button>
        <button onClick={() => setIsSettingsOpen(true)}>⚙ Ajustes</button>
          {/* Modal de configuración */}
            {isSettingsOpen && (
              <div className={`modal ${darkMode ? "dark-mode" : ""}`}>
                <div className="modal-content">
                  <span className="close-modal" onClick={() => setIsSettingsOpen(false)}>✖</span>
                  <h2>Configuración</h2>

                  {/* Selector de tamaño de letra */}
                  <label htmlFor="font-size">Tamaño de letra:</label>
                  <select 
                    id="font-size" 
                    value={fontSize} 
                    onChange={(e) => setFontSize(e.target.value)}
                  >
                    <option value="small">Pequeño</option>
                    <option value="medium">Mediano</option>
                    <option value="large">Grande</option>
                  </select>

                  {/* Activar/Desactivar sonido */}
                  <label>
                    <input 
                      type="checkbox" 
                      checked={soundEnabled} 
                      onChange={() => setSoundEnabled(!soundEnabled)} 
                    />
                    Activar sonido de notificación
                  </label>

                  {/* Botón para guardar ajustes */}
                  <button 
                    onClick={() => {
                      localStorage.setItem("fontSize", fontSize);
                      localStorage.setItem("soundEnabled", soundEnabled);
                      setIsSettingsOpen(false);
                    }}
                  >
                    Guardar
                  </button>
                </div>
              </div>
            )}
        <button>🎨 Personalizar</button>
      </div>

      <h1 className="chat-title">⚕️ DeepCare</h1>
      
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-content">{message.content}</div>
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
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Escribe tu mensaje..."
        disabled={isLoading}
        rows="1"
        ref={inputRef}
        onInput={adjustTextareaHeight}
      />


        <button type="submit" disabled={isLoading}>➤</button>
      </form>
    </div>
  );
}

export default App;
