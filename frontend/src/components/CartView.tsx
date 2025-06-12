import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Trash2, Plus, Minus, ShoppingBag, ArrowLeft, Truck, Receipt, Shield, CreditCard } from 'lucide-react';
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

  const gradientHeader = "bg-gradient-to-r from-[#003366] via-[#004d99] to-[#002244]";
  const accentColor = "text-[#F36A21]";
  const buttonColor = "bg-[#F36A21] text-white hover:bg-orange-600";
  const emptyCart = state.items.length === 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100">
      {/* Header con mejor espaciado */}
      <div className={`${gradientHeader} shadow-lg`}>
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate('/')}
              className="flex items-center text-white hover:text-[#F36A21] transition-colors duration-200 group"
            >
              <ArrowLeft className="w-5 h-5 mr-3 group-hover:-translate-x-1 transition-transform duration-200" />
              <span className="font-medium">Volver a la tienda</span>
            </button>

            <div className="text-center">
              <h1 className="text-4xl font-bold text-white mb-1">Carrito de Compras</h1>
              {!emptyCart && (
                <p className="text-blue-200 text-sm">
                  {state.itemCount} {state.itemCount === 1 ? 'producto' : 'productos'} en tu carrito
                </p>
              )}
            </div>

            {!emptyCart && (
              <button
                onClick={handleClearCart}
                className="flex items-center text-red-200 hover:text-red-400 transition-colors duration-200 group"
              >
                <Trash2 className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform duration-200" />
                <span className="font-medium">Vaciar carrito</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Espaciado superior */}
      <div className="py-8"></div>

      {/* Carrito vacío mejorado */}
      {emptyCart ? (
        <div className="max-w-4xl mx-auto px-6">
          <div className="bg-white rounded-3xl shadow-xl p-16 text-center border border-gray-100">
            <div className="mb-8">
              <ShoppingBag className="w-32 h-32 text-gray-300 mx-auto mb-6" />
              <h2 className="text-4xl font-bold text-gray-800 mb-4">Tu Carrito está Vacío</h2>
              <p className="text-xl text-gray-500 mb-2">¡Descubre nuestros increíbles productos!</p>
              <p className="text-gray-400">Agrega algunos artículos para comenzar tu compra</p>
            </div>

            <div className="space-y-4">
              <button
                onClick={() => navigate('/')}
                className={`${buttonColor} px-8 py-4 rounded-full font-bold text-lg transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105`}
              >
                Explorar Productos
              </button>

              <div className="flex justify-center items-center gap-6 text-sm text-gray-400 mt-8">
                <div className="flex items-center gap-2">
                  <Shield className="w-4 h-4" />
                  <span>Compra segura</span>
                </div>
                <div className="flex items-center gap-2">
                  <Truck className="w-4 h-4" />
                  <span>Envío gratis</span>
                </div>
                <div className="flex items-center gap-2">
                  <CreditCard className="w-4 h-4" />
                  <span>Pago fácil</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="max-w-7xl mx-auto px-6 pb-12">
          <div className="lg:grid lg:grid-cols-12 lg:gap-12">

            {/* Lista de productos mejorada */}
            <div className="lg:col-span-7 space-y-6">
              {/* Header de productos */}
              <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                <div className="flex items-center justify-between">
                  <h2 className="text-2xl font-bold text-[#003366]">
                    Productos en tu carrito
                  </h2>
                  <div className="bg-[#F36A21]/10 text-[#F36A21] px-4 py-2 rounded-full font-semibold">
                    {state.itemCount} {state.itemCount === 1 ? 'artículo' : 'artículos'}
                  </div>
                </div>
              </div>

              {/* Productos */}
              <div className="space-y-4">
                {state.items.map((item, index) => (
                  <div key={item.id} className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-shadow duration-300">
                    <div className="flex items-center gap-6">
                      {/* Imagen del producto */}
                      <div className="w-32 h-32 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl overflow-hidden flex items-center justify-center shadow-inner">
                        {item.product.image_url ? (
                          <img
                            src={item.product.image_url}
                            alt={item.product.name}
                            className="object-cover w-full h-full hover:scale-105 transition-transform duration-300"
                            onError={(e) => {
                              e.currentTarget.src = 'https://via.placeholder.com/120x120/e5e7eb/6b7280?text=Sin+Imagen';
                            }}
                          />
                        ) : (
                          <ShoppingBag className="w-12 h-12 text-gray-400" />
                        )}
                      </div>

                      {/* Detalles del producto */}
                      <div className="flex-1 space-y-2">
                        <h3 className="text-xl font-bold text-gray-900">{item.product.name}</h3>
                        <p className="text-gray-500 bg-gray-50 px-3 py-1 rounded-full inline-block text-sm">
                          Marca: {item.product.brand}
                        </p>
                        <div className="flex items-center gap-4">
                          <p className="text-2xl font-bold text-[#003366]">
                            S/ {item.product.price.toFixed(2)}
                          </p>
                          <p className="text-sm text-gray-500">
                            Stock disponible: {item.product.stock_quantity}
                          </p>
                        </div>
                      </div>

                      {/* Controles de cantidad y total */}
                      <div className="flex flex-col items-end space-y-4">
                        {/* Precio total del item */}
                        <div className="text-right">
                          <p className="text-sm text-gray-500">Total por producto</p>
                          <p className="text-2xl font-bold text-[#F36A21]">
                            S/ {(item.product.price * item.quantity).toFixed(2)}
                          </p>
                        </div>

                        {/* Controles de cantidad */}
                        <div className="flex items-center border-2 border-gray-200 rounded-xl overflow-hidden bg-white shadow-sm">
                          <button
                            onClick={() => handleQuantityChange(item.product.id, item.quantity - 1)}
                            disabled={item.quantity <= 1}
                            className="px-4 py-2 hover:bg-gray-100 text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                          >
                            <Minus className="w-4 h-4" />
                          </button>
                          <span className="px-6 py-2 text-lg font-semibold bg-gray-50 min-w-[60px] text-center">
                            {item.quantity}
                          </span>
                          <button
                            onClick={() => handleQuantityChange(item.product.id, item.quantity + 1)}
                            disabled={item.quantity >= item.product.stock_quantity}
                            className="px-4 py-2 hover:bg-gray-100 text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                          >
                            <Plus className="w-4 h-4" />
                          </button>
                        </div>

                        {/* Botón eliminar */}
                        <button
                          onClick={() => handleRemoveItem(item.product.id)}
                          className="text-red-500 hover:text-red-700 text-sm flex items-center gap-2 bg-red-50 hover:bg-red-100 px-3 py-2 rounded-lg transition-colors duration-200"
                        >
                          <Trash2 className="w-4 h-4" />
                          Eliminar
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Resumen del pedido mejorado */}
            <div className="lg:col-span-5 mt-8 lg:mt-0">
              <div className="sticky top-8 space-y-6">

                {/* Resumen principal */}
                <div className="bg-gradient-to-br from-[#003366] via-[#004d99] to-[#002244] text-white rounded-3xl shadow-2xl p-8 border border-[#002244]/30">
                  <div className="text-center mb-8">
                    <h2 className="text-3xl font-bold mb-2">Resumen del Pedido</h2>
                    <div className="w-20 h-1 bg-[#F36A21] mx-auto rounded-full"></div>
                  </div>

                  <div className="space-y-6">
                    {/* Subtotal */}
                    <div className="flex justify-between items-center p-4 bg-white/10 rounded-xl">
                      <div className="flex items-center gap-3">
                        <ShoppingBag className="w-5 h-5 text-[#F36A21]" />
                        <span className="font-medium">Subtotal</span>
                      </div>
                      <span className="text-xl font-bold text-[#F36A21]">S/ {state.total.toFixed(2)}</span>
                    </div>

                    {/* Envío */}
                    <div className="flex justify-between items-center p-4 bg-white/10 rounded-xl">
                      <div className="flex items-center gap-3">
                        <Truck className="w-5 h-5 text-green-400" />
                        <span className="font-medium">Envío</span>
                      </div>
                      <div className="text-right">
                        <span className="text-lg font-bold text-green-400">Gratis</span>
                        <p className="text-xs text-green-200">Envío incluido</p>
                      </div>
                    </div>

                    {/* IGV */}
                    <div className="flex justify-between items-center p-4 bg-white/10 rounded-xl">
                      <div className="flex items-center gap-3">
                        <Receipt className="w-5 h-5 text-blue-300" />
                        <span className="font-medium">IGV (18%)</span>
                      </div>
                      <span className="text-lg font-semibold text-blue-300">S/ {(state.total * 0.18).toFixed(2)}</span>
                    </div>

                    {/* Separador */}
                    <div className="border-t border-white/20 pt-6">
                      <div className="flex justify-between items-center text-2xl font-bold">
                        <span>Total a Pagar</span>
                        <span className="text-[#F36A21]">S/ {(state.total * 1.18).toFixed(2)}</span>
                      </div>
                    </div>
                  </div>

                  {/* Botón de compra */}
                  <div className="mt-8 space-y-4">
                    <button
                      onClick={handleCheckout}
                      className="w-full py-4 px-6 bg-[#F36A21] hover:bg-orange-600 text-white text-xl font-bold rounded-2xl shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
                    >
                      Proceder al Pago
                    </button>

                    <p className="text-center text-white/80">
                      o{' '}
                      <button
                        onClick={() => navigate('/')}
                        className="underline hover:text-[#F36A21] transition-colors duration-200 font-medium"
                      >
                        seguir comprando
                      </button>
                    </p>
                  </div>
                </div>

                {/* Información de seguridad */}
                <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                  <div className="text-center">
                    <Shield className="w-8 h-8 text-green-500 mx-auto mb-3" />
                    <h3 className="font-bold text-gray-800 mb-2">Compra 100% Segura</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Tus datos están protegidos con encriptación SSL
                    </p>

                    <div className="flex justify-center gap-3">
                      <div className="bg-gray-100 px-3 py-2 rounded-lg text-xs font-medium text-gray-600">
                        SSL Seguro
                      </div>
                      <div className="bg-gray-100 px-3 py-2 rounded-lg text-xs font-medium text-gray-600">
                        Visa
                      </div>
                      <div className="bg-gray-100 px-3 py-2 rounded-lg text-xs font-medium text-gray-600">
                        Mastercard
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Espaciado inferior */}
      <div className="py-8"></div>
    </div>
  );
};