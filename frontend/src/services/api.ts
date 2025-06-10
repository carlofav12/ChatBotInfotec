import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export interface ChatMessage {
  message: string;
  session_id?: string;
  current_page?: string;
  current_product_id?: number;
  context_data?: Record<string, any>;
}

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  original_price?: number;
  brand: string;
  model: string;
  stock_quantity: number;
  rating: number;
  review_count: number;
  image_url: string;
}

export interface ChatResponse {
  response: string;
  timestamp: string;
  tokens_used?: number;
  intent?: string;
  entities?: Record<string, any>;
  products?: Product[];
  cart_total?: number;
}

export interface ConversationHistoryItem {
  role: string;
  content: string;
  timestamp: string;
}

// Configurar axios
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 segundos timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para logging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.data);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Funciones de API
export const apiService = {  // Enviar mensaje al chatbot
  sendMessage: async (
    userMessage: string,
    sessionId?: string,
    currentPage?: string,
    currentProductId?: number,
    contextData?: Record<string, any>
  ): Promise<ChatResponse> => {
    try {
      const response = await api.post<ChatResponse>('/api/chat', {
        message: userMessage,
        session_id: sessionId,
        current_page: currentPage,
        current_product_id: currentProductId,
        context_data: contextData,
      });
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw new Error('Error al enviar mensaje. Verifica que el backend esté ejecutándose.');
    }
  },

  // Obtener historial de conversación
  getHistory: async (): Promise<ConversationHistoryItem[]> => {
    try {
      const response = await api.get<{ history: ConversationHistoryItem[] }>('/api/history');
      return response.data.history;
    } catch (error) {
      console.error('Error getting history:', error);
      throw new Error('Error al obtener historial');
    }
  },
  // Limpiar historial
  clearHistory: async (sessionId?: string): Promise<void> => {
    try {
      await api.post('/api/clear-history', {
        session_id: sessionId,
      });
    } catch (error) {
      console.error('Error clearing history:', error);
      throw new Error('Error al limpiar historial');
    }
  },

  // Verificar salud del API
  healthCheck: async (): Promise<boolean> => {
    try {
      const response = await api.get('/health');
      return response.status === 200;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  },

  // Obtener estadísticas
  getStats: async (): Promise<any> => {
    try {
      const response = await api.get('/api/stats');
      return response.data.stats;
    } catch (error) {
      console.error('Error getting stats:', error);
      throw new Error('Error al obtener estadísticas');
    }
  },
};

// Funciones específicas para productos
export const fetchProducts = async (category?: string, search?: string) => {
  try {
    let url = '/api/products';
    const params = new URLSearchParams();
    
    if (category) params.append('category_id', category);
    if (search) params.append('search', search);
    
    if (params.toString()) {
      url += `?${params.toString()}`;
    }
    
    const response = await api.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    throw new Error('Error al obtener productos');
  }
};

export const fetchProductById = async (id: number) => {
  try {
    const response = await api.get(`/api/products/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching product ${id}:`, error);
    throw new Error('Error al obtener el producto');
  }
};

export const fetchCategories = async () => {
  try {
    const response = await api.get('/api/categories');
    return response.data;
  } catch (error) {
    console.error('Error fetching categories:', error);
    throw new Error('Error al obtener categorías');
  }
};

export const addToCart = async (userId: number, productId: number, quantity: number) => {
  try {
    const response = await api.post('/api/cart', {
      user_id: userId,
      product_id: productId,
      quantity
    });
    return response.data;
  } catch (error) {
    console.error('Error adding to cart:', error);
    throw new Error('Error al agregar al carrito');
  }
};

export const getCart = async (userId: number) => {
  try {
    const response = await api.get(`/api/cart/${userId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching cart:', error);
    throw new Error('Error al obtener el carrito');
  }
};

export default apiService;
