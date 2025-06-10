import React from 'react';
import { Search, User, ShoppingCart, Phone, Mail } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm">
      {/* Top bar */}
      <div className="bg-gray-800 text-white py-2">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center text-sm">
            <div className="flex space-x-4">
              <div className="flex items-center">
                <Phone className="w-4 h-4 mr-1" />
                <span>+51 1 234-5678</span>
              </div>
              <div className="flex items-center">
                <Mail className="w-4 h-4 mr-1" />
                <span>ventas@infotec.com.pe</span>
              </div>
            </div>
            <div className="flex space-x-4">
              <span>Lun - Vie: 9:00 AM - 6:00 PM</span>
              <span>Sáb: 9:00 AM - 2:00 PM</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main header */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <div className="flex-shrink-0">
            <img 
              className="h-12 w-auto" 
              src="/logo-infotec.png" 
              alt="GRUPO INFOTEC" 
            />
            <div className="text-xl font-bold text-blue-600">GRUPO INFOTEC</div>
          </div>

          {/* Search bar */}
          <div className="flex-1 max-w-lg mx-8">
            <div className="relative">
              <input
                type="text"
                placeholder="Buscar productos..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
            </div>
          </div>

          {/* Right section */}
          <div className="flex items-center space-x-4">
            <button className="flex items-center text-gray-700 hover:text-blue-600">
              <User className="w-5 h-5 mr-1" />
              <span className="text-sm">Mi Cuenta</span>
            </button>
            <button className="flex items-center text-gray-700 hover:text-blue-600">
              <ShoppingCart className="w-5 h-5 mr-1" />
              <span className="text-sm">Carrito (0)</span>
            </button>
          </div>
        </div>

        {/* Navigation */}
        <nav className="border-t border-gray-200">
          <div className="flex space-x-8 py-4">
            <a href="#" className="text-gray-700 hover:text-blue-600 font-medium">Inicio</a>
            <a href="#" className="text-gray-700 hover:text-blue-600 font-medium">Laptops</a>
            <a href="#" className="text-gray-700 hover:text-blue-600 font-medium">PC Gamer</a>
            <a href="#" className="text-gray-700 hover:text-blue-600 font-medium">Monitores</a>
            <a href="#" className="text-gray-700 hover:text-blue-600 font-medium">Accesorios</a>
            <a href="#" className="text-gray-700 hover:text-blue-600 font-medium">Impresoras</a>
            <a href="#" className="text-gray-700 hover:text-blue-600 font-medium">Soporte Técnico</a>
            <a href="#" className="text-gray-700 hover:text-blue-600 font-medium">Contacto</a>
          </div>
        </nav>
      </div>
    </header>
  );
};
