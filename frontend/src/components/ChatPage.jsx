import React, { useState, useEffect, useRef } from "react";
import "./ChatPage.css";

function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const sendMessage = async () => {
  if (!input.trim()) return;
  const userMessage = { sender: "user", text: input };
  setMessages((prev) => [...prev, userMessage]);
  setInput("");
  setLoading(true);

  try {
    const BASE_URL = import.meta.env.VITE_API_URL;
    const response = await fetch(`${BASE_URL}/start-chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: input }),
    });

    if (!response.ok) {
      throw new Error(`Server returned ${response.status} ${response.statusText}`);
    }

    const data = await response.json();

    if (!data.message) {
      throw new Error("Response does not contain a message.");
    }

    const botMessage = { sender: "bot", text: data.message };
    setMessages((prev) => [...prev, botMessage]);
  } catch (err) {
    setMessages((prev) => [
      ...prev,
      { sender: "bot", text: `Error: ${err.message}` },
    ]);
  } finally {
    setLoading(false);
  }
};


  const handleKeyDown = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div className={`chat-page ${darkMode ? "dark" : "light"}`}>
      <div className="chat-header">
        <h2>Code-Whisper Assistant</h2>
        <button className="mode-toggle" onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? "🌞 Light Mode" : "🌙 Dark Mode"}
        </button>
      </div>

      <div className="chat-window">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message-bubble ${msg.sender === "user" ? "user" : "bot"}`}
          >
            {msg.text}
          </div>
        ))}
        {loading && <div className="message-bubble bot">Thinking...</div>}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question..."
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatPage;
