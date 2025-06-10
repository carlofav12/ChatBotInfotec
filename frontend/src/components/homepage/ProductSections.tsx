import React from 'react';
import { Star, Heart, ShoppingCart } from 'lucide-react';

interface Product {
  id: number;
  name: string;
  price: number;
  originalPrice?: number;
  image: string;
  rating: number;
  reviews: number;
  isNew?: boolean;
}

const ProductCard: React.FC<{ product: Product }> = ({ product }) => {
  const discount = product.originalPrice 
    ? Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100)
    : 0;

  return (
    <div className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow border">
      <div className="relative">
        <img 
          src={product.image} 
          alt={product.name}
          className="w-full h-48 object-cover rounded-t-lg"
        />
        {product.isNew && (
          <span className="absolute top-2 left-2 bg-green-500 text-white px-2 py-1 text-xs rounded">
            NUEVO
          </span>
        )}
        {discount > 0 && (
          <span className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 text-xs rounded">
            -{discount}%
          </span>
        )}
        <button className="absolute top-2 right-2 p-1 bg-white rounded-full shadow-sm hover:bg-gray-100">
          <Heart className="w-4 h-4 text-gray-400" />
        </button>
      </div>
      
      <div className="p-4">
        <h3 className="font-semibold text-gray-800 mb-2 line-clamp-2">{product.name}</h3>
        
        <div className="flex items-center mb-2">
          <div className="flex items-center">
            {[...Array(5)].map((_, i) => (
              <Star 
                key={i} 
                className={`w-4 h-4 ${i < product.rating ? 'text-yellow-400 fill-current' : 'text-gray-300'}`} 
              />
            ))}
          </div>
          <span className="text-sm text-gray-600 ml-2">({product.reviews})</span>
        </div>
        
        <div className="flex items-center justify-between">
          <div>
            <span className="text-lg font-bold text-blue-600">S/ {product.price.toLocaleString()}</span>
            {product.originalPrice && (
              <span className="text-sm text-gray-500 line-through ml-2">
                S/ {product.originalPrice.toLocaleString()}
              </span>
            )}
          </div>
          <button className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 transition-colors">
            <ShoppingCart className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export const ProductSections: React.FC = () => {
  // Mock data basado en la información de Infotec
  const newProducts: Product[] = [
    {
      id: 1,
      name: "Laptop HP Pavilion Gaming 15.6\" Intel Core i5 16GB RAM 512GB SSD",
      price: 3299,
      originalPrice: 3899,
      image: "/api/placeholder/300/200",
      rating: 5,
      reviews: 24,
      isNew: true
    },
    {
      id: 2,
      name: "PC Gamer AMD Ryzen 5 RTX 4060 16GB RAM 1TB SSD",
      price: 4599,
      originalPrice: 5199,
      image: "/api/placeholder/300/200",
      rating: 4,
      reviews: 18,
      isNew: true
    },
    {
      id: 3,
      name: "Monitor Gamer Asus 24\" 144Hz 1ms FHD",
      price: 899,
      originalPrice: 1099,
      image: "/api/placeholder/300/200",
      rating: 5,
      reviews: 32,
      isNew: true
    },
    {
      id: 4,
      name: "Teclado Mecánico RGB Gamer Logitech G915",
      price: 649,
      image: "/api/placeholder/300/200",
      rating: 4,
      reviews: 15
    }
  ];

  const gamingLaptops: Product[] = [
    {
      id: 5,
      name: "Laptop ASUS ROG Strix G15 AMD Ryzen 7 RTX 4060 16GB",
      price: 5499,
      originalPrice: 5999,
      image: "/api/placeholder/300/200",
      rating: 5,
      reviews: 28
    },
    {
      id: 6,
      name: "Laptop MSI Gaming GF63 Intel i7 GTX 1650 8GB",
      price: 3799,
      originalPrice: 4299,
      image: "/api/placeholder/300/200",
      rating: 4,
      reviews: 19
    },
    {
      id: 7,
      name: "Laptop Acer Nitro 5 AMD Ryzen 5 RTX 3050 16GB",
      price: 3999,
      image: "/api/placeholder/300/200",
      rating: 4,
      reviews: 35
    },
    {
      id: 8,
      name: "Laptop Lenovo Legion 5 AMD Ryzen 7 RTX 4070 32GB",
      price: 6899,
      originalPrice: 7499,
      image: "/api/placeholder/300/200",
      rating: 5,
      reviews: 22
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Lo + Nuevo en Infotec */}
      <section className="mb-12">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Lo + Nuevo en Infotec</h2>
          <button className="text-blue-600 hover:text-blue-800 font-medium">Ver todos</button>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {newProducts.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>

      {/* Laptops Gamer */}
      <section className="mb-12">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Laptops Gamer</h2>
          <button className="text-blue-600 hover:text-blue-800 font-medium">Ver todos</button>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {gamingLaptops.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>

      {/* Categorías destacadas */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Categorías Destacadas</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-6 text-white text-center hover:from-blue-600 hover:to-blue-700 transition-colors cursor-pointer">
            <h3 className="font-semibold mb-2">PC Gamer</h3>
            <p className="text-sm opacity-90">Computadoras de alto rendimiento</p>
          </div>
          <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg p-6 text-white text-center hover:from-purple-600 hover:to-purple-700 transition-colors cursor-pointer">
            <h3 className="font-semibold mb-2">Monitores</h3>
            <p className="text-sm opacity-90">Pantallas para gaming y trabajo</p>
          </div>
          <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-6 text-white text-center hover:from-green-600 hover:to-green-700 transition-colors cursor-pointer">
            <h3 className="font-semibold mb-2">Accesorios</h3>
            <p className="text-sm opacity-90">Teclados, mouse y más</p>
          </div>
          <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg p-6 text-white text-center hover:from-orange-600 hover:to-orange-700 transition-colors cursor-pointer">
            <h3 className="font-semibold mb-2">Impresoras</h3>
            <p className="text-sm opacity-90">Soluciones de impresión</p>
          </div>
        </div>
      </section>
    </div>
  );
};
