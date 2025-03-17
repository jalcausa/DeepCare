import { useState, useRef, useEffect } from "react";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [user, setUser] = useState(null);
  const [showAuthForm, setShowAuthForm] = useState(true);
  const [authMode, setAuthMode] = useState("login");
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem("darkMode") === "true");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [fontSize, setFontSize] = useState(() => localStorage.getItem("fontSize") || "medium");
  const [soundEnabled, setSoundEnabled] = useState(() => localStorage.getItem("soundEnabled") === "true");

  const messagesEndRef = useRef(null);
  const textAreaRef = useRef(null);

  const adjustTextareaHeight = () => {
    if (inputRef.current) {
      inputRef.current.style.height = "auto"; 
      inputRef.current.style.height = inputRef.current.scrollHeight + "px";
    }
  };

  useEffect(() => {
    // Cambiar el modo oscuro y el tamaño de la fuente en el body
    document.body.classList.toggle("dark-mode", darkMode);
    document.body.classList.remove("small-font", "medium-font", "large-font");
    document.body.classList.add(`${fontSize}-font`);
    
    // Guardar en localStorage
    localStorage.setItem("darkMode", darkMode);
    localStorage.setItem("fontSize", fontSize);
  
    // Ajustar la altura del textArea para que se ajuste al contenido
    if (textAreaRef.current) {
      textAreaRef.current.style.height = "auto";
      textAreaRef.current.style.height = `${textAreaRef.current.scrollHeight}px`;
    }
  
    // Desplazar automáticamente hacia abajo en el chat cuando cambian los mensajes
    scrollToBottom();
  }, [darkMode, fontSize, input, messages]);
  

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const toggleDarkMode = () => setDarkMode(!darkMode);
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);
  
  const handleAuth = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const credentials = {
      username: formData.get("username"),
      password: formData.get("password")
    };

    try {
      const endpoint = authMode === "login" ? "/login" : "/register";
      const res = await fetch(`http://localhost:5000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(credentials)
      });

      if (res.ok) {
        const data = await res.json();
        setUser({ username: credentials.username });
        setShowAuthForm(false);
        loadUserConversations(credentials.username);
      }
    } catch (error) {
      console.error("Authentication error:", error);
    }
  };

  const loadUserConversations = async (username) => {
    try {
      const res = await fetch(`http://localhost:5000/users/${username}/conversations`);
      if (res.ok) {
        const data = await res.json();
        setConversations(data);
        if (data.length > 0) {
          loadConversation(data[0].id);
        }
      }
    } catch (error) {
      console.error("Error loading conversations:", error);
    }
  };

  const loadConversation = async (conversationId) => {
    try {
      const res = await fetch(`http://localhost:5000/conversations/${conversationId}/messages`);
      if (res.ok) {
        const data = await res.json();
        setMessages(data);
        setActiveConversation(conversationId);
      }
    } catch (error) {
      console.error("Error loading messages:", error);
    }
  };

  const handleNewConversation = async () => {
    try {
      const res = await fetch("http://localhost:5000/start_conversation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: user.id })
      });
      
      if (res.ok) {
        const data = await res.json();
        setActiveConversation(data.conversation_id);
        loadUserConversations(user.username);
        setMessages([]);
      }
    } catch (error) {
      console.error("Error creating new conversation:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    let currentConv = activeConversation;
    if (!currentConv) {
      try {
        const res = await fetch("http://localhost:5000/start_conversation", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_id: user.id })
        });
        
        if (res.ok) {
          const data = await res.json();
          currentConv = data.conversation_id;
          setActiveConversation(currentConv);
          loadUserConversations(user.username);
        }
      } catch (error) {
        console.error("Error creating conversation:", error);
        return;
      }
    }

    // Guardar mensaje del usuario
    try {
      await fetch("http://localhost:5000/send_message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: currentConv,
          sender: "user",
          content: input
        })
      });
    } catch (error) {
      console.error("Error saving message:", error);
    }

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ peticion: input })
      });

      if (res.ok) {
        const data = await res.json();
        const botMessage = {
          role: "bot",
          content: data.tipo === "grafico" ? (
            <img 
              src={`data:image/png;base64,${data.grafico}`} 
              alt="Gráfico generado"
              className="chart-image"
            />
          ) : data.texto
        };
        
        setMessages(prev => [...prev, botMessage]);
        
        // Guardar respuesta del bot
        await fetch("http://localhost:5000/send_message", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            conversation_id: currentConv,
            sender: "bot",
            content: data.tipo === "grafico" ? "Gráfico generado" : data.texto
          })
        });
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages(prev => [
        ...prev,
        { role: "bot", content: "Ocurrió un error al procesar tu mensaje." }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      {showAuthForm ? (
        <div className="auth-container">
          <div className="auth-box">
            <h2>{authMode === "login" ? "Iniciar Sesión" : "Registro"}</h2>
            <form onSubmit={handleAuth}>
              <input
                type="text"
                name="username"
                placeholder="Nombre de usuario"
                required
              />
              <input
                type="password"
                name="password"
                placeholder="Contraseña"
                required
              />
              <button type="submit">
                {authMode === "login" ? "Entrar" : "Registrarse"}
              </button>
            </form>
            <button 
              className="switch-mode"
              onClick={() => setAuthMode(authMode === "login" ? "register" : "login")}
            >
              {authMode === "login" 
                ? "¿No tienes cuenta? Regístrate" 
                : "¿Ya tienes cuenta? Inicia sesión"}
            </button>
          </div>
        </div>
      ) : (
        <div className="chat-container">
          {/* Botón para abrir la barra lateral */}
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
  
          {/* Título de la conversación */}
          <h1 className="chat-title">⚕️ DeepCare</h1>
  
          <div className="chat-sidebar-info">
            <div className="user-info">
              <span className="username">{user?.username}</span>
              <button 
                className="new-chat-btn"
                onClick={handleNewConversation}
              >
                + Nueva conversación
              </button>
              <button 
                className="logout-btn"
                onClick={() => setShowAuthForm(true)}
              >
                Cerrar sesión
              </button>
            </div>
            <div className="conversations-list">
              {conversations.map((conv) => (
                <div
                  key={conv.id}
                  className={`conversation-item ${activeConversation === conv.id ? 'active' : ''}`}
                  onClick={() => loadConversation(conv.id)}
                >
                  <div className="conversation-preview">
                    {conv.preview}
                  </div>
                  <div className="conversation-date">
                    {new Date(conv.created_at).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>
          </div>
  
          <div className="chat-messages">
            {messages.map((message, index) => (
              <div key={index} className={`message ${message.role}`}>
                <div className="avatar">
                  {message.role === "user" ? (
                    <svg viewBox="0 0 24 24" width="24" height="24">
                      <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
                    </svg>
                  ) : (
                    <svg viewBox="0 0 24 24" width="24" height="24">
                      <path fill="currentColor" d="M20.9 10.5c-.2-.6-.8-1-1.4-1h-4.5v-5c0-.6-.4-1-1-1s-1 .4-1 1v5h-4.5c-.6 0-1.2.4-1.4 1s0 1.2.4 1.6l7.5 7.5c.2.2.4.3.6.3s.4-.1.6-.3l7.5-7.5c.5-.4.6-1 .4-1.6z"/>
                    </svg>
                  )}
                </div>
                <div className="message-content">
                  {message.content}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message bot">
                <div className="loading-dots">
                  <div className="dot"></div>
                  <div className="dot"></div>
                  <div className="dot"></div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
  
          <form onSubmit={handleSubmit} className="chat-input-form">
            <textarea
              ref={textAreaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Escribe tu mensaje..."
              rows="1"
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading}>
              ➤
            </button>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;