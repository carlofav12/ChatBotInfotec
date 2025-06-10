import React, { useState, useEffect } from "react";
import { Minimize2, Phone, Video, Bot, Settings } from "lucide-react";
import { ChatInterface } from "./ChatInterface";
import { ChatSettingsPanel, ChatSettings } from "./ChatSettingsPanel";
import { useChat } from "../hooks/useChat";

export const FloatingChatbot: React.FC = () => {
  // Obtener el número de mensajes para detectar nuevos mensajes
  const { messages } = useChat();

  // Cargar estado minimizado desde localStorage
  const [isMinimized, setIsMinimized] = useState(() => {
    const savedState = localStorage.getItem("chatbot_minimized");
    return savedState ? JSON.parse(savedState) : true; // Por defecto minimizado
  });
  const [showWelcome, setShowWelcome] = useState(true);
  const [showSettings, setShowSettings] = useState(false);

  // Cargar configuraciones del chat desde localStorage
  const [chatSettings, setChatSettings] = useState<ChatSettings>(() => {
    const savedSettings = localStorage.getItem("chat_settings");
    return savedSettings
      ? JSON.parse(savedSettings)
      : {
          soundEnabled: true,
          notificationsEnabled: true,
          theme: "auto",
          fontSize: "medium",
          autoScroll: true,
          showTypingIndicator: true,
        };
  });

  // Estado para tracking de mensajes no leídos
  const [unreadCount, setUnreadCount] = useState(0);
  const [lastReadMessageId, setLastReadMessageId] = useState<string | null>(
    null
  );

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowWelcome(false);
    }, 5000);
    return () => clearTimeout(timer);
  }, []);

  // Guardar estado minimizado en localStorage
  useEffect(() => {
    localStorage.setItem("chatbot_minimized", JSON.stringify(isMinimized));
  }, [isMinimized]);

  const toggleMinimize = () => {
    setIsMinimized(!isMinimized);
    setShowWelcome(false);
  };
  const handleSettingsChange = (settings: ChatSettings) => {
    setChatSettings(settings);
    // Guardar configuraciones en localStorage
    localStorage.setItem("chat_settings", JSON.stringify(settings));
  };

  // Aplicar configuraciones del chat (para futuras mejoras)
  useEffect(() => {
    // Aquí se pueden aplicar las configuraciones como tema, tamaño de fuente, etc.
    console.log("Chat settings updated:", chatSettings);
  }, [chatSettings]);

  // Actualizar contador de mensajes no leídos
  useEffect(() => {
    if (!isMinimized) {
      setUnreadCount(0);
      setLastReadMessageId(messages[messages.length - 1]?.id || null);
    } else {
      // Contar mensajes no leídos
      const count = messages.filter(
        (msg) => msg.id !== lastReadMessageId
      ).length;
      setUnreadCount(count);
    }
  }, [messages, isMinimized, lastReadMessageId]);

  // Determinar clases para tema y fuente
  const themeClass =
    chatSettings.theme === "dark"
      ? "chatbot-dark"
      : chatSettings.theme === "light"
      ? "chatbot-light"
      : "";
  let fontSizeClass = "";
  if (chatSettings.fontSize === "small") fontSizeClass = "chatbot-font-small";
  else if (chatSettings.fontSize === "large")
    fontSizeClass = "chatbot-font-large";

  return (
    <div
      className={`fixed right-4 bottom-4 z-50 ${themeClass} ${fontSizeClass}`}
    >
      {/* Welcome Message - WhatsApp Style */}
      {showWelcome && !isMinimized && (
        <div className="absolute bottom-full right-0 mb-4 bg-white rounded-lg shadow-lg border border-gray-200 p-3 max-w-64 animate-bounce">
          <div className="flex items-start space-x-2">
            <div className="w-8 h-8 bg-[var(--infotec-orange)] rounded-full flex items-center justify-center flex-shrink-0">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-800">
                InfoBot GRUPO INFOTEC
              </p>
              <p className="text-xs text-gray-600 mt-1">
                ¡Hola! ¿En qué puedo ayudarte hoy?
              </p>
            </div>
          </div>
          <div className="absolute top-full right-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-white"></div>
        </div>
      )}

      {/* Minimized State - Round Robot Icon */}
      {isMinimized && (
        <div className="relative">
          <button
            onClick={toggleMinimize}
            className="w-16 h-16 bg-[var(--infotec-orange)] hover:bg-[var(--infotec-orange-dark)] rounded-full shadow-lg flex items-center justify-center transition-all duration-300 hover:scale-105"
            aria-label="Abrir chat"
          >
            <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
              <Bot className="w-4 h-4 text-[var(--infotec-orange)]" />
            </div>
          </button>
          {/* Online Status Indicator */}
          <div className="absolute top-1 right-1 w-4 h-4 bg-[var(--infotec-orange)] rounded-full border-2 border-white animate-pulse"></div>
          {/* Unread Messages Indicator */}
          {unreadCount > 0 && (
            <div className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
              {unreadCount}
            </div>
          )}
        </div>
      )}

      {/* WhatsApp-Style Chat Widget - Expanded State */}
      {!isMinimized && (
        <div className="w-96 h-[600px] bg-white rounded-lg shadow-2xl border border-gray-200 flex flex-col overflow-hidden transition-all duration-300">
          {/* WhatsApp-Style Header */}
          <div className="bg-[var(--infotec-orange)] text-white px-4 py-3 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              {/* Profile Picture */}
              <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
                <div className="w-8 h-8 bg-[var(--infotec-orange)] rounded-full flex items-center justify-center">
                  <Bot className="w-4 h-4 text-white" />
                </div>
              </div>

              <div className="flex-1">
                <h3 className="font-medium text-sm">InfoBot GRUPO INFOTEC</h3>
                <p className="text-xs opacity-90">En línea</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setShowSettings(!showSettings)}
                className="p-2 hover:bg-green-700 rounded-full transition-colors"
                title="Configuración"
              >
                <Settings className="w-4 h-4" />
              </button>
              <button
                onClick={toggleMinimize}
                className="p-1 hover:bg-green-700 rounded transition-colors ml-2"
                aria-label="Minimizar chat"
              >
                <Minimize2 className="w-4 h-4" />
              </button>
            </div>
          </div>{" "}
          {/* Chat Content */}{" "}
          <div className="flex-1 flex flex-col overflow-hidden relative">
            {showSettings ? (
              <ChatSettingsPanel
                isOpen={showSettings}
                onClose={() => setShowSettings(false)}
                onSettingsChange={handleSettingsChange}
              />
            ) : (
              <ChatInterface />
            )}
          </div>
        </div>
      )}
    </div>
  );
};
