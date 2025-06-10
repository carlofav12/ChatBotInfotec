import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchProductById } from '../services/api';
import { useChat } from '../hooks/useChat';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  original_price?: number;
  brand: string;
  model: string;
  specifications: any;
  image_url: string;
  rating: number;
  review_count: number;
  stock_quantity: number;
  is_featured: boolean;
  category_id: number;
}

const ProductDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [quantity, setQuantity] = useState<number>(1);
  const [addingToCart, setAddingToCart] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  // Usar el hook de chat para actualizar el contexto
  const { updateCurrentPage, updateCurrentProduct } = useChat();  useEffect(() => {
    const getProduct = async () => {
      try {
        setLoading(true);
        // Asegúrate de que el ID sea un número
        const productId = parseInt(id || '0', 10);
        if (productId <= 0) {
          throw new Error('ID de producto inválido');
        }

        const data = await fetchProductById(productId);
        setProduct(data);
        
        // Actualizar el contexto del chatbot cuando se carga un producto
        updateCurrentPage('product_detail');
        updateCurrentProduct(productId);
      } catch (err) {
        console.error('Error al cargar el producto:', err);
        setError('No se pudo cargar el producto. Por favor, inténtalo de nuevo.');
      } finally {
        setLoading(false);
      }
    };

    getProduct();
  }, [id, updateCurrentPage, updateCurrentProduct]);

  const handleQuantityChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value, 10);
    if (value > 0 && product && value <= product.stock_quantity) {
      setQuantity(value);
    }
  };

  const addToCart = async () => {
    if (!product) return;
    
    try {
      setAddingToCart(true);
      // Aquí iría la llamada a la API para agregar al carrito
      // Por ahora simulamos un retardo
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Mostrar mensaje de éxito
      alert(`Se agregaron ${quantity} unidad(es) de ${product.name} al carrito`);
      
      // Opcional: redirigir al carrito o mantener al usuario en la página
    } catch (err) {
      console.error('Error al agregar al carrito:', err);
      setError('No se pudo agregar al carrito. Por favor, inténtalo de nuevo.');
    } finally {
      setAddingToCart(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Error: </strong>
          <span className="block sm:inline">{error || 'Producto no encontrado'}</span>
        </div>
        <button 
          onClick={() => navigate('/')}
          className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Volver al inicio
        </button>
      </div>
    );
  }

  // Calcular descuento si existe
  const discountPercentage = product.original_price 
    ? Math.round(((product.original_price - product.price) / product.original_price) * 100) 
    : 0;

  // Parsear especificaciones si están en formato JSON
  let specifications = {};
  try {
    if (typeof product.specifications === 'string') {
      specifications = JSON.parse(product.specifications);
    } else if (typeof product.specifications === 'object') {
      specifications = product.specifications;
    }
  } catch (e) {
    console.error('Error al parsear especificaciones:', e);
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex flex-col md:flex-row -mx-4">
        {/* Imagen del producto */}
        <div className="md:flex-1 px-4 mb-6 md:mb-0">
          <div className="h-64 md:h-80 rounded-lg bg-gray-100 mb-4 flex items-center justify-center">
            {product.image_url ? (
              <img 
                src={product.image_url.startsWith('/api') ? 'https://via.placeholder.com/400x300' : product.image_url} 
                alt={product.name}
                className="max-h-full" 
              />
            ) : (
              <div className="text-center p-5 text-gray-500">
                <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p>Imagen no disponible</p>
              </div>
            )}
          </div>
          
          <div className="flex -mx-2 mb-4">
            <div className="w-1/2 px-2">
              <button 
                onClick={() => navigate('/')}
                className="w-full bg-gray-400 text-white py-2 px-4 rounded-full font-bold hover:bg-gray-500"
              >
                Volver
              </button>
            </div>
            <div className="w-1/2 px-2">
              <button 
                onClick={addToCart}
                disabled={addingToCart || product.stock_quantity <= 0}
                className={`w-full py-2 px-4 rounded-full font-bold ${
                  product.stock_quantity <= 0 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-blue-500 hover:bg-blue-700 text-white'
                }`}
              >
                {addingToCart ? 'Agregando...' : product.stock_quantity <= 0 ? 'Sin stock' : 'Agregar al carrito'}
              </button>
            </div>
          </div>
        </div>
        
        {/* Detalles del producto */}
        <div className="md:flex-1 px-4">
          <h2 className="text-2xl font-bold mb-2">{product.name}</h2>
          <div className="flex items-center mb-4">
            <div className="flex">
              {[...Array(5)].map((_, i) => (
                <svg 
                  key={i}
                  className={`w-5 h-5 ${i < Math.round(product.rating) ? 'text-yellow-500' : 'text-gray-300'}`}
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              ))}
            </div>
            <span className="text-gray-600 ml-2">({product.review_count} reseñas)</span>
          </div>
          
          <div className="mb-4">
            <div className="flex items-center">
              <span className="text-3xl font-bold text-blue-600">S/ {product.price.toFixed(2)}</span>
              {discountPercentage > 0 && (
                <>
                  <span className="text-lg text-gray-500 line-through ml-2">
                    S/ {product.original_price?.toFixed(2)}
                  </span>
                  <span className="ml-2 px-2 py-1 bg-red-500 text-white text-xs font-bold rounded">
                    {discountPercentage}% OFF
                  </span>
                </>
              )}
            </div>
            <div className="text-green-600 mt-1">
              {product.stock_quantity > 0 ? (
                <span>En stock: {product.stock_quantity} unidades</span>
              ) : (
                <span className="text-red-600">Agotado</span>
              )}
            </div>
          </div>
          
          <div className="mb-4">
            <span className="font-bold text-gray-700">Marca: </span>
            <span className="text-gray-600">{product.brand}</span>
          </div>
          
          <div className="mb-4">
            <span className="font-bold text-gray-700">Modelo: </span>
            <span className="text-gray-600">{product.model}</span>
          </div>
          
          <div className="mb-4">
            <label className="block text-gray-700 font-bold mb-2" htmlFor="quantity">
              Cantidad
            </label>
            <div className="flex items-center">
              <button 
                onClick={() => quantity > 1 && setQuantity(quantity - 1)}
                className="bg-gray-300 text-gray-600 hover:bg-gray-400 h-10 w-10 rounded-l cursor-pointer"
                disabled={quantity <= 1}
              >
                <span className="m-auto text-2xl font-thin">−</span>
              </button>
              <input 
                type="number" 
                id="quantity"
                className="h-10 w-16 text-center border-t border-b border-gray-300"
                value={quantity}
                onChange={handleQuantityChange}
                min="1"
                max={product.stock_quantity}
                disabled={product.stock_quantity <= 0}
              />
              <button 
                onClick={() => quantity < product.stock_quantity && setQuantity(quantity + 1)}
                className="bg-gray-300 text-gray-600 hover:bg-gray-400 h-10 w-10 rounded-r cursor-pointer"
                disabled={quantity >= product.stock_quantity}
              >
                <span className="m-auto text-2xl font-thin">+</span>
              </button>
            </div>
          </div>
          
          <div className="mb-4">
            <h3 className="text-xl font-bold mb-2">Descripción</h3>
            <p className="text-gray-600">{product.description}</p>
          </div>
          
          {Object.keys(specifications).length > 0 && (
            <div className="mb-4">
              <h3 className="text-xl font-bold mb-2">Especificaciones</h3>
              <ul className="list-disc list-inside text-gray-600">                {Object.entries(specifications).map(([key, value]) => (
                  <li key={key}>
                    <span className="font-semibold capitalize">{key.replace('_', ' ')}</span>: {String(value)}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;
