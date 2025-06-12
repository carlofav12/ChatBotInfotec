import React, { useState, useEffect } from 'react';
import {
  ChevronLeft,
  ChevronRight,
  Award,
  MapPin
} from 'lucide-react';

export const Hero: React.FC = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    {
      title: "Líderes en Tecnología",
      subtitle: "Laptops de Alto Rendimiento",
      description:
        "Encuentra las mejores laptops gamer y profesionales con garantía y soporte técnico especializado.",
      buttonText: "Ver Laptops",
      bg: ["#003366", "#003366", "#003366"]
    },
    {
      title: "Envíos a Nivel Nacional",
      subtitle: "Servidores y Computadoras Pro",
      description:
        "Soluciones para empresas, equipos potentes y configuraciones a medida.",
      buttonText: "Ver Equipos",
      bg: ["#003366", "#003366", "#003366"]
    },
    {
      title: "Tecnología de Confianza",
      subtitle: "Proyectores y Monitores Certificados",
      description:
        "Productos con garantía extendida, precios competitivos y atención personalizada.",
      buttonText: "Ver Pantallas",
      bg: ["#003366", "#003366", "#003366"]
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSlide((i) => (i + 1) % slides.length);
    }, 6000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-[#FFFFFF] font-sans">
      <div className="relative h-[520px] overflow-hidden">
        {/* Fondo con gradiente y overlays */}
        <div className="absolute inset-0 bg-[#F36A21] transition-all duration-1000">
          <div className="absolute inset-0" />
        </div>

        {/* Contenido del Hero */}
        <div className="relative z-10 max-w-7xl mx-auto px-6 h-full flex items-center">
          <div className="text-white max-w-4xl">
            <div className="flex items-center space-x-2 mb-4">
              <Award className="w-6 h-6 text-[#003366]" />
              <span className="text-sm uppercase tracking-wider text-[#003366]">
                {slides[currentSlide].title}
              </span>
            </div>

            <h1 className="text-5xl md:text-6xl font-extrabold mb-6 leading-tight">
              {slides[currentSlide].subtitle.split(' ').slice(0, -1).join(' ')}{" "}
              <span className="text-[#003366]">
                {slides[currentSlide].subtitle.split(' ').slice(-1)}
              </span>
            </h1>

            <p className="text-lg md:text-xl mb-8 text-gray-200 font-light">
              {slides[currentSlide].description}
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <button className="bg-[#FFFFFF] text-black px-8 py-3 rounded-xl font-bold text-lg hover:bg-[#FFFFFF] transition transform hover:scale-105 shadow-md">
                {slides[currentSlide].buttonText}
              </button>
              <button className="bg-[#FFFFFF] text-black px-8 py-3 rounded-xl font-semibold text-lg transition transform hover:scale-105 shadow-md hover:text-[#F36A21]">
                Ver Catálogo Completo
              </button>
            </div>
          </div>
        </div>

        {/* Flechas de navegación */}
        <button
          onClick={() =>
            setCurrentSlide((i) => (i - 1 + slides.length) % slides.length)
          }
          className="absolute left-6 top-1/2 -translate-y-1/2 bg-white bg-opacity-20 hover:bg-opacity-40 backdrop-blur-sm p-3 rounded-full transition"
        >
          <ChevronLeft className="w-6 h-6 text-white" />
        </button>
        <button
          onClick={() => setCurrentSlide((i) => (i + 1) % slides.length)}
          className="absolute right-6 top-1/2 -translate-y-1/2 bg-white bg-opacity-20 hover:bg-opacity-40 backdrop-blur-sm p-3 rounded-full transition"
        >
          <ChevronRight className="w-6 h-6 text-white" />
        </button>

        {/* Indicadores */}
        <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex space-x-3">
          {slides.map((_, idx) => (
            <button
              key={idx}
              onClick={() => setCurrentSlide(idx)}
              className={`rounded-full transition-all duration-300 ${idx === currentSlide
                ? 'bg-[#F36A21] w-8 h-3'
                : 'bg-white bg-opacity-40 w-3 h-3 hover:bg-opacity-80'
                }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};