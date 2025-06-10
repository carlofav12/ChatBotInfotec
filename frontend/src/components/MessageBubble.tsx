import React, { useState } from 'react';
import { Bot, ThumbsUp, ThumbsDown, Copy, RotateCcw } from 'lucide-react';
import { ChatMessage } from '../hooks/useChat';
import ProductCarousel from './ProductCarousel';

interface MessageBubbleProps {
  message: ChatMessage;
  onSendQuickReply?: (message: string) => void;
  onRegenerateResponse?: (messageId: string) => void;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ 
  message, 
  onSendQuickReply,
  onRegenerateResponse 
}) => {
  const [showActions, setShowActions] = useState(false);
  const [copied, setCopied] = useState(false);

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Error al copiar:', err);
    }
  };

  const getQuickReplies = () => {
    if (!message.isBot || message.isLoading) return [];
    
    const lowerText = message.text.toLowerCase();
    
    if (lowerText.includes('producto') || lowerText.includes('laptop') || lowerText.includes('computadora')) {
      return [
        "Mostrar más opciones",
        "¿Cuál recomiendas?",
        "Ver especificaciones",
        "Precios y ofertas"
      ];
    } else if (lowerText.includes('ayuda') || lowerText.includes('soporte')) {
      return [
        "Contactar soporte",
        "Ver horarios",
        "Preguntas frecuentes"
      ];
    } else if (lowerText.includes('hola') || lowerText.includes('infobot')) {
      return [
        "Ver productos",
        "Necesito ayuda",
        "Información de la empresa",
        "Servicios técnicos"
      ];
    }
    
    return [];
  };

  const quickReplies = getQuickReplies();

  return (
    <div
      className={`flex w-full mb-2 ${
        message.isBot ? 'justify-start' : 'justify-end'
      }`}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      <div
        className={`flex max-w-[80%] ${
          message.isBot ? 'flex-row' : 'flex-row-reverse'
        }`}
      >
        {/* Avatar - only for bot messages */}
        {message.isBot && (
          <div className="flex-shrink-0 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center mr-2 mt-1">
            <Bot size={16} className="text-white" />
          </div>
        )}

        {/* Message Content */}
        <div className="flex flex-col">
          <div className="relative group">
            <div
              className={`px-3 py-2 rounded-lg shadow-sm ${
                message.isBot
                  ? 'bg-white text-gray-800 border border-gray-200'
                  : 'bg-green-500 text-white'
              } ${message.isLoading ? 'animate-pulse' : ''}`}
              style={{
                borderRadius: message.isBot 
                  ? '18px 18px 18px 4px' 
                  : '18px 18px 4px 18px'
              }}
            >
              {message.isLoading ? (
                <div className="flex items-center space-x-2">
                  {/* Indicador visual basado en el tipo de acción */}
                  {message.typingState === 'thinking' ? (
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" />
                      <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse delay-150" />
                      <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse delay-300" />
                    </div>
                  ) : message.typingState === 'searching' ? (
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-orange-400 rounded-full animate-spin" />
                      <div className="w-2 h-2 bg-orange-400 rounded-full animate-ping delay-100" />
                      <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce delay-200" />
                    </div>
                  ) : (
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-green-400 rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-green-400 rounded-full animate-bounce delay-100" />
                      <div className="w-2 h-2 bg-green-400 rounded-full animate-bounce delay-200" />
                    </div>
                  )}
                  <span className="ml-2 text-sm text-gray-600">
                    {message.text}
                  </span>
                </div>
              ) : (
                <div>
                  <p className="text-sm leading-relaxed whitespace-pre-wrap">
                    {message.text}
                  </p>
                  
                  {/* Mostrar productos si existen */}
                  {message.products && message.products.length > 0 && (
                    <div className="mt-2">
                      <ProductCarousel products={message.products} />
                    </div>
                  )}
                  
                  {/* Timestamp inside bubble */}
                  <div
                    className={`text-xs mt-1 ${
                      message.isBot ? 'text-gray-500' : 'text-green-100'
                    } flex justify-end`}
                  >
                    {formatTime(message.timestamp)}
                    {!message.isBot && (
                      <span className="ml-1">✓✓</span>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Message Actions (visible on hover) */}
            {message.isBot && !message.isLoading && showActions && (
              <div className="absolute left-full ml-2 top-0 flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  onClick={handleCopy}
                  className="p-1 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100 transition-colors"
                  title="Copiar mensaje"
                >
                  <Copy size={14} />
                </button>
                <button
                  onClick={() => onRegenerateResponse?.(message.id)}
                  className="p-1 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100 transition-colors"
                  title="Regenerar respuesta"
                >
                  <RotateCcw size={14} />
                </button>
              </div>
            )}
          </div>

          {/* Quick Reply Buttons */}
          {quickReplies.length > 0 && !message.isLoading && (
            <div className="mt-2 flex flex-wrap gap-2">
              {quickReplies.map((reply, index) => (
                <button
                  key={index}
                  onClick={() => onSendQuickReply?.(reply)}
                  className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full border border-gray-300 transition-colors duration-200 hover:shadow-sm"
                >
                  {reply}
                </button>
              ))}
            </div>
          )}

          {/* Copy feedback */}
          {copied && (
            <div className="mt-1 text-xs text-green-600 animate-fade-in">
              ✓ Copiado
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
