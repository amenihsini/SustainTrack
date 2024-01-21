<template>
    <div>
      <h2>Record Transaction</h2>
      <form @submit.prevent="recordTransaction">
        <label for="productId">Product ID:</label>
        <input type="text" v-model="productId" required>
        
        <label for="transactionType">Transaction Type (sale/purchase):</label>
        <input type="text" v-model="transactionType" required>
        
        <label for="quantity">Quantity:</label>
        <input type="number" v-model="quantity" required>
  
        <button type="submit">Record Transaction</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        productId: '',
        transactionType: '',
        quantity: 0,
      };
    },
    methods: {
      async recordTransaction() {
        try {
          const response = await axios.post(`http://localhost:8000/products/${this.productId}/${this.transactionType}`, {
            quantity_sold: this.transactionType === 'sale' ? this.quantity : 0,
            quantity_purchased: this.transactionType === 'purchase' ? this.quantity : 0,
          });
          console.log('Transaction recorded successfully:', response.data);
          // Optionally, update the product list after recording a transaction
          this.$emit('transaction-recorded');
          // Reset form fields
          this.productId = '';
          this.transactionType = '';
          this.quantity = 0;
        } catch (error) {
          console.error('Error recording transaction:', error);
        }
      },
    },
  };
  </script>
  
