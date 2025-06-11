import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ShoppingCart } from "lucide-react";
import { useCart } from "../../contexts/CartContext";

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

export const ProductSections: React.FC = () => {
  const navigate = useNavigate();
  const { addItem } = useCart();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const handleAddToCart = (product: Product, e: React.MouseEvent) => {
    e.stopPropagation();
    addItem(product, 1);
  };

  const handleProductClick = (productId: number) => {
    navigate(`/product/${productId}`);
  };

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const response = await fetch("http://localhost:8000/api/products?limit=100");
        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        const data = await response.json();
        const formattedProducts: Product[] = data.map((item: any) => ({
          id: item.id,
          name: item.name,
          price: item.price,
          original_price: item.original_price,
          image_url: item.image_url,
          rating: item.rating || 0,
          stock_quantity: item.stock_quantity || 0,
          brand: item.brand,
        }));

        setProducts(formattedProducts);
        setError(null);
      } catch (error) {
        console.error("Error al cargar productos:", error);
        setError("Error al cargar productos. Por favor, intenta de nuevo.");
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return (
    <div className="bg-white py-16 mb-24 font-nunito">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-3xl font-bold text-[#002855] mb-8 text-center">
          Nuestros Productos
        </h2>

        {loading && (
          <div className="grid gap-6 grid-cols-1 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
            {[...Array(8)].map((_, index) => (
              <div key={index} className="bg-gray-100 rounded-lg shadow p-4 animate-pulse">
                <div className="bg-gray-300 h-48 rounded mb-4"></div>
                <div className="bg-gray-300 h-4 rounded mb-2"></div>
                <div className="bg-gray-300 h-4 rounded w-2/3"></div>
              </div>
            ))}
          </div>
        )}

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded text-center">
            {error}
          </div>
        )}

        {!loading && !error && (
          <div className="grid gap-6 grid-cols-1 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
            {products.map((product) => (
              <div
                key={product.id}
                className="bg-white rounded-lg shadow border p-4 flex flex-col cursor-pointer hover:shadow-lg transition-shadow"
                onClick={() => handleProductClick(product.id)}
              >
                <img
                  src={product.image_url}
                  alt={product.name}
                  className="w-full h-48 object-cover rounded"
                  onError={(e) => {
                    e.currentTarget.src =
                      "https://via.placeholder.com/300x200/e5e7eb/6b7280?text=Sin+Imagen";
                  }}
                />
                <h3 className="mt-4 font-semibold text-black text-sm line-clamp-2">
                  {product.name}
                </h3>
                <div className="mt-2 flex items-center justify-between">
                  <span className="text-[#002855] font-bold text-base">
                    S/ {product.price.toFixed(2)}
                  </span>
                  <button
                    onClick={(e) => handleAddToCart(product, e)}
                    className="bg-[#FFD100] text-[#002855] p-2 rounded hover:bg-yellow-400 transition"
                    title="Agregar al carrito"
                  >
                    <ShoppingCart className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {!loading && !error && products.length === 0 && (
          <div className="text-center py-10">
            <p className="text-gray-500">No se encontraron productos.</p>
          </div>
        )}
      </div>
    </div>
  );
};
