import React, { useEffect, useState } from "react";
import { ShoppingCart } from "lucide-react";

interface Product {
  id: number;
  name: string;
  price: number;
  image: string;
}

export const ProductSections: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/products")
      .then((res) => res.json())
      .then((data) => {
        const formattedProducts: Product[] = data.map((item: any) => ({
          id: item.id,
          name: item.name,
          price: item.price,
          image: item.image_url,
        }));
        setProducts(formattedProducts);
      })
      .catch((error) => console.error("Error al cargar productos:", error));
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 py-10 grid gap-6 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
      {products.map((product) => (
        <div
          key={product.id}
          className="bg-white rounded-lg shadow border p-4 flex flex-col"
        >
          <img
            src={product.image}
            alt={product.name}
            className="w-full h-48 object-cover rounded"
          />
          <h3 className="mt-4 font-semibold text-gray-800 text-sm line-clamp-2">
            {product.name}
          </h3>
          <div className="mt-2 flex items-center justify-between">
            <span className="text-blue-600 font-bold text-base">
              S/ {product.price}
            </span>
            <button className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700 transition">
              <ShoppingCart className="w-4 h-4" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};
