import React, { useState, useEffect } from 'react';
import { Minimize2, Phone, Video, MoreVertical, Bot, Settings } from 'lucide-react';
import { ChatInterface } from './ChatInterface';
import { ChatSettingsPanel, ChatSettings } from './ChatSettingsPanel';

export const FloatingChatbot: React.FC = () => {
  const [isMinimized, setIsMinimized] = useState(false);
  const [showWelcome, setShowWelcome] = useState(true);
  const [showSettings, setShowSettings] = useState(false);
  const [chatSettings, setChatSettings] = useState<ChatSettings>({
    soundEnabled: true,
    notificationsEnabled: true,
    theme: 'auto',
    fontSize: 'medium',
    autoScroll: true,
    showTypingIndicator: true
  });

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowWelcome(false);
    }, 5000);
    return () => clearTimeout(timer);
  }, []);

  const toggleMinimize = () => {
    setIsMinimized(!isMinimized);
    setShowWelcome(false);
  };

  const handleSettingsChange = (settings: ChatSettings) => {
    setChatSettings(settings);
  };return (
    <div className="fixed right-4 bottom-4 z-50">
      {/* Welcome Message - WhatsApp Style */}
      {showWelcome && !isMinimized && (
        <div className="absolute bottom-full right-0 mb-4 bg-white rounded-lg shadow-lg border border-gray-200 p-3 max-w-64 animate-bounce">
          <div className="flex items-start space-x-2">
            <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center flex-shrink-0">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-800">InfoBot GRUPO INFOTEC</p>
              <p className="text-xs text-gray-600 mt-1">¡Hola! ¿En qué puedo ayudarte hoy?</p>
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
            className="w-16 h-16 bg-green-500 hover:bg-green-600 rounded-full shadow-lg flex items-center justify-center transition-all duration-300 hover:scale-105"
            aria-label="Abrir chat"
          >
            <Bot className="w-8 h-8 text-white" />
          </button>
          {/* Online Status Indicator */}
          <div className="absolute top-1 right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-white animate-pulse"></div>
        </div>
      )}

      {/* WhatsApp-Style Chat Widget - Expanded State */}
      {!isMinimized && (
        <div className="w-96 h-[600px] bg-white rounded-lg shadow-2xl border border-gray-200 flex flex-col overflow-hidden transition-all duration-300">
          {/* WhatsApp-Style Header */}
          <div className="bg-green-600 text-white px-4 py-3 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              {/* Profile Picture */}
              <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
                <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
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
              <button className="p-2 hover:bg-green-700 rounded-full transition-colors">
                <Video className="w-4 h-4" />
              </button>
              <button className="p-2 hover:bg-green-700 rounded-full transition-colors">
                <Phone className="w-4 h-4" />
              </button>
              <button className="p-2 hover:bg-green-700 rounded-full transition-colors">
                <MoreVertical className="w-4 h-4" />
              </button>
              <button
                onClick={toggleMinimize}
                className="p-1 hover:bg-green-700 rounded transition-colors ml-2"
                aria-label="Minimizar chat"
              >
                <Minimize2 className="w-4 h-4" />
              </button>
            </div>
          </div>          {/* Chat Content */}
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
