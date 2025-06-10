import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Homepage } from './components/Homepage';
import { FloatingChatbot } from './components/FloatingChatbot';
import ProductDetail from './components/ProductDetail';
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
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<Homepage />} />
            <Route path="/product/:id" element={<ProductDetail />} />
          </Routes>
          <FloatingChatbot />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
