// ProductDetail.tsx
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchProductById } from '../services/api';
import { useChat } from '../hooks/useChat';
import { useCart } from '../contexts/CartContext';

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

  const { updateCurrentPage, updateCurrentProduct } = useChat();
  const { addItem } = useCart();

  useEffect(() => {
    const getProduct = async () => {
      try {
        setLoading(true);
        const productId = parseInt(id || '0', 10);
        if (productId <= 0) throw new Error('ID de producto inválido');
        const data = await fetchProductById(productId);
        setProduct(data);
        updateCurrentPage('product_detail');
        updateCurrentProduct(productId);
      } catch (err) {
        console.error('Error al cargar el producto:', err);
        setError('No se pudo cargar el producto.');
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
      addItem(product, quantity);
      const goToCart = window.confirm('Producto agregado al carrito. ¿Ir al carrito?');
      if (goToCart) navigate('/cart');
    } catch (err) {
      setError('No se pudo agregar al carrito.');
    } finally {
      setAddingToCart(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-[#003f7f]"></div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
          <strong>Error:</strong> {error || 'Producto no encontrado'}
        </div>
        <button
          onClick={() => navigate('/')}
          className="mt-4 bg-[#003f7f] hover:bg-[#001F3F] text-white font-bold py-2 px-4 rounded"
        >
          Volver al inicio
        </button>
      </div>
    );
  }

  const discountPercentage = product.original_price
    ? Math.round(((product.original_price - product.price) / product.original_price) * 100)
    : 0;

  let specifications = {};
  try {
    specifications =
      typeof product.specifications === 'string'
        ? JSON.parse(product.specifications)
        : product.specifications;
  } catch (e) {
    console.error('Error al parsear especificaciones:', e);
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Imagen centrada arriba */}
      <div className="flex justify-center mb-6">
        <div className="w-full max-w-md bg-gray-100 rounded-lg overflow-hidden shadow-lg">
          {product.image_url ? (
            <img
              src={product.image_url.startsWith('/api') ? 'https://via.placeholder.com/400x300' : product.image_url}
              alt={product.name}
              className="w-full object-contain h-72"
            />
          ) : (
            <div className="p-10 text-center text-gray-400">Imagen no disponible</div>
          )}
        </div>
      </div>

      {/* Contenido debajo de la imagen */}
      <div className="bg-white text-black shadow-lg rounded-lg p-6">
        <h2 className="text-3xl font-bold mb-2">{product.name}</h2>
        <div className="flex items-center mb-4">
          {[...Array(5)].map((_, i) => (
            <svg
              key={i}
              className={`w-5 h-5 ${i < Math.round(product.rating) ? 'text-yellow-400' : 'text-gray-300'}`}
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          ))}
          <span className="ml-2 text-sm text-gray-600">({product.review_count} reseñas)</span>
        </div>

        <div className="flex items-center text-2xl font-bold text-[#002855] mb-2">
          S/ {product.price.toFixed(2)}
          {discountPercentage > 0 && (
            <>
              <span className="text-lg line-through text-gray-500 ml-4">
                S/ {product.original_price?.toFixed(2)}
              </span>
              <span className="ml-3 px-2 py-1 bg-red-600 text-white text-sm font-semibold rounded">
                {discountPercentage}% OFF
              </span>
            </>
          )}
        </div>

        <p className={`text-sm ${product.stock_quantity > 0 ? 'text-green-600' : 'text-red-600'} mb-4`}>
          {product.stock_quantity > 0 ? `En stock: ${product.stock_quantity}` : 'Agotado'}
        </p>

        <p><span className="font-semibold">Marca:</span> {product.brand}</p>
        <p><span className="font-semibold">Modelo:</span> {product.model}</p>

        <div className="my-4">
          <label className="block text-gray-800 font-bold mb-2" htmlFor="quantity">
            Cantidad
          </label>
          <div className="flex items-center">
            <button
              onClick={() => quantity > 1 && setQuantity(quantity - 1)}
              className="bg-gray-300 h-10 w-10 rounded-l text-2xl"
              disabled={quantity <= 1}
            >−</button>
            <input
              type="number"
              value={quantity}
              onChange={handleQuantityChange}
              className="text-center h-10 w-16 border-t border-b border-gray-300"
              min={1}
              max={product.stock_quantity}
            />
            <button
              onClick={() => quantity < product.stock_quantity && setQuantity(quantity + 1)}
              className="bg-gray-300 h-10 w-10 rounded-r text-2xl"
              disabled={quantity >= product.stock_quantity}
            >+</button>
          </div>
        </div>

        <div className="mb-4">
          <h3 className="text-lg font-bold mb-1">Descripción</h3>
          <p className="text-gray-800">{product.description}</p>
        </div>

        {Object.keys(specifications).length > 0 && (
          <div className="mb-4">
            <h3 className="text-lg font-bold mb-1">Especificaciones</h3>
            <ul className="list-disc list-inside text-gray-700">
              {Object.entries(specifications).map(([key, value]) => (
                <li key={key}>
                  <span className="font-semibold capitalize">{key.replace('_', ' ')}</span>: {String(value)}
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="flex flex-col md:flex-row gap-4 mt-6">
          <button
            onClick={() => navigate('/')}
            className="w-full md:w-1/2 bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 rounded-full"
          >
            Volver
          </button>
          <button
            onClick={addToCart}
            disabled={addingToCart || product.stock_quantity <= 0}
            className={`w-full md:w-1/2 py-2 rounded-full font-bold ${
              product.stock_quantity <= 0
                ? 'bg-gray-400 cursor-not-allowed text-white'
                : 'bg-[#003f7f] hover:bg-[#001F3F] text-white'
            }`}
          >
            {addingToCart ? 'Agregando...' : 'Agregar al Carrito'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;
