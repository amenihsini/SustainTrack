<template>
  <div>
    <h2>Delete Product</h2>
    <form @submit.prevent="deleteProduct">
      <label for="productId">Product ID:</label>
      <input type="text" v-model="productId" required>
      
      <button type="submit">Delete Product</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      productId: '',
    };
  },
  methods: {
    async deleteProduct() {
      try {
        const response = await axios.delete(`http://localhost:8000/products/${this.productId}`);
        console.log('Product deleted successfully:', response.data);
        
        // Optionally, emit an event to notify the parent (App.vue) to update the product list
        this.$emit('product-deleted');
        
        // Reset form fields
        this.productId = '';
      } catch (error) {
        console.error('Error deleting product:', error);
      }
    },
  },
};
</script>
