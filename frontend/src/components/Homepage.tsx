import React, { useEffect } from 'react';
import { Header } from './homepage/Header';
import { Hero } from './homepage/Hero';
import { ProductSections } from './homepage/ProductSections';
import { Footer } from './homepage/Footer';
import { useChat } from '../hooks/useChat';

export const Homepage: React.FC = () => {
  const { updateCurrentPage, updateCurrentProduct } = useChat();
  
  useEffect(() => {
    // Actualizar el contexto cuando se carga la página de inicio
    updateCurrentPage('home');
    updateCurrentProduct(undefined); // Limpiar el producto actual
  }, [updateCurrentPage, updateCurrentProduct]);
  
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <Hero />
      <ProductSections />
      <Footer />
    </div>
  );
};
