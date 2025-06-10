import React from 'react';
import { ChevronLeft, ChevronRight, Star, Truck, Shield, Headphones } from 'lucide-react';

export const Hero: React.FC = () => {
  return (
    <div className="bg-gray-50">
      {/* Hero Carousel */}
      <div className="relative h-96 bg-gradient-to-r from-blue-600 to-indigo-600">
        <div className="absolute inset-0 bg-black bg-opacity-20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center">
          <div className="text-white">
            <h1 className="text-4xl md:text-6xl font-bold mb-4">
              Las Mejores <span className="text-yellow-400">Laptops Gamer</span>
            </h1>
            <p className="text-xl mb-6">Descubre nuestra nueva colección de laptops gaming de última generación</p>
            <button className="bg-yellow-400 text-black px-8 py-3 rounded-lg font-semibold hover:bg-yellow-300 transition-colors">
              Ver Ofertas
            </button>
          </div>
        </div>
        
        {/* Carousel controls */}
        <button className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-full p-2">
          <ChevronLeft className="w-6 h-6 text-white" />
        </button>
        <button className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-full p-2">
          <ChevronRight className="w-6 h-6 text-white" />
        </button>
      </div>

      {/* Features */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="flex items-center space-x-3 p-4 bg-white rounded-lg shadow-sm">
            <Truck className="w-8 h-8 text-blue-600" />
            <div>
              <h3 className="font-semibold">Envío Gratis</h3>
              <p className="text-sm text-gray-600">En compras mayores a S/500</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3 p-4 bg-white rounded-lg shadow-sm">
            <Shield className="w-8 h-8 text-green-600" />
            <div>
              <h3 className="font-semibold">Garantía Extendida</h3>
              <p className="text-sm text-gray-600">Hasta 3 años de garantía</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3 p-4 bg-white rounded-lg shadow-sm">
            <Headphones className="w-8 h-8 text-purple-600" />
            <div>
              <h3 className="font-semibold">Soporte 24/7</h3>
              <p className="text-sm text-gray-600">Atención técnica especializada</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3 p-4 bg-white rounded-lg shadow-sm">
            <Star className="w-8 h-8 text-yellow-500" />
            <div>
              <h3 className="font-semibold">Calidad Premium</h3>
              <p className="text-sm text-gray-600">Productos certificados</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
