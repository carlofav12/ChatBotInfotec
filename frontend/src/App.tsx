import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Homepage } from './components/Homepage';
import { FloatingChatbot } from './components/FloatingChatbot';
import ProductDetail from './components/ProductDetail';
import { CartView } from './components/CartView';
import { CartProvider } from './contexts/CartContext';
import './App.css';

// Configurar React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 2,
      staleTime: 1000 * 60 * 5, // 5 minutos
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <CartProvider>
        <Router>
          <div className="App">
            <Routes>
              <Route path="/" element={<Homepage />} />
              <Route path="/product/:id" element={<ProductDetail />} />
              <Route path="/cart" element={<CartView />} />
            </Routes>
            <FloatingChatbot />
          </div>
        </Router>
      </CartProvider>
    </QueryClientProvider>
  );
}

export default App;
