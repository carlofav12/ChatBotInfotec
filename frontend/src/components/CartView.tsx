import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Trash2, Plus, Minus, ShoppingBag, ArrowLeft, Truck, Receipt } from 'lucide-react';
import { useCart } from '../contexts/CartContext';


export const CartView: React.FC = () => {
  const navigate = useNavigate();
  const { state, removeItem, updateQuantity, clearCart } = useCart();

  const handleQuantityChange = (productId: number, newQuantity: number) => {
    if (newQuantity >= 1) updateQuantity(productId, newQuantity);
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
    alert('Funcionalidad de checkout próximamente disponible');
  };

  const gradientHeader = "bg-gradient-to-r from-[#002855] via-[#003f7f] to-[#001F3F]";
  const accentColor = "text-[#FFD100]";
  const buttonColor = "bg-[#FFD100] text-[#002855] hover:bg-yellow-400";
  const emptyCart = state.items.length === 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 via-white to-gray-100 font-nunito">
      {/* Header */}
      <div className={`${gradientHeader} shadow`}>
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between text-black">
          <button onClick={() => navigate('/')} className="flex items-center hover:text-[#FFD100]">
            <ArrowLeft className="w-5 h-5 mr-2" />
            Volver a la tienda
          </button>
          <h1 className="text-3xl font-bold text-white">Carrito de Compras</h1>
          {!emptyCart && (
            <button onClick={handleClearCart} className="flex items-center text-red-300 hover:text-red-500">
              <Trash2 className="w-5 h-5 mr-2" />
              Vaciar carrito
            </button>
          )}
        </div>
      </div>

      {/* Carrito vacío */}
      {emptyCart ? (
        <div className="max-w-7xl mx-auto px-4 py-20 text-center">
          <ShoppingBag className="w-24 h-24 text-gray-400 mx-auto mb-4" />
          <h2 className="text-3xl font-bold text-gray-800 mb-2">Tu Carrito está Vacío</h2>
          <p className="text-gray-600 mb-8">¡Empieza a agregar productos para comenzar tu compra!</p>
          <button
            onClick={() => navigate('/')}
            className={`${buttonColor} px-6 py-3 rounded-full font-semibold transition shadow-lg`}
          >
            Explorar Productos
          </button>
        </div>
      ) : (
        <div className="max-w-7xl mx-auto px-4 py-10">
          <div className="lg:grid lg:grid-cols-12 lg:gap-10">
            {/* Lista de productos */}
            <div className="lg:col-span-7">
              <div className="bg-white rounded-2xl shadow-xl p-8 space-y-6 border border-gray-200">
                <h2 className="text-2xl font-bold text-[#002855] mb-4">
                  Productos ({state.itemCount} {state.itemCount === 1 ? 'artículo' : 'artículos'})
                </h2>
                {state.items.map((item) => (
                  <div key={item.id} className="flex items-center gap-6 border-b pb-6">
                    {/* Imagen */}
                    <div className="w-28 h-28 bg-gray-100 rounded-xl overflow-hidden flex items-center justify-center">
                      {item.product.image_url ? (
                        <img
                          src={item.product.image_url}
                          alt={item.product.name}
                          className="object-cover w-full h-full"
                          onError={(e) => {
                            e.currentTarget.src = 'https://via.placeholder.com/100x100/e5e7eb/6b7280?text=Sin+Imagen';
                          }}
                        />
                      ) : (
                        <ShoppingBag className="w-10 h-10 text-gray-400" />
                      )}
                    </div>

                    {/* Detalles */}
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-gray-900 mb-1">{item.product.name}</h3>
                      <p className="text-sm text-gray-500 mb-1">Marca: {item.product.brand}</p>
                      <p className="text-md font-semibold text-[#002855]">
                        S/ {item.product.price.toFixed(2)}
                      </p>
                    </div>

                    {/* Controles */}
                    <div className="flex flex-col items-end space-y-2">
                      <p className="font-bold text-gray-800">
                        S/ {(item.product.price * item.quantity).toFixed(2)}
                      </p>
                      <div className="flex border border-gray-300 rounded-lg overflow-hidden">
                        <button
                          onClick={() => handleQuantityChange(item.product.id, item.quantity - 1)}
                          disabled={item.quantity <= 1}
                          className="px-3 py-1 hover:bg-gray-200 text-gray-600"
                        >
                          <Minus className="w-4 h-4" />
                        </button>
                        <span className="px-4 py-1 text-sm font-medium">{item.quantity}</span>
                        <button
                          onClick={() => handleQuantityChange(item.product.id, item.quantity + 1)}
                          disabled={item.quantity >= item.product.stock_quantity}
                          className="px-3 py-1 hover:bg-gray-200 text-gray-600"
                        >
                          <Plus className="w-4 h-4" />
                        </button>
                      </div>
                      <button
                        onClick={() => handleRemoveItem(item.product.id)}
                        className="text-red-600 hover:text-red-800 text-sm flex items-center"
                      >
                        <Trash2 className="w-4 h-4 mr-1" />
                        Eliminar
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Resumen del pedido (Diseño renovado) */}
            <div className="lg:col-span-5 mt-10 lg:mt-0">
              <div className="bg-gradient-to-tr from-[#002855] via-[#003f7f] to-[#001F3F] text-white rounded-3xl shadow-2xl p-8 sticky top-8 border border-[#001f3f]/30">
                <h2 className="text-3xl font-extrabold mb-6 text-center">Resumen del Pedido</h2>

                <div className="space-y-5 text-md">
                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-2">
                      <ShoppingBag className="w-5 h-5 text-yellow-300" />
                      <p>Subtotal</p>
                    </div>
                    <p className="font-semibold text-yellow-300">S/ {state.total.toFixed(2)}</p>
                  </div>

                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-2">
                      <Truck className="w-5 h-5 text-green-400" />
                      <p>Envío</p>
                    </div>
                    <p className="font-semibold text-green-400">Gratis</p>
                  </div>

                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-2">
                      <Receipt className="w-5 h-5 text-blue-200" />
                      <p>IGV (18%)</p>
                    </div>
                    <p className="text-blue-200">S/ {(state.total * 0.18).toFixed(2)}</p>
                  </div>

                  <hr className="border-gray-400/30 my-4" />

                  <div className="flex justify-between items-center text-xl font-bold">
                    <p>Total</p>
                    <p className="text-yellow-300">S/ {(state.total * 1.18).toFixed(2)}</p>
                  </div>
                </div>

                <button
                  onClick={handleCheckout}
                  className="w-full mt-8 py-4 px-4 bg-[#FFD100] hover:bg-yellow-400 text-[#002855] text-lg font-bold rounded-full shadow-lg transition-all duration-300"
                >
                  Proceder al Pago
                </button>

                <p className="mt-4 text-sm text-center text-white/80">
                  o{' '}
                  <button onClick={() => navigate('/')} className="underline hover:text-yellow-300">
                    seguir comprando
                  </button>
                </p>

                <div className="mt-8 text-center text-xs text-white/60">
                  <p>Compra protegida y segura</p>
                  <div className="flex justify-center gap-3 mt-3">
                    <div className="bg-white/10 px-3 py-1 rounded-full">SSL</div>
                    <div className="bg-white/10 px-3 py-1 rounded-full">Visa</div>
                    <div className="bg-white/10 px-3 py-1 rounded-full">Mastercard</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};