import React from 'react';
import { Bot, Search, Brain, Edit3 } from 'lucide-react';

interface TypingIndicatorProps {
  state: 'idle' | 'thinking' | 'typing' | 'searching';
  message?: string;
}

export const TypingIndicator: React.FC<TypingIndicatorProps> = ({ state, message }) => {
  if (state === 'idle') return null;

  const getIcon = () => {
    switch (state) {
      case 'thinking':
        return <Brain className="w-4 h-4 text-blue-500" />;
      case 'searching':
        return <Search className="w-4 h-4 text-orange-500" />;
      case 'typing':
        return <Edit3 className="w-4 h-4 text-green-500" />;
      default:
        return <Bot className="w-4 h-4 text-gray-500" />;
    }
  };

  const getAnimation = () => {
    switch (state) {
      case 'thinking':
        return 'animate-pulse';
      case 'searching':
        return 'animate-spin';
      case 'typing':
        return 'animate-bounce';
      default:
        return '';
    }
  };

  const getMessage = () => {
    if (message) return message;
    
    switch (state) {
      case 'thinking':
        return 'InfoBot está analizando tu mensaje...';
      case 'searching':
        return 'InfoBot está buscando productos...';
      case 'typing':
        return 'InfoBot está escribiendo una respuesta...';
      default:
        return 'InfoBot está procesando...';
    }
  };

  return (
    <div className="flex items-center space-x-2 text-sm text-gray-600 p-2">
      <div className={`${getAnimation()}`}>
        {getIcon()}
      </div>
      <span>{getMessage()}</span>
      <div className="flex space-x-1">
        <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" />
        <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce delay-100" />
        <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce delay-200" />
      </div>
    </div>
  );
};
