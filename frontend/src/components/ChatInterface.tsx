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

  // Sugerencias inteligentes basadas en el contexto
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

  // Auto-scroll al final cuando hay nuevos mensajes
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Enfocar input al cargar
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
    // Buscar el mensaje anterior del usuario para regenerar
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
      className="flex flex-col h-full bg-gray-100"
      style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23e5e7eb' fill-opacity='0.3' fill-rule='evenodd'%3E%3Cpath d='m0 40l40-40h-40z'/%3E%3Cpath d='m40 40v-40h-40z' fill='%23f3f4f6'/%3E%3C/g%3E%3C/svg%3E")`,
      }}
    >
      {" "}
      {/* Welcome message for first time users - WhatsApp Style */}
      {messages.length === 0 && (
        <div className="p-4 text-center">
          <div className="bg-yellow-100 border border-yellow-200 rounded-lg p-4 mx-auto max-w-sm">
            <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-base font-semibold text-gray-800 mb-2">
              ¡Hola! Soy InfoBot
            </h3>{" "}
            <p className="text-xs text-gray-600 mb-3">
              Tu asistente virtual de GRUPO INFOTEC. Puedo ayudarte con
              información sobre productos, servicios técnicos, precios y más.
              <br />
              <span className="text-gray-500 text-xs">
                Sesión: {sessionId.slice(-8)}
              </span>
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
      {/* Área de mensajes */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full px-4 py-2">
          <div className="h-full overflow-y-auto scroll-smooth">
            {" "}
            <div className="space-y-1">
              {messages.map((message) => (
                <MessageBubble
                  key={message.id}
                  message={message}
                  onSendQuickReply={handleQuickReply}
                  onRegenerateResponse={handleRegenerateResponse}
                />
              ))}

              {/* Indicador de escritura cuando el bot está activo */}
              {botTypingState !== "idle" && (
                <TypingIndicator state={botTypingState} />
              )}
            </div>
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>{" "}
      {/* Área de input - WhatsApp Style Mejorada */}
      <div className="bg-gray-200 border-t border-gray-300 p-3">
        {/* Sugerencias rápidas */}
        {showSuggestions && !isLoading && (
          <div className="mb-3 flex flex-wrap gap-2">
            <span className="text-xs text-gray-600 mb-1 w-full">
              Sugerencias:
            </span>
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                className="px-3 py-1 text-xs bg-white hover:bg-blue-50 text-gray-700 rounded-full border border-gray-300 transition-colors duration-200 hover:border-blue-300"
              >
                {suggestion}
              </button>
            ))}
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          {/* Botón vaciar chat */}
          <button
            type="button"
            className="w-10 h-10 text-gray-500 hover:text-red-600 rounded-full hover:bg-gray-200 transition-colors flex items-center justify-center"
            title="Vaciar chat"
            onClick={clearChat}
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
              className="w-full px-4 py-3 pr-16 bg-white border border-gray-300 rounded-full focus:ring-2 focus:ring-green-500 focus:border-transparent text-sm disabled:bg-gray-100 disabled:cursor-not-allowed shadow-sm transition-all duration-200"
              maxLength={1000}
            />

            {/* Indicadores del input */}
            <div className="absolute right-4 top-1/2 transform -translate-y-1/2 flex items-center space-x-2">
              {/* Contador de caracteres */}
              <div
                className={`text-xs ${
                  inputValue.length > 800 ? "text-red-500" : "text-gray-400"
                }`}
              >
                {inputValue.length}/1000
              </div>

              {/* Emoji button */}
              <button
                type="button"
                className="text-gray-400 hover:text-gray-600 transition-colors"
                title="Emojis"
              >
                <Smile className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Botón de voz o envío */}
          {inputValue.trim() ? (
            <button
              type="submit"
              disabled={!inputValue.trim() || isLoading || !isConnected}
              className="w-12 h-12 bg-green-500 text-white rounded-full hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center shadow-sm"
            >
              <Send className="w-5 h-5" />
            </button>
          ) : (
            <button
              type="button"
              className="w-12 h-12 bg-gray-500 text-white rounded-full hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-all duration-200 flex items-center justify-center shadow-sm"
              title="Mensaje de voz"
            >
              <Mic className="w-5 h-5" />
            </button>
          )}
        </form>

        {/* Mensaje de estado */}
        {!isConnected && (
          <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center justify-between">
              <p className="text-xs text-red-700">
                No se puede conectar al servidor.
              </p>
              <button
                onClick={() => checkConnection()}
                className="text-xs text-red-600 hover:text-red-800 underline"
              >
                Reintentar
              </button>
            </div>
          </div>
        )}
      </div>
      {/* Estadísticas de la conversación */}
      <ChatStats
        messages={messages}
        sessionId={sessionId}
        isConnected={isConnected}
      />
    </div>
  );
};
