import { useState, useRef, useEffect } from "react";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [user, setUser] = useState(() => {
    // Intentar cargar el usuario desde localStorage si existe
    const storedUser = localStorage.getItem("user");
    return storedUser ? JSON.parse(storedUser) : null;
  });
  const [showAuthForm, setShowAuthForm] = useState(true);
  const [authMode, setAuthMode] = useState("login");
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [darkMode, setDarkMode] = useState(
    () => localStorage.getItem("darkMode") === "true"
  );
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [fontSize, setFontSize] = useState(
    () => localStorage.getItem("fontSize") || "medium"
  );
  const [soundEnabled, setSoundEnabled] = useState(
    () => localStorage.getItem("soundEnabled") === "true"
  );

  const messagesEndRef = useRef(null);
  const textAreaRef = useRef(null);

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

  const adjustTextareaHeight = () => {
    if (textAreaRef.current) {
      textAreaRef.current.style.height = "auto";
      textAreaRef.current.style.height =
        textAreaRef.current.scrollHeight + "px";
    }
  };

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
        setUser(userData); // <-- Guardamos el id y el username
        localStorage.setItem("user", JSON.stringify(userData)); // <-- Guardamos en localStorage
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
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
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

    // Guardar mensaje del usuario
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
        body: JSON.stringify({ peticion: input }),
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

        // Guardar respuesta del bot
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
          {/* Botón para abrir la barra lateral */}
          <button className="sidebar-toggle" onClick={toggleSidebar}>
            ☰
          </button>

          {/* Barra lateral */}
          <div className={`sidebar ${sidebarOpen ? "open" : ""}`}>
            <button className="close-sidebar" onClick={toggleSidebar}>
              ✖
            </button>
            <button onClick={toggleDarkMode}>
              🌙 {darkMode ? "Modo Claro" : "Modo Oscuro"}
            </button>
            <button onClick={() => setIsSettingsOpen(true)}>⚙ Ajustes</button>

            <div className="conversations">
              <button
                className="new-conversation-btn"
                onClick={handleNewConversation}
              >
                Nueva Conversación
              </button>
              {conversations.length > 0 &&
                conversations.map((conv) => (
                  <div key={conv.id} className="conversation-item">
                    <button onClick={() => loadConversation(conv.id)}>
                      Conversación {conv.id}
                    </button>
                  </div>
                ))}
            </div>
          </div>

          {/* Chat */}
          <div className="chat-box">
            <div className="messages">
              {messages.map((message, index) => (
                <div key={index} className={`message ${message.role}`}>
                  {message.content}
                </div>
              ))}
              <div ref={messagesEndRef}></div>
            </div>
            <div className="input-container">
              <textarea
                ref={textAreaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onInput={adjustTextareaHeight}
                placeholder="Escribe un mensaje..."
              />
              <button onClick={handleSubmit}>Enviar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
