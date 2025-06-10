import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useChat } from '../hooks/useChat';

interface Product {
  id: number;
  name: string;
  price: number;
  original_price?: number;
  image_url: string;
  rating: number;
  stock_quantity: number;
  brand: string;
}

interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const navigate = useNavigate();
  const { updateCurrentProduct } = useChat();
  
  // Calcular descuento si existe
  const discountPercentage = product.original_price 
    ? Math.round(((product.original_price - product.price) / product.original_price) * 100) 
    : 0;
    
  const handleClick = () => {
    // Actualizar el contexto antes de navegar a la página del producto
    updateCurrentProduct(product.id);
    navigate(`/product/${product.id}`);
  };
  
  return (
    <div 
      className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200 hover:shadow-lg transition-shadow duration-300 cursor-pointer"
      onClick={handleClick}
    >
      <div className="h-32 bg-gray-100 flex items-center justify-center">
        {product.image_url ? (
          <img 
            src={product.image_url.startsWith('/api') ? 'https://via.placeholder.com/150x100' : product.image_url} 
            alt={product.name}
            className="max-h-full object-cover" 
          />
        ) : (
          <div className="text-center p-2 text-gray-400">
            <svg className="w-8 h-8 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        )}
      </div>
      
      <div className="p-3">
        <h3 className="text-sm font-medium text-gray-900 truncate" title={product.name}>
          {product.name.length > 40 ? product.name.substring(0, 40) + '...' : product.name}
        </h3>
        
        <div className="flex items-center mt-1">
          <div className="flex">
            {[...Array(5)].map((_, i) => (
              <svg 
                key={i}
                className={`w-3 h-3 ${i < Math.round(product.rating) ? 'text-yellow-500' : 'text-gray-300'}`}
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            ))}
          </div>
          <span className="text-xs text-gray-500 ml-1">({product.rating})</span>
        </div>
        
        <div className="mt-2 flex items-center justify-between">
          <div>
            <div className="text-sm font-semibold text-blue-600">S/ {product.price.toFixed(2)}</div>
            {discountPercentage > 0 && (
              <div className="flex items-center">
                <span className="text-xs text-gray-500 line-through">
                  S/ {product.original_price?.toFixed(2)}
                </span>
                <span className="ml-1 px-1 py-0.5 bg-red-500 text-white text-xs rounded">
                  -{discountPercentage}%
                </span>
              </div>
            )}
          </div>
          
          <span className="text-xs text-gray-500">
            {product.stock_quantity > 0 ? (
              <span className="text-green-600">En stock</span>
            ) : (
              <span className="text-red-600">Agotado</span>
            )}
          </span>
        </div>
      </div>
    </div>
  );
};

interface ProductCarouselProps {
  products: Product[];
}

const ProductCarousel: React.FC<ProductCarouselProps> = ({ products }) => {
  if (!products || products.length === 0) {
    return null;
  }
  
  return (
    <div className="my-2">
      <div className="grid grid-cols-2 gap-3">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
};

export default ProductCarousel;
