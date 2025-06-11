import React, { useState, useEffect } from 'react';
import {
  ChevronLeft,
  ChevronRight,
  Star,
  Truck,
  Shield,
  Headphones,
  Award,
  MapPin
} from 'lucide-react';

export const Hero: React.FC = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    {
      title: "Líderes en Tecnología",
      subtitle: "Las Mejores Laptops Gamer",
      description:
        "Descubre nuestra nueva colección de laptops gaming de última generación con la mejor garantía del Perú",
      buttonText: "Ver Ofertas Gaming",
      bgClass: "from-[#002855] via-[#003f7f] to-[#001F3F]"
    },
    {
      title: "Venta Online en Todo el Perú",
      subtitle: "Computadoras y Servidores",
      description:
        "Equipos empresariales y profesionales con soporte técnico especializado y garantía extendida",
      buttonText: "Ver Equipos Pro",
      bgClass: "from-[#1C2E4A] via-[#2F4E6E] to-[#1B2C47]"
    },
    {
      title: "Tecnología Certificada",
      subtitle: "Proyectores y Monitores",
      description:
        "La más amplia gama de monitores gaming y proyectores profesionales con envío gratuito",
      buttonText: "Explorar Catálogo",
      bgClass: "from-[#003f7f] via-[#0053a6] to-[#002855]"
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 6000);
    return () => clearInterval(timer);
  }, []);

  const nextSlide = () => setCurrentSlide((prev) => (prev + 1) % slides.length);
  const prevSlide = () => setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);

  return (
    <div className="bg-[#F3F4F6] font-sans">
      {/* Hero Carousel */}
      <div className="relative h-[520px] overflow-hidden">
        <div className={`absolute inset-0 bg-gradient-to-br ${slides[currentSlide].bgClass} transition-all duration-1000`}>
          <div className="absolute inset-0 bg-black bg-opacity-40" />

          {/* Animated elements */}
          <div className="absolute top-12 right-12 w-28 h-28 border-2 border-yellow-300 opacity-20 rotate-45 animate-pulse"></div>
          <div className="absolute bottom-16 left-16 w-20 h-20 border-2 border-yellow-300 rounded-full animate-bounce"></div>
          <div className="absolute top-1/3 right-1/4 w-14 h-14 bg-white bg-opacity-10 rotate-12 animate-pulse"></div>
        </div>

        <div className="relative max-w-7xl mx-auto px-6 h-full flex items-center z-10">
          <div className="text-white max-w-4xl">
            <div className="flex items-center mb-4 space-x-2">
              <Award className="w-6 h-6 text-[#FFD100]" />
              <span className="text-sm font-medium uppercase tracking-wider text-[#FFD100]">
                {slides[currentSlide].title}
              </span>
            </div>

            <h1 className="text-5xl md:text-7xl font-extrabold mb-6 leading-tight">
              {slides[currentSlide].subtitle.split(' ').slice(0, -1).join(' ')}{' '}
              <span className="text-[#FFD100]">{slides[currentSlide].subtitle.split(' ').slice(-1)}</span>
            </h1>

            <p className="text-lg md:text-2xl mb-8 text-gray-200 max-w-3xl font-light">
              {slides[currentSlide].description}
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <button className="bg-[#FFD100] text-black px-8 py-4 rounded-xl font-bold text-lg hover:bg-yellow-400 transition-transform duration-300 transform hover:scale-105 shadow-xl">
                {slides[currentSlide].buttonText}
              </button>
              <button className="border-2 border-white text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white hover:text-black transition-all duration-300">
                Ver Catálogo Completo
              </button>
            </div>

            <div className="flex items-center mt-8 text-sm text-gray-200">
              <MapPin className="w-4 h-4 mr-2" />
              <span>Envíos a todo el Perú • Tiendas en Lima • Atención 24/7</span>
            </div>
          </div>
        </div>

        {/* Carousel controls */}
        <button onClick={prevSlide} className="absolute left-6 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-20 hover:bg-opacity-40 backdrop-blur-sm rounded-full p-3 transition">
          <ChevronLeft className="w-6 h-6 text-white" />
        </button>
        <button onClick={nextSlide} className="absolute right-6 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-20 hover:bg-opacity-40 backdrop-blur-sm rounded-full p-3 transition">
          <ChevronRight className="w-6 h-6 text-white" />
        </button>

        {/* Indicators */}
        <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2 flex space-x-3">
          {slides.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentSlide(index)}
              className={`h-3 rounded-full transition-all duration-300 ${
                index === currentSlide ? 'bg-[#FFD100] w-8' : 'bg-white bg-opacity-40 w-3 hover:bg-opacity-80'
              }`}
            />
          ))}
        </div>
      </div>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-6 py-14">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold text-[#002855] mb-3">¿Por qué elegir Infotec?</h2>
          <p className="text-gray-600 text-lg">Más de 15 años siendo líderes en tecnología en el Perú</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {[
            {
              icon: <Truck className="w-8 h-8 text-blue-700" />,
              title: "Envío Gratis",
              color: "blue-100",
              lines: ["En compras mayores a S/500", "• Delivery 24-48 horas en Lima", "• Envíos a todo el Perú"]
            },
            {
              icon: <Shield className="w-8 h-8 text-green-700" />,
              title: "Garantía Extendida",
              color: "green-100",
              lines: ["Hasta 3 años de garantía", "• Productos certificados", "• Respaldo internacional"]
            },
            {
              icon: <Headphones className="w-8 h-8 text-purple-700" />,
              title: "Soporte 24/7",
              color: "purple-100",
              lines: ["Atención técnica especializada", "• Técnicos certificados", "• Chat en vivo"]
            },
            {
              icon: <Star className="w-8 h-8 text-yellow-500" />,
              title: "Calidad Premium",
              color: "yellow-100",
              lines: ["Productos originales y certificados", "• Marcas reconocidas", "• Mejor precio garantizado"]
            }
          ].map((feature, i) => (
            <div key={i} className={`group bg-white p-6 rounded-2xl shadow-md hover:shadow-xl border border-gray-100 hover:-translate-y-1.5 transition-transform`}>
              <div className={`bg-${feature.color} w-16 h-16 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition`}>
                {feature.icon}
              </div>
              <h3 className="font-bold text-xl mb-2 text-[#002855]">{feature.title}</h3>
              <p className="text-gray-600 mb-2">{feature.lines[0]}</p>
              {feature.lines.slice(1).map((line, idx) => (
                <p key={idx} className="text-sm text-blue-700 font-semibold">{line}</p>
              ))}
            </div>
          ))}
        </div>

        {/* Stats */}
        <div className="bg-gradient-to-r from-[#002855] to-[#003f7f] rounded-3xl p-10 mt-14 text-white">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            {[
              ["15+", "Años en el mercado"],
              ["50K+", "Clientes satisfechos"],
              ["1000+", "Productos disponibles"],
              ["99%", "Satisfacción del cliente"]
            ].map(([stat, label], idx) => (
              <div key={idx}>
                <div className="text-4xl font-extrabold text-[#FFD100] mb-2">{stat}</div>
                <div className="text-sm font-medium">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};
