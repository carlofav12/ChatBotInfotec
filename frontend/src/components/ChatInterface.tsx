// ChatInterface.tsx
import React, { useState, useRef, useEffect } from "react";
import {
  Send,
  Trash2,
  Wifi,
  WifiOff,
  Bot,
  Paperclip,
  Mic,
  Smile,
} from "lucide-react";
import { useChat } from "../hooks/useChat";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { ChatStats } from "./ChatStats";

export const ChatInterface: React.FC = () => {
  const [inputValue, setInputValue] = useState("");
  const [isComposing, setIsComposing] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const {
    messages,
    sendMessage,
    isLoading,
    isConnected,
    checkConnection,
    sessionId,
    clearChat,
    botTypingState,
  } = useChat();

  const getSuggestions = () => {
    const lastBotMessage = messages.filter((m) => m.isBot).slice(-1)[0];
    if (!lastBotMessage) {
      return [
        "Buscar laptops gaming",
        "Ver ofertas del día",
        "Soporte técnico",
        "Información de garantía",
      ];
    }

    const text = lastBotMessage.text.toLowerCase();
    if (text.includes("laptop") || text.includes("producto")) {
      return [
        "¿Cuál es el mejor precio?",
        "¿Tienen garantía?",
        "Especificaciones técnicas",
        "¿Está disponible?",
      ];
    }

    return [
      "Necesito más información",
      "¿Tienen otros modelos?",
      "¿Cuándo llega el envío?",
      "Hablar con un agente",
    ];
  };

  const suggestions = getSuggestions();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      sendMessage(inputValue);
      setInputValue("");
      setShowSuggestions(false);
    }
  };

  const handleQuickReply = (message: string) => {
    if (!isLoading) {
      sendMessage(message);
    }
  };

  const handleRegenerateResponse = (messageId: string) => {
    const messageIndex = messages.findIndex((m) => m.id === messageId);
    if (messageIndex > 0) {
      const userMessage = messages[messageIndex - 1];
      if (!userMessage.isBot) {
        sendMessage(userMessage.text);
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey && !isComposing) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
    setShowSuggestions(e.target.value.length === 0);
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInputValue(suggestion);
    setShowSuggestions(false);
    inputRef.current?.focus();
  };

  return (
    <div
      className="flex flex-col h-full"
      style={{
        background: "linear-gradient(to bottom right, #002855, #001F3F)",
        color: "#f8fafc",
      }}
    >
      {/* Mensaje de bienvenida */}
      {messages.length === 0 && (
        <div className="p-4 text-center">
          <div className="bg-yellow-100 border border-yellow-300 rounded-lg p-4 mx-auto max-w-sm text-gray-900 shadow-md">
            <div className="w-10 h-10 bg-[#003f7f] rounded-full flex items-center justify-center mx-auto mb-3">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-base font-semibold">¡Hola! Soy InfoBot</h3>
            <p className="text-xs text-gray-700 mb-3">
              Tu asistente virtual de GRUPO INFOTEC. Puedo ayudarte con
              información sobre productos, servicios técnicos, precios y más.
              <br />
              <span className="text-gray-500">Sesión: {sessionId.slice(-8)}</span>
            </p>
            <div className="flex items-center justify-center space-x-3 text-xs">
              {isConnected ? (
                <div className="flex items-center text-green-600">
                  <Wifi className="w-3 h-3 mr-1" />
                  <span>Conectado</span>
                </div>
              ) : (
                <div className="flex items-center text-red-500">
                  <WifiOff className="w-3 h-3 mr-1" />
                  <span>Desconectado</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Mensajes */}
      <div className="flex-1 overflow-hidden px-4 py-2">
        <div className="h-full overflow-y-auto scroll-smooth">
          <div className="space-y-1">
            {messages.map((message) => (
              <MessageBubble
                key={message.id}
                message={message}
                onSendQuickReply={handleQuickReply}
                onRegenerateResponse={handleRegenerateResponse}
              />
            ))}
            {botTypingState !== "idle" && (
              <TypingIndicator state={botTypingState} />
            )}
          </div>
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="bg-[#003f7f] p-3 border-t border-blue-900">
        {showSuggestions && !isLoading && (
          <div className="mb-3 flex flex-wrap gap-2">
            <span className="text-xs text-white w-full">Sugerencias:</span>
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                className="px-3 py-1 text-xs bg-[#FFD100] hover:bg-yellow-400 text-black rounded-full shadow-sm transition"
              >
                {suggestion}
              </button>
            ))}
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <button
            type="button"
            onClick={clearChat}
            className="w-10 h-10 text-white hover:text-red-400 rounded-full hover:bg-[#002855] transition flex items-center justify-center"
            title="Vaciar chat"
          >
            <Trash2 className="w-5 h-5" />
          </button>

          <div className="flex-1 relative">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              onCompositionStart={() => setIsComposing(true)}
              onCompositionEnd={() => setIsComposing(false)}
              onFocus={() => setShowSuggestions(inputValue.length === 0)}
              onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
              placeholder={
                isConnected
                  ? "Escribe un mensaje..."
                  : "Verificando conexión..."
              }
              disabled={!isConnected || isLoading}
              maxLength={1000}
              className="w-full px-4 py-3 pr-20 bg-white text-gray-800 border border-gray-300 rounded-full shadow-sm focus:ring-2 focus:ring-[#FFD100] focus:outline-none text-sm"
            />
            <div className="absolute right-4 top-1/2 transform -translate-y-1/2 flex items-center space-x-2">
              <div
                className={`text-xs ${
                  inputValue.length > 800 ? "text-red-500" : "text-gray-400"
                }`}
              >
                {inputValue.length}/1000
              </div>
              <button
                type="button"
                title="Emojis"
                className="text-gray-400 hover:text-gray-600"
              >
                <Smile className="w-4 h-4" />
              </button>
            </div>
          </div>

          {inputValue.trim() ? (
            <button
              type="submit"
              disabled={!isConnected || isLoading}
              className="w-12 h-12 bg-[#FFD100] text-[#002855] hover:bg-yellow-400 rounded-full shadow-md transition flex items-center justify-center"
              title="Enviar"
            >
              <Send className="w-5 h-5" />
            </button>
          ) : (
            <button
              type="button"
              className="w-12 h-12 bg-gray-500 text-white rounded-full hover:bg-gray-600 transition flex items-center justify-center"
              title="Mensaje de voz"
            >
              <Mic className="w-5 h-5" />
            </button>
          )}
        </form>

        {!isConnected && (
          <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded-lg text-xs text-red-700">
            No se puede conectar al servidor.
            <button
              onClick={() => checkConnection()}
              className="ml-2 text-red-600 underline hover:text-red-800"
            >
              Reintentar
            </button>
          </div>
        )}
      </div>

      <ChatStats
        messages={messages}
        sessionId={sessionId}
        isConnected={isConnected}
      />
    </div>
  );
};
