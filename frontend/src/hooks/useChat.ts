import { useState, useCallback, useEffect } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { apiService, ChatResponse } from '../services/api';

interface Product {
  id: number;
  name: string;
  price: number;
  original_price?: number;
  image_url: string;
  rating: number;
  stock_quantity: number;
  brand: string;
  description?: string;
}

export interface ChatMessage {
  id: string;
  text: string;
  isBot: boolean;
  timestamp: Date;
  isLoading?: boolean;
  typingState?: 'typing' | 'thinking' | 'searching';
  products?: Product[];
  intent?: string;
}

export const useChat = () => {
  // Generar un ID de sesión si no existe
  const [sessionId] = useState<string>(() => {
    const existingSessionId = localStorage.getItem('chat_session_id');
    if (existingSessionId) {
      return existingSessionId;
    }
    const newSessionId = `session_${Date.now()}`;
    localStorage.setItem('chat_session_id', newSessionId);
    return newSessionId;
  });
  
  // Estado para seguimiento de contexto
  const [currentPage, setCurrentPage] = useState<string>('home');
  const [currentProductId, setCurrentProductId] = useState<number | undefined>(undefined);
  const [contextData, setContextData] = useState<Record<string, any>>({});
  
  // Cargar mensajes desde localStorage o usar mensaje inicial
  const [messages, setMessages] = useState<ChatMessage[]>(() => {
    const savedMessages = localStorage.getItem(`chat_messages_${sessionId}`);
    if (savedMessages) {
      try {
        const parsedMessages = JSON.parse(savedMessages);
        // Convertir las fechas de string a Date objects
        return parsedMessages.map((msg: any) => ({
          ...msg,
          timestamp: new Date(msg.timestamp)
        }));
      } catch (error) {
        console.error('Error parsing saved messages:', error);
      }
    }
    
    // Mensaje inicial si no hay mensajes guardados
    return [
      {
        id: '1',
        text: '¡Hola! Soy InfoBot, tu asistente virtual de GRUPO INFOTEC. ¿En qué puedo ayudarte hoy? Puedo brindarte información sobre nuestros productos, servicios técnicos y soporte. 🤖💻',
        isBot: true,
        timestamp: new Date(),
      },
    ];
  });
  // Nuevo estado para manejar la escritura del bot
  const [botTypingState, setBotTypingState] = useState<'idle' | 'thinking' | 'typing' | 'searching'>('idle');
    // Nuevo estado para métricas de conversación
  const [conversationMetrics, setConversationMetrics] = useState({
    totalMessages: 0,
    averageResponseTime: 0,
    lastActivity: new Date(),
    sessionStartTime: new Date()
  });

  // Efecto para guardar mensajes en localStorage automáticamente
  useEffect(() => {
    localStorage.setItem(`chat_messages_${sessionId}`, JSON.stringify(messages));
  }, [messages, sessionId]);

  // Mutation para enviar mensajes
  const sendMessageMutation = useMutation({
    mutationFn: (userMessageText: string) => apiService.sendMessage(
      userMessageText,
      sessionId,
      currentPage,
      currentProductId,
      contextData
    ),
    onSuccess: (response: ChatResponse, userMessage: string) => {
      // Remover mensaje de carga y agregar respuesta del bot
      setMessages(prev => {
        const withoutLoading = prev.filter(msg => !msg.isLoading);
        return [
          ...withoutLoading,
          {
            id: Date.now().toString(),
            text: response.response,
            isBot: true,
            timestamp: new Date(response.timestamp),
            products: response.products,
            intent: response.intent
          },
        ];
      });
      
      // Actualizar contexto con los productos mencionados
      if (response.products && response.products.length > 0) {
        setContextData(prev => ({
          ...prev,
          products: response.products,
          lastIntent: response.intent,
          lastEntities: response.entities
        }));
      }
    },
    onError: (error: Error) => {
      // Remover mensaje de carga y mostrar error
      setMessages(prev => {
        const withoutLoading = prev.filter(msg => !msg.isLoading);
        return [
          ...withoutLoading,
          {
            id: Date.now().toString(),
            text: 'Lo siento, ocurrió un error. Por favor, verifica que el backend esté ejecutándose e intenta de nuevo.',
            isBot: true,
            timestamp: new Date(),
          },
        ];
      });
    },
  });

  // Query para verificar conexión
  const { data: isConnected, refetch: checkConnection } = useQuery({
    queryKey: ['health-check'],
    queryFn: apiService.healthCheck,
    refetchInterval: 30000, // Verificar cada 30 segundos
    retry: 1,
  });

  // Función para simular escritura realista
  const simulateTyping = useCallback((messageLength: number) => {
    setBotTypingState('thinking');
    
    // Tiempo basado en la longitud del mensaje
    const baseTime = Math.min(messageLength * 50, 3000); // Max 3 segundos
    const thinkingTime = Math.random() * 1000 + 500; // 0.5-1.5 segundos pensando
    
    setTimeout(() => {
      setBotTypingState('typing');
      
      setTimeout(() => {
        setBotTypingState('idle');
      }, baseTime);
    }, thinkingTime);
  }, []);

  // Función para enviar mensaje mejorada
  const sendMessage = useCallback((text: string) => {
    if (!text.trim()) return;

    // Agregar mensaje del usuario
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text: text.trim(),
      isBot: false,
      timestamp: new Date(),
    };

    // Determinar el estado de carga basado en el tipo de mensaje
    let typingState: 'thinking' | 'typing' | 'searching' = 'thinking';
    const lowerText = text.toLowerCase();
    
    if (lowerText.includes('buscar') || lowerText.includes('mostrar') || lowerText.includes('productos')) {
      typingState = 'searching';
    } else if (lowerText.length > 50) {
      typingState = 'thinking';
    } else {
      typingState = 'typing';
    }

    // Agregar mensaje de carga del bot con estado específico
    const loadingMessage: ChatMessage = {
      id: `loading-${Date.now()}`,
      text: getTypingMessage(typingState),
      isBot: true,
      timestamp: new Date(),
      isLoading: true,
      typingState,
    };

    setMessages(prev => [...prev, userMessage, loadingMessage]);
    setBotTypingState(typingState);

    // Simular escritura realista
    simulateTyping(text.length);

    // Enviar al backend
    sendMessageMutation.mutate(text.trim());
  }, [sendMessageMutation, simulateTyping]);  // Función para limpiar chat
  const clearChat = useCallback(() => {
    const initialMessage = {
      id: '1',
      text: '¡Hola! Soy InfoBot, tu asistente virtual de GRUPO INFOTEC. ¿En qué puedo ayudarte hoy? Puedo brindarte información sobre nuestros productos, servicios técnicos y soporte. 🤖💻',
      isBot: true,
      timestamp: new Date(),
    };
    
    setMessages([initialMessage]);
    
    // Limpiar contexto
    setContextData({});
    
    // Limpiar localStorage
    localStorage.removeItem(`chat_messages_${sessionId}`);
    
    // También limpiar en el backend con sessionId específico
    apiService.clearHistory(sessionId).catch(console.error);
  }, [sessionId]);

  // Funciones para actualizar el contexto
  const updateCurrentPage = useCallback((page: string) => {
    setCurrentPage(page);
  }, []);

  const updateCurrentProduct = useCallback((productId: number | undefined) => {
    setCurrentProductId(productId);
    if (productId) {
      // Si hay un producto, actualizamos el contexto
      setContextData(prev => ({
        ...prev,
        lastViewedProductId: productId
      }));
    }
  }, []);

  const updateContextData = useCallback((data: Record<string, any>) => {
    setContextData(prev => ({
      ...prev,
      ...data
    }));
  }, []);

  // Función para actualizar métricas
  const updateMetrics = useCallback(() => {
    const userMessages = messages.filter(m => !m.isBot).length;
    const botMessages = messages.filter(m => m.isBot && !m.isLoading).length;
    
    setConversationMetrics(prev => ({
      ...prev,
      totalMessages: userMessages + botMessages,
      lastActivity: new Date()
    }));
  }, [messages]);

  // Actualizar métricas cuando cambien los mensajes
  useEffect(() => {
    updateMetrics();
  }, [messages, updateMetrics]);

  // Función para obtener resumen de conversación
  const getConversationSummary = useCallback(() => {
    const userMessages = messages.filter(m => !m.isBot);
    const botMessages = messages.filter(m => m.isBot && !m.isLoading);
    
    return {
      userMessageCount: userMessages.length,
      botMessageCount: botMessages.length,
      totalMessages: userMessages.length + botMessages.length,
      sessionDuration: Date.now() - conversationMetrics.sessionStartTime.getTime(),
      lastActivity: conversationMetrics.lastActivity,
      hasProducts: messages.some(m => m.products && m.products.length > 0),
      mostCommonIntent: messages
        .filter(m => m.intent)
        .reduce((acc, m) => {
          acc[m.intent!] = (acc[m.intent!] || 0) + 1;
          return acc;
        }, {} as Record<string, number>)
    };
  }, [messages, conversationMetrics]);

  return {
    messages,
    sendMessage,
    clearChat,
    isLoading: sendMessageMutation.isPending,
    isConnected: isConnected ?? false,
    checkConnection,
    error: sendMessageMutation.error,
    // Exportar funciones de contexto
    updateCurrentPage,
    updateCurrentProduct,
    updateContextData,
    sessionId,
    // Nuevas exportaciones
    botTypingState,
    conversationMetrics,
    getConversationSummary
  };
};

// Función helper para obtener mensaje de escritura
function getTypingMessage(state: 'thinking' | 'typing' | 'searching'): string {
  switch (state) {
    case 'thinking':
      return 'InfoBot está pensando...';
    case 'searching':
      return 'InfoBot está buscando productos...';
    case 'typing':
      return 'InfoBot está escribiendo...';
    default:
      return 'InfoBot está escribiendo...';
  }
}
