import React from 'react';
import { Facebook, Instagram, Twitter, Youtube, MapPin, Phone, Mail, Clock } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-[#F36A21]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <h3 className="text-2xl font-extrabold text-white mb-4">GRUPO INFOTEC</h3>
            <p className="text-gray-200 mb-4 leading-relaxed">
              Tu aliado tecnológico de confianza. Especialistas en equipos de cómputo, gaming y soluciones empresariales desde 2010.
            </p>
            <div className="flex space-x-4">
              <Facebook className="w-5 h-5 text-gray-300 hover:text-white cursor-pointer transition-colors" />
              <Instagram className="w-5 h-5 text-gray-300 hover:text-white cursor-pointer transition-colors" />
              <Twitter className="w-5 h-5 text-gray-300 hover:text-white cursor-pointer transition-colors" />
              <Youtube className="w-5 h-5 text-gray-300 hover:text-white cursor-pointer transition-colors" />
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold text-lg text-white mb-4">Enlaces Rápidos</h4>
            <ul className="space-y-2 text-gray-200">
              {['Inicio', 'Productos', 'Servicios', 'Soporte Técnico', 'Garantías', 'Contacto'].map((text, i) => (
                <li key={i}><a href="#" className="hover:text-white transition-colors">{text}</a></li>
              ))}
            </ul>
          </div>

          {/* Categories */}
          <div>
            <h4 className="font-semibold text-lg text-white mb-4">Categorías</h4>
            <ul className="space-y-2 text-gray-200">
              {['Laptops Gamer', 'PC Gamer', 'Monitores', 'Accesorios Gaming', 'Impresoras', 'Tablets'].map((text, i) => (
                <li key={i}><a href="#" className="hover:text-white transition-colors">{text}</a></li>
              ))}
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="font-semibold text-lg text-white mb-4">Contacto</h4>
            <div className="space-y-4 text-gray-200 text-sm">
              <div className="flex items-start space-x-3">
                <MapPin className="w-5 h-5 mt-0.5 text-[#F36A21]" />
                <div>
                  <p>Av. Tecnología 123</p>
                  <p>San Isidro, Lima - Perú</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Phone className="w-5 h-5 text-[#F36A21]" />
                <div>
                  <p>+51 1 234-5678</p>
                  <p>+51 987-654-321</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="w-5 h-5 text-[#F36A21]" />
                <div>
                  <p>ventas@infotec.com.pe</p>
                  <p>soporte@infotec.com.pe</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Clock className="w-5 h-5 mt-0.5 text-[#F36A21]" />
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
      <div className="border-t border-[#003366]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-300 text-sm">
              © 2024 <span className="text-white font-semibold">GRUPO INFOTEC</span>. Todos los derechos reservados.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0 text-sm">
              <a href="#" className="text-gray-300 hover:text-white transition-colors">Términos y Condiciones</a>
              <a href="#" className="text-gray-300 hover:text-white transition-colors">Política de Privacidad</a>
              <a href="#" className="text-gray-300 hover:text-white transition-colors">Política de Cookies</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};