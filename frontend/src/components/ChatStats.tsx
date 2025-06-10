import React from 'react';
import { MessageCircle, Clock, Zap, CheckCircle } from 'lucide-react';
import { ChatMessage } from '../hooks/useChat';

interface ChatStatsProps {
  messages: ChatMessage[];
  sessionId: string;
  isConnected: boolean;
}

export const ChatStats: React.FC<ChatStatsProps> = ({ messages, sessionId, isConnected }) => {
  const userMessages = messages.filter(m => !m.isBot);
  const botMessages = messages.filter(m => m.isBot && !m.isLoading);
  const avgResponseTime = '< 2s'; // Esto podría calcularse realmente
  
  const getSessionDuration = () => {
    if (messages.length < 2) return '0m';
    const firstMessage = messages[0];
    const lastMessage = messages[messages.length - 1];
    const diffMs = lastMessage.timestamp.getTime() - firstMessage.timestamp.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    return `${diffMins}m`;
  };

  return (
    <div className="bg-gray-50 border-t border-gray-200 p-3">
      <div className="flex items-center justify-between text-xs text-gray-600">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-1">
            <MessageCircle className="w-3 h-3" />
            <span>{userMessages.length} mensajes</span>
          </div>
          
          <div className="flex items-center space-x-1">
            <Clock className="w-3 h-3" />
            <span>{getSessionDuration()}</span>
          </div>
          
          <div className="flex items-center space-x-1">
            <Zap className="w-3 h-3" />
            <span>Resp: {avgResponseTime}</span>
          </div>
        </div>
        
        <div className="flex items-center space-x-1">
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
          <span className="text-xs">
            {isConnected ? 'En línea' : 'Desconectado'}
          </span>
        </div>
      </div>
      
      <div className="mt-1 text-xs text-gray-500">
        ID de sesión: {sessionId.slice(-12)}
      </div>
    </div>
  );
};
