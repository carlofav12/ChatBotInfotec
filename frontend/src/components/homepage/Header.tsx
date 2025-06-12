import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, User, ShoppingCart, Phone, Mail, Mic, Camera } from 'lucide-react';
import { useCart } from '../../contexts/CartContext';

export const Header: React.FC = () => {
  const navigate = useNavigate();
  const { state } = useCart();
  const [isFocused, setIsFocused] = useState(false);
  const [searchValue, setSearchValue] = useState("");

  return (
    <header className="bg-white shadow-md font-sans">
      {/* Top bar */}
      <div className="bg-gradient-to-r text-black text-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 flex justify-between items-center">
          <div className="flex space-x-6">
            <div className="flex items-center">
              <Phone className="w-4 h-4 mr-1" />
              <span>+51 1 234-5678</span>
            </div>
            <div className="flex items-center">
              <Mail className="w-4 h-4 mr-1" />
              <span>ventas@infotec.com.pe</span>
            </div>
          </div>
          <div className="space-x-4 hidden md:flex">
            <span>Lun - Vie: 9:00 AM - 6:00 PM</span>
            <span>Sáb: 9:00 AM - 2:00 PM</span>
          </div>
        </div>
      </div>

      {/* Main header */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5 flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
        {/* Logo */}
        <div className="flex items-center space-x-3">
          <span className="text-2xl font-extrabold text-[#002855] tracking-wide">GRUPO INFOTEC</span>
        </div>

        {/* Enhanced Search bar */}
        <div className="w-full max-w-2xl relative">
          {/* Search container with gradient background */}
          <div className={`relative overflow-hidden rounded-2xl transition-all duration-300 ${isFocused
            ? 'shadow-2xl shadow-[#FFD100]/20 scale-105'
            : 'shadow-lg hover:shadow-xl hover:scale-102'
            }`}>

            {/* Animated gradient background */}
            <div className="absolute inset-0 bg-gradient-to-r from-[#FFD100] via-[#FFF200] to-[#FFD100] opacity-10 animate-pulse"></div>

            {/* Main search input */}
            <div className="relative bg-white/95 backdrop-blur-sm">
              <input
                type="text"
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
                placeholder="¿Qué estás buscando hoy?"
                className="w-full pl-14 pr-32 py-4 text-lg bg-transparent border-2 border-transparent rounded-2xl focus:border-[#FFD100] focus:outline-none transition-all duration-300 placeholder-gray-500"
              />

              {/* Search icon with animation */}
              <div className={`absolute left-4 top-1/2 transform -translate-y-1/2 transition-all duration-300 ${isFocused ? 'text-[#FFD100] scale-110' : 'text-gray-400'
                }`}>
                <Search className="h-6 w-6" />
              </div>

              {/* Action buttons */}
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-2">
                {/* Voice search button */}
                <button className="p-2 rounded-full bg-gray-100 hover:bg-[#FFD100] hover:text-white transition-all duration-300 group">
                  <Mic className="h-4 w-4 group-hover:scale-110 transition-transform" />
                </button>

                {/* Camera search button */}
                <button className="p-2 rounded-full bg-gray-100 hover:bg-[#FFD100] hover:text-white transition-all duration-300 group">
                  <Camera className="h-4 w-4 group-hover:scale-110 transition-transform" />
                </button>

                {/* Search button */}
                <button className="px-6 py-2 bg-gradient-to-r from-[#FFD100] to-[#FFF200] text-black font-semibold rounded-full hover:shadow-lg hover:scale-105 transition-all duration-300 hover:from-[#FFF200] hover:to-[#FFD100]">
                  Buscar
                </button>
              </div>
            </div>

            {/* Bottom glow effect */}
            <div className={`absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-3/4 h-1 bg-gradient-to-r from-transparent via-[#FFD100] to-transparent rounded-full transition-opacity duration-300 ${isFocused ? 'opacity-60' : 'opacity-0'
              }`}></div>
          </div>

          {/* Search suggestions (visible when focused) */}
          {isFocused && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-xl shadow-2xl border border-gray-100 z-50 overflow-hidden animate-in slide-in-from-top-2 duration-200">
              <div className="p-2">
                <div className="text-sm text-gray-500 px-3 py-2 font-medium">Búsquedas populares</div>
                {['Laptops gaming', 'Smartphones', 'Audífonos bluetooth', 'Tablets', 'Accesorios tech'].map((suggestion, index) => (
                  <button
                    key={index}
                    className="w-full text-left px-3 py-2 hover:bg-[#FFD100]/10 rounded-lg transition-colors duration-200 flex items-center space-x-3"
                    onClick={() => {
                      setSearchValue(suggestion);
                      setIsFocused(false);
                    }}
                  >
                    <Search className="h-4 w-4 text-gray-400" />
                    <span>{suggestion}</span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* User & Cart */}
        <div className="flex items-center space-x-6">
          <button className="flex items-center text-gray-700 hover:text-[#002855] transition">
            <User className="w-5 h-5 mr-1" />
            <span className="text-sm">Mi Cuenta</span>
          </button>
          <button
            onClick={() => navigate('/cart')}
            className="relative flex items-center text-gray-700 hover:text-[#002855] transition"
          >
            <ShoppingCart className="w-5 h-5 mr-1" />
            <span className="text-sm">Carrito ({state.itemCount})</span>
            {state.itemCount > 0 && (
              <span className="absolute -top-2 -right-2 bg-red-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center animate-pulse">
                {state.itemCount > 99 ? '99+' : state.itemCount}
              </span>
            )}
          </button>
        </div>
      </div>

      {/* Navigation */}
      <nav className="bg-[#002855]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap justify-center md:justify-start space-x-6 py-3 text-sm font-medium text-white">
            {['Inicio', 'Laptops', 'PC Gamer', 'Monitores', 'Accesorios', 'Impresoras', 'Soporte Técnico', 'Contacto'].map((item, index) => (
              <a
                key={index}
                href="#"
                className="hover:text-[#FFD100] transition-colors duration-200"
              >
                {item}
              </a>
            ))}
          </div>
        </div>
      </nav>
    </header>
  );
};