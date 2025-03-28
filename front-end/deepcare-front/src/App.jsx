import { useState, useRef, useEffect } from "react";
import "./App.css";
import React from 'react';

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem("user");
    return storedUser ? JSON.parse(storedUser) : null;
  });
  const [showAuthForm, setShowAuthForm] = useState(true);
  const [authMode, setAuthMode] = useState("login");
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [darkMode, setDarkMode] = useState(
    () => (user ? localStorage.getItem("darkMode") === "true" : false)
  );
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [fontSize, setFontSize] = useState(
    () => localStorage.getItem("fontSize") || "medium"
  );
  const [soundEnabled, setSoundEnabled] = useState(
    () => localStorage.getItem("soundEnabled") === "true"
  );

  const adjustTextareaHeight = () => {
    if (inputRef.current) {
      inputRef.current.style.height = "auto"; 
      inputRef.current.style.height = inputRef.current.scrollHeight + "px";
    }
  };

  const messagesEndRef = useRef(null);
  const textAreaRef = useRef(null);

  const convertirNegrita = (texto) => {
    return texto.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  };
  


  useEffect(() => {
    document.body.classList.toggle("dark-mode", darkMode);
  }, [darkMode]);

  useEffect(() => {
    document.body.classList.remove("small-font", "medium-font", "large-font");
    document.body.classList.add(`${fontSize}-font`);
    localStorage.setItem("fontSize", fontSize);
  }, [fontSize]);

  useEffect(() => {
    localStorage.setItem("darkMode", darkMode);
  }, [darkMode]);

  useEffect(() => {
    localStorage.setItem("soundEnabled", soundEnabled);
  }, [soundEnabled]);

  useEffect(() => {
    if (textAreaRef.current) {
      textAreaRef.current.style.height = "auto";
      textAreaRef.current.style.height = `${textAreaRef.current.scrollHeight}px`;
    }
  }, [input]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const toggleDarkMode = () => {
    setDarkMode((prev) => {
      const newMode = !prev;
      localStorage.setItem("darkMode", newMode);
      return newMode;
    });
  };
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  const handleAuth = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const credentials = {
      username: formData.get("username"),
      password: formData.get("password"),
    };

    try {
      const endpoint = authMode === "login" ? "/login" : "/register";
      const res = await fetch(`http://localhost:5000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(credentials),
      });
      if (res.ok) {
        const data = await res.json();
        const userData = { id: data.id, username: data.username };
        setUser(userData);
        localStorage.setItem("user", JSON.stringify(userData));
        setShowAuthForm(false);
        loadUserConversations(data.username);
      }
    } catch (error) {
      console.error("Authentication error:", error);
    }
  };

  const loadUserConversations = async (username) => {
    try {
      const res = await fetch(
        `http://localhost:5000/users/${username}/conversations`
      );
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
      const res = await fetch(
        `http://localhost:5000/conversations/${conversationId}/messages`
      );
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
        body: JSON.stringify({ user_id: user.id }),
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
          body: JSON.stringify({ user_id: user.id }),
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
    try {
      await fetch("http://localhost:5000/send_message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: currentConv,
          sender: "user",
          content: input,
        }),
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
        body: JSON.stringify({
          peticion: input,
          user_id: user.id,
          conversation_id: activeConversation,
       	}),
      });
      if (res.ok) {
        const data = await res.json();
        const botMessage = {
          role: "bot",
          content:
            data.tipo === "grafico" ? (
              <img
                src={`data:image/png;base64,${data.grafico}`}
                alt="Gráfico generado"
                className="chart-image"
              />
            ) : (
              data.texto
            ),
        };
        setMessages((prev) => [...prev, botMessage]);
        await fetch("http://localhost:5000/send_message", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            conversation_id: currentConv,
            sender: "bot",
            content: data.tipo === "grafico" ? "Gráfico generado" : data.texto,
          }),
        });
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

  const handleLogout = () => {
    localStorage.removeItem("user");
    setUser(null);
    setShowAuthForm(true);
    setConversations([]);
    setMessages([]);
    setActiveConversation(null);
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
              onClick={() =>
                setAuthMode(authMode === "login" ? "register" : "login")
              }
            >
              {authMode === "login"
                ? "¿No tienes cuenta? Regístrate"
                : "¿Ya tienes cuenta? Inicia sesión"}
            </button>
          </div>
        </div>
      ) : (
        <div className="chat-container">
          <header className="chat-header">
            <h1 className="chat-title">⚕️ DeepCare</h1>
          </header>
          <button className="sidebar-toggle" onClick={toggleSidebar}>
            ☰
          </button>
          <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
            <button className="close-sidebar" onClick={toggleSidebar}>
              ✖
            </button>
            <button onClick={toggleDarkMode}>
              🌙 {darkMode ? "Modo Claro" : "Modo Oscuro"}
            </button>
            <button onClick={() => setIsSettingsOpen(true)}>⚙ Ajustes</button>
            {/* Modal de configuración */}
            {isSettingsOpen && (
              <div className={`modal ${darkMode ? "dark-mode" : ""}`}>
                <div className="modal-content">
                  <span
                    className="close-modal"
                    onClick={() => setIsSettingsOpen(false)}
                  >
                    ✖
                  </span>
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
                    {"  "}Activar sonido de notificación
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
            <div className="conversations-section">
              <button
                className="new-conversation-btn"
                onClick={handleNewConversation}
              >
                + Nueva conversación
              </button>
              {conversations.length > 0 && (
                <div className="conversations-list">
                  {conversations.map((conv) => (
                    <div
                      key={conv.id}
                      className={`conversation-item ${
                        activeConversation === conv.id ? "active" : ""
                      }`}
                      onClick={() => loadConversation(conv.id)}
                    >
                      <div className="conversation-preview">
                        <div
                          className="conversation-preview"
                          dangerouslySetInnerHTML={{
                            __html:
                              typeof conv.preview === "string"
                                ? convertirNegrita(conv.preview)
                                : "",
                          }}
                        ></div>
                        {typeof conv.preview !== "string" && conv.preview}
                      </div>
                      <div className="conversation-date">
                        {new Date(conv.created_at).toLocaleDateString()}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
            <button className="logout-btn" onClick={handleLogout}>
              Cerrar sesión
            </button>
          </aside>
          <main className="chat-main">
            <div className="messages">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`message-wrapper ${
                    message.role === "user" ? "user" : "bot"
                  }`}
                >
                  {message.role === "bot" && (
                    <div className="avatar bot-avatar">🤖</div>
                  )}

                  <div className={`message ${message.role}`}>
                    <div
                      className="message-content"
                      dangerouslySetInnerHTML={{
                        __html:
                          typeof message.content === "string"
                            ? convertirNegrita(message.content)
                            : "",
                      }}
                    ></div>
                    {typeof message.content !== "string" && message.content}
                  </div>

                  {message.role === "user" && (
                    <div className="avatar user-avatar">
                      <svg viewBox="0 0 24 24" width="24" height="24">
                        <path
                          fill="currentColor"
                          d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"
                        />
                      </svg>
                    </div>
                  )}
                </div>
              ))}
              {isLoading && (
                <div className="message-wrapper bot">
                  <div className="avatar bot-avatar">🤖</div>
                  <div className="message bot">
                    <div className="loading-dots">
                      <span className="dot"></span>
                      <span className="dot"></span>
                      <span className="dot"></span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef}></div>
            </div>
            <form onSubmit={handleSubmit} className="chat-input-form">
              <textarea
                ref={textAreaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onInput={() => {
                  if (textAreaRef.current) {
                    textAreaRef.current.style.height = "auto";
                    textAreaRef.current.style.height = `${textAreaRef.current.scrollHeight}px`;
                  }
                }}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault(); // Evita el salto de línea
                    handleSubmit(e); // Envía el mensaje
                  }
                }}
                placeholder="Escribe tu mensaje..."
                rows="1"
                disabled={isLoading}
              />
              <button type="submit" disabled={isLoading}>
                ➤
              </button>
            </form>
          </main>
        </div>
      )}
    </div>
  );
}

export default App;
