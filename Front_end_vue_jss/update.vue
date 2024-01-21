<template>
    <div>
      <h2>Update Product</h2>
      <form @submit.prevent="updateProduct">
        <label for="productId">Product ID:</label>
        <input type="text" v-model="productId" required>
        
        <label for="name">New Name:</label>
        <input type="text" v-model="newProductName" required>
        
        <label for="price">New Price:</label>
        <input type="number" v-model="newProductPrice" required>
        
        <label for="expirationDate">New Expiration Date:</label>
        <input type="date" v-model="newProductExpirationDate" required>
        
        <label for="quantityInStock">New Quantity in Stock:</label>
        <input type="number" v-model="newProductQuantityInStock" required>
  
        <button type="submit">Update Product</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        productId: '',
        newProductName: '',
        newProductPrice: 0,
        newProductExpirationDate: '',
        newProductQuantityInStock: 0,
      };
    },
    methods: {
      async updateProduct() {
        try {
          const response = await axios.put(`http://localhost:8000/products/${this.productId}`, {
            name: this.newProductName,
            price: this.newProductPrice,
            expiration_date: this.newProductExpirationDate,
            quantity_in_stock: this.newProductQuantityInStock,
          });
          console.log('Product updated successfully:', response.data);
          // Optionally, update the product list after updating
          this.$emit('product-updated');
          // Reset form fields
          this.productId = '';
          this.newProductName = '';
          this.newProductPrice = 0;
          this.newProductExpirationDate = '';
          this.newProductQuantityInStock = 0;
        } catch (error) {
          console.error('Error updating product:', error);
        }
      },
    },
  };
  </script>
  
