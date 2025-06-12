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
  MessageCircle,
  Zap,
  Shield,
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
    <div className="flex flex-col h-full bg-gradient-to-br from-slate-50 via-white to-slate-100">
      {/* Header del Chat */}
      <div className="bg-gradient-to-r from-[#002855] via-[#003f7f] to-[#001F3F] shadow-lg">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-[#F36A21] rounded-full flex items-center justify-center shadow-lg">
                <Bot className="w-6 h-6 text-[#002855]" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">InfoBot Assistant</h1>
                <div className="flex items-center space-x-3 text-sm">
                  {isConnected ? (
                    <div className="flex items-center text-[#F36A21]">
                      <div className="w-2 h-2 bg-[#F36A21] rounded-full mr-2 animate-pulse"></div>
                      <Wifi className="w-4 h-4 mr-1" />
                      <span>En línea</span>
                    </div>

                  ) : (
                    <div className="flex items-center text-red-300">
                      <div className="w-2 h-2 bg-red-400 rounded-full mr-2"></div>
                      <WifiOff className="w-4 h-4 mr-1" />
                      <span>Desconectado</span>
                    </div>
                  )}
                  <div className="text-blue-200 text-xs">
                    ID: {sessionId.slice(-8)}
                  </div>
                </div>
              </div>
            </div>

            <button
              onClick={clearChat}
              className="flex items-center space-x-2 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-200 hover:text-red-100 rounded-lg transition-all duration-200 group"
              title="Limpiar conversación"
            >
              <Trash2 className="w-4 h-4 group-hover:scale-110 transition-transform" />
              <span className="text-sm font-medium">Limpiar</span>
            </button>
          </div>
        </div>
      </div>

      {/* Mensaje de bienvenida mejorado */}
      {messages.length === 0 && (
        <div className="p-8">
          <div className="max-w-2xl mx-auto">
            <div className="bg-white rounded-3xl shadow-xl p-8 border border-gray-100">
              <div className="text-center mb-8">
                <div className="w-20 h-20 bg-gradient-to-br from-[#003f7f] to-[#002855] rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <Bot className="w-10 h-10 text-white" />
                </div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2">¡Hola! Soy InfoBot</h2>
                <p className="text-lg text-gray-600 mb-6">
                  Tu asistente virtual de <span className="font-semibold text-[#003f7f]">GRUPO INFOTEC</span>
                </p>
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-100">
                  <p className="text-gray-700 leading-relaxed">
                    Puedo ayudarte con información sobre productos, servicios técnicos,
                    precios, garantías y mucho más. ¡Pregúntame lo que necesites!
                  </p>
                </div>
              </div>

              {/* Características destacadas */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="text-center p-4 bg-green-50 rounded-xl border border-green-100">
                  <Zap className="w-8 h-8 text-green-500 mx-auto mb-2" />
                  <p className="text-sm font-medium text-green-700">Respuestas rápidas</p>
                </div>
                <div className="text-center p-4 bg-blue-50 rounded-xl border border-blue-100">
                  <MessageCircle className="w-8 h-8 text-blue-500 mx-auto mb-2" />
                  <p className="text-sm font-medium text-blue-700">Soporte 24/7</p>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-xl border border-purple-100">
                  <Shield className="w-8 h-8 text-purple-500 mx-auto mb-2" />
                  <p className="text-sm font-medium text-purple-700">100% Seguro</p>
                </div>
              </div>

              {/* Sugerencias iniciales */}
              <div className="space-y-3">
                <p className="text-sm font-medium text-gray-500 text-center">Puedes empezar preguntando:</p>
                <div className="flex flex-wrap justify-center gap-2">
                  {suggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => handleSuggestionClick(suggestion)}
                      className="px-4 py-2 bg-[#F36A21] text-[#002855] text-sm font-medium rounded-full shadow-sm hover:shadow-md transition-all duration-200 hover:scale-105"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Área de mensajes mejorada */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full px-6 py-4">
          <div className="h-full overflow-y-auto scroll-smooth">
            <div className="space-y-6 pb-4">
              {messages.map((message, index) => (
                <div key={message.id} className="animate-fade-in">
                  <MessageBubble
                    message={message}
                    onSendQuickReply={handleQuickReply}
                    onRegenerateResponse={handleRegenerateResponse}
                  />
                  {/* Separador entre mensajes */}
                  {index < messages.length - 1 && (
                    <div className="my-4 border-t border-gray-100"></div>
                  )}
                </div>
              ))}
              {botTypingState !== "idle" && (
                <div className="animate-fade-in">
                  <TypingIndicator state={botTypingState} />
                </div>
              )}
            </div>
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>

      {/* Área de input mejorada */}
      <div className="bg-white border-t border-gray-200 shadow-lg">
        <div className="px-6 py-4">
          {/* Sugerencias dinámicas */}
          {showSuggestions && !isLoading && messages.length > 0 && (
            <div className="mb-4 p-4 bg-gray-50 rounded-2xl border border-gray-100">
              <div className="flex items-center mb-3">
                <Zap className="w-4 h-4 text-[#FFD100] mr-2" />
                <span className="text-sm font-medium text-gray-700">Respuestas rápidas:</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {suggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => handleSuggestionClick(suggestion)}
                    className="px-3 py-2 text-sm bg-white hover:bg-[#FFD100] hover:text-[#002855] text-gray-600 border border-gray-200 rounded-full shadow-sm transition-all duration-200 hover:shadow-md hover:scale-105"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input principal */}
          <form onSubmit={handleSubmit} className="space-y-3">
            <div className="flex items-end space-x-3">
              {/* Input de texto */}
              <div className="flex-1 relative">
                <div className="relative bg-gray-50 rounded-2xl border-2 border-gray-200 hover:border-gray-300 focus-within:border-[#FFD100] transition-colors duration-200">
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
                        ? "Escribe tu mensaje aquí..."
                        : "Verificando conexión..."
                    }
                    disabled={!isConnected || isLoading}
                    maxLength={1000}
                    className="w-full px-6 py-4 pr-24 bg-transparent text-gray-800 placeholder-gray-500 focus:outline-none text-base resize-none"
                  />

                  {/* Controles del input */}
                  <div className="absolute right-4 top-1/2 transform -translate-y-1/2 flex items-center space-x-3">
                    <div className="flex items-center space-x-2">
                      <div
                        className={`text-xs font-medium ${inputValue.length > 800 ? "text-red-500" : "text-gray-400"
                          }`}
                      >
                        {inputValue.length}/1000
                      </div>
                      <button
                        type="button"
                        title="Adjuntar archivo"
                        className="text-gray-400 hover:text-gray-600 transition-colors duration-200"
                      >
                        <Paperclip className="w-5 h-5" />
                      </button>
                      <button
                        type="button"
                        title="Emojis"
                        className="text-gray-400 hover:text-gray-600 transition-colors duration-200"
                      >
                        <Smile className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              {/* Botones de acción */}
              <div className="flex space-x-2">
                {inputValue.trim() ? (
                  <button
                    type="submit"
                    disabled={!isConnected || isLoading}
                    className="w-14 h-14 bg-gradient-to-r from-[#FFD100] to-yellow-400 text-[#002855] hover:from-yellow-400 hover:to-[#FFD100] rounded-2xl shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed hover:scale-105 group"
                    title="Enviar mensaje"
                  >
                    <Send className="w-6 h-6 group-hover:translate-x-0.5 transition-transform duration-200" />
                  </button>
                ) : (
                  <button
                    type="button"
                    className="w-14 h-14 bg-gradient-to-r from-gray-400 to-gray-500 text-white rounded-2xl hover:from-gray-500 hover:to-gray-600 shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center hover:scale-105 group"
                    title="Mensaje de voz"
                  >
                    <Mic className="w-6 h-6 group-hover:scale-110 transition-transform duration-200" />
                  </button>
                )}
              </div>
            </div>

            {/* Estado de conexión */}
            {!isConnected && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-sm">
                <div className="flex items-center justify-between">
                  <div className="flex items-center text-red-700">
                    <WifiOff className="w-4 h-4 mr-2" />
                    <span>No se puede conectar al servidor</span>
                  </div>
                  <button
                    onClick={() => checkConnection()}
                    className="px-3 py-1 bg-red-100 hover:bg-red-200 text-red-700 rounded-lg font-medium transition-colors duration-200"
                  >
                    Reintentar
                  </button>
                </div>
              </div>
            )}
          </form>
        </div>
      </div>

      {/* Estadísticas del chat */}
      <div className="bg-gray-50 border-t border-gray-100">
        <ChatStats
          messages={messages}
          sessionId={sessionId}
          isConnected={isConnected}
        />
      </div>
    </div>
  );
};