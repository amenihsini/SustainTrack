<template>
  <div>
    <h2>Product List</h2>
    <ul>
      <li v-for="product in products" :key="product.product_id">
        {{ product.product_id }} - {{ product.name }} - Price: {{ product.price }} - Quantity: {{ product.quantity_in_stock }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      products: [],
    };
  },
  mounted() {
    this.fetchProducts();
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('http://localhost:8000/products');
        this.products = response.data;
        console.log('Products fetched successfully:', this.products);
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    },
  },
};
</script>

