import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Trash2, Plus, Minus, ShoppingBag, ArrowLeft } from 'lucide-react';
import { useCart } from '../contexts/CartContext';

export const CartView: React.FC = () => {
  const navigate = useNavigate();
  const { state, removeItem, updateQuantity, clearCart } = useCart();

  const handleQuantityChange = (productId: number, newQuantity: number) => {
    if (newQuantity >= 1) {
      updateQuantity(productId, newQuantity);
    }
  };

  const handleRemoveItem = (productId: number) => {
    removeItem(productId);
  };

  const handleClearCart = () => {
    if (window.confirm('¿Estás seguro de que quieres vaciar el carrito?')) {
      clearCart();
    }
  };

  const handleCheckout = () => {
    // Aquí iría la lógica para proceder al checkout
    alert('Funcionalidad de checkout próximamente disponible');
  };

  if (state.items.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <button
                onClick={() => navigate('/')}
                className="flex items-center text-gray-600 hover:text-gray-800"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Volver a la tienda
              </button>
              <h1 className="text-2xl font-bold text-gray-900">Carrito de Compras</h1>
              <div className="w-24"></div> {/* Spacer */}
            </div>
          </div>
        </div>

        {/* Empty Cart */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <ShoppingBag className="w-24 h-24 text-gray-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Tu carrito está vacío</h2>
            <p className="text-gray-600 mb-8">¡Empieza a agregar productos para comenzar tu compra!</p>
            <button
              onClick={() => navigate('/')}
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Explorar Productos
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate('/')}
              className="flex items-center text-gray-600 hover:text-gray-800"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Volver a la tienda
            </button>
            <h1 className="text-2xl font-bold text-gray-900">Carrito de Compras</h1>
            <button
              onClick={handleClearCart}
              className="flex items-center text-red-600 hover:text-red-800"
            >
              <Trash2 className="w-5 h-5 mr-2" />
              Vaciar carrito
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="lg:grid lg:grid-cols-12 lg:gap-x-12 lg:items-start">
          {/* Cart Items */}
          <div className="lg:col-span-7">
            <div className="bg-white rounded-lg shadow-sm">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">
                  Productos ({state.itemCount} {state.itemCount === 1 ? 'artículo' : 'artículos'})
                </h2>
              </div>
              
              <div className="divide-y divide-gray-200">
                {state.items.map((item) => (
                  <div key={item.id} className="p-6">
                    <div className="flex items-center">
                      {/* Product Image */}
                      <div className="flex-shrink-0 w-24 h-24 bg-gray-100 rounded-lg overflow-hidden">
                        {item.product.image_url ? (
                          <img
                            src={item.product.image_url}
                            alt={item.product.name}
                            className="w-full h-full object-cover"
                            onError={(e) => {
                              e.currentTarget.src = 'https://via.placeholder.com/100x100/e5e7eb/6b7280?text=Sin+Imagen';
                            }}
                          />
                        ) : (
                          <div className="w-full h-full flex items-center justify-center text-gray-400">
                            <ShoppingBag className="w-8 h-8" />
                          </div>
                        )}
                      </div>

                      {/* Product Details */}
                      <div className="ml-6 flex-1">
                        <div className="flex justify-between">
                          <div className="pr-6">
                            <h3 className="text-lg font-medium text-gray-900 mb-1">
                              {item.product.name}
                            </h3>
                            <p className="text-sm text-gray-600 mb-2">
                              Marca: {item.product.brand}
                            </p>
                            <p className="text-lg font-semibold text-blue-600">
                              S/ {item.product.price.toFixed(2)}
                            </p>
                          </div>
                          
                          <div className="flex flex-col items-end space-y-2">
                            {/* Price */}
                            <p className="text-lg font-bold text-gray-900">
                              S/ {(item.product.price * item.quantity).toFixed(2)}
                            </p>
                            
                            {/* Quantity Controls */}
                            <div className="flex items-center border border-gray-300 rounded-lg">
                              <button
                                onClick={() => handleQuantityChange(item.product.id, item.quantity - 1)}
                                className="p-2 hover:bg-gray-100 text-gray-600"
                                disabled={item.quantity <= 1}
                              >
                                <Minus className="w-4 h-4" />
                              </button>
                              <span className="px-4 py-2 min-w-16 text-center font-medium">
                                {item.quantity}
                              </span>
                              <button
                                onClick={() => handleQuantityChange(item.product.id, item.quantity + 1)}
                                className="p-2 hover:bg-gray-100 text-gray-600"
                                disabled={item.quantity >= item.product.stock_quantity}
                              >
                                <Plus className="w-4 h-4" />
                              </button>
                            </div>
                            
                            {/* Remove Button */}
                            <button
                              onClick={() => handleRemoveItem(item.product.id)}
                              className="flex items-center text-red-600 hover:text-red-800 text-sm"
                            >
                              <Trash2 className="w-4 h-4 mr-1" />
                              Eliminar
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-5 mt-8 lg:mt-0">
            <div className="bg-white rounded-lg shadow-sm p-6 sticky top-8">
              <h2 className="text-lg font-medium text-gray-900 mb-6">Resumen del pedido</h2>
              
              <div className="space-y-4">
                <div className="flex justify-between text-base">
                  <p>Subtotal ({state.itemCount} {state.itemCount === 1 ? 'artículo' : 'artículos'})</p>
                  <p className="font-medium">S/ {state.total.toFixed(2)}</p>
                </div>
                
                <div className="flex justify-between text-base">
                  <p>Envío</p>
                  <p className="font-medium">Gratis</p>
                </div>
                
                <div className="flex justify-between text-base">
                  <p>Impuestos estimados</p>
                  <p className="font-medium">S/ {(state.total * 0.18).toFixed(2)}</p>
                </div>
                
                <div className="border-t border-gray-200 pt-4">
                  <div className="flex justify-between text-lg font-bold">
                    <p>Total</p>
                    <p>S/ {(state.total * 1.18).toFixed(2)}</p>
                  </div>
                </div>
              </div>
              
              <button
                onClick={handleCheckout}
                className="w-full mt-6 bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                Proceder al pago
              </button>
              
              <div className="mt-6 text-center">
                <p className="text-sm text-gray-600">
                  o{' '}
                  <button
                    onClick={() => navigate('/')}
                    className="text-blue-600 hover:text-blue-800 underline"
                  >
                    continuar comprando
                  </button>
                </p>
              </div>
              
              {/* Security badges */}
              <div className="mt-6 pt-6 border-t border-gray-200">
                <p className="text-xs text-gray-500 text-center mb-2">Compra 100% segura</p>
                <div className="flex justify-center space-x-2">
                  <div className="bg-gray-100 px-2 py-1 rounded text-xs font-medium">
                    SSL
                  </div>
                  <div className="bg-gray-100 px-2 py-1 rounded text-xs font-medium">
                    Visa
                  </div>
                  <div className="bg-gray-100 px-2 py-1 rounded text-xs font-medium">
                    Mastercard
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
