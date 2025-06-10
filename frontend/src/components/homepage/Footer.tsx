import React from 'react';
import { Facebook, Instagram, Twitter, Youtube, MapPin, Phone, Mail, Clock } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <h3 className="text-xl font-bold mb-4">GRUPO INFOTEC</h3>
            <p className="text-gray-300 mb-4">
              Tu aliado tecnológico de confianza. Especialistas en equipos de cómputo, 
              gaming y soluciones empresariales desde 2010.
            </p>
            <div className="flex space-x-4">
              <Facebook className="w-5 h-5 text-gray-400 hover:text-blue-400 cursor-pointer" />
              <Instagram className="w-5 h-5 text-gray-400 hover:text-pink-400 cursor-pointer" />
              <Twitter className="w-5 h-5 text-gray-400 hover:text-blue-300 cursor-pointer" />
              <Youtube className="w-5 h-5 text-gray-400 hover:text-red-400 cursor-pointer" />
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold mb-4">Enlaces Rápidos</h4>
            <ul className="space-y-2 text-gray-300">
              <li><a href="#" className="hover:text-white">Inicio</a></li>
              <li><a href="#" className="hover:text-white">Productos</a></li>
              <li><a href="#" className="hover:text-white">Servicios</a></li>
              <li><a href="#" className="hover:text-white">Soporte Técnico</a></li>
              <li><a href="#" className="hover:text-white">Garantías</a></li>
              <li><a href="#" className="hover:text-white">Contacto</a></li>
            </ul>
          </div>

          {/* Categories */}
          <div>
            <h4 className="font-semibold mb-4">Categorías</h4>
            <ul className="space-y-2 text-gray-300">
              <li><a href="#" className="hover:text-white">Laptops Gamer</a></li>
              <li><a href="#" className="hover:text-white">PC Gamer</a></li>
              <li><a href="#" className="hover:text-white">Monitores</a></li>
              <li><a href="#" className="hover:text-white">Accesorios Gaming</a></li>
              <li><a href="#" className="hover:text-white">Impresoras</a></li>
              <li><a href="#" className="hover:text-white">Tablets</a></li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="font-semibold mb-4">Contacto</h4>
            <div className="space-y-3 text-gray-300">
              <div className="flex items-start space-x-3">
                <MapPin className="w-5 h-5 mt-0.5 flex-shrink-0" />
                <div>
                  <p>Av. Tecnología 123</p>
                  <p>San Isidro, Lima - Perú</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <Phone className="w-5 h-5 flex-shrink-0" />
                <div>
                  <p>+51 1 234-5678</p>
                  <p>+51 987-654-321</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <Mail className="w-5 h-5 flex-shrink-0" />
                <div>
                  <p>ventas@infotec.com.pe</p>
                  <p>soporte@infotec.com.pe</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <Clock className="w-5 h-5 mt-0.5 flex-shrink-0" />
                <div>
                  <p>Lun - Vie: 9:00 AM - 6:00 PM</p>
                  <p>Sáb: 9:00 AM - 2:00 PM</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">
              © 2024 GRUPO INFOTEC. Todos los derechos reservados.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="#" className="text-gray-400 hover:text-white text-sm">Términos y Condiciones</a>
              <a href="#" className="text-gray-400 hover:text-white text-sm">Política de Privacidad</a>
              <a href="#" className="text-gray-400 hover:text-white text-sm">Política de Cookies</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};
