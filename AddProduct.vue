<template>
  <div>
    <h2>Add Product</h2>
    <form @submit.prevent="addProduct">
      <label for="name">Name:</label>
      <input type="text" v-model="productName" required>
      
      <label for="price">Price:</label>
      <input type="number" v-model="productPrice" required>
      
      <label for="expirationDate">Expiration Date:</label>
      <input type="date" v-model="productExpirationDate" required>
      
      <label for="quantityInStock">Quantity in Stock:</label>
      <input type="number" v-model="productQuantityInStock" required>

      <button type="submit">Add Product</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      productName: '',
      productPrice: 0,
      productExpirationDate: '',
      productQuantityInStock: 0,
    };
  },
  methods: {
    async addProduct() {
      try {
        const response = await axios.post('http://localhost:8000/products', {
          name: this.productName,
          price: this.productPrice,
          expiration_date: this.productExpirationDate,
          quantity_in_stock: this.productQuantityInStock,
        });
        console.log('Product added successfully:', response.data);
        // Optionally, update the product list after adding
        this.$emit('product-added');
        // Reset form fields
        this.productName = '';
        this.productPrice = 0;
        this.productExpirationDate = '';
        this.productQuantityInStock = 0;
      } catch (error) {
        console.error('Error adding product:', error);
      }
    },
  },
};
</script>
