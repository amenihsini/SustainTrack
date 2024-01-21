<template>
    <div id="app">
      <header>
        <h1 class="app-title">Product Management</h1>
      </header>
      <nav>
        <button @click="showProductList">View Products</button>
        <button @click="showAddProduct">Add Product</button>
        <button @click="showUpdateProduct">Update Product</button>
        <button @click="showDeleteProduct">Delete Product</button>
        <button @click="showRecordTransaction">Record Transaction</button>
      </nav>
      <main>
        <component :is="currentComponent" :key="componentKey" @product-list-updated="updateProductList" />
      </main>
      <footer>
        <ExpirationCheck />
      </footer>
    </div>
  </template>
  
  <script>
  import ProductList from './components/ProductList.vue';
  import AddProduct from './components/AddProduct.vue';
  import UpdateProduct from './components/UpdateProduct.vue';
  import DeleteProduct from './components/DeleteProduct.vue';
  import RecordTransaction from './components/RecordTransaction.vue';
  import ExpirationCheck from './components/ExpirationCheck.vue';
  
  export default {
    name: 'App',
    components: {
      ProductList,
      AddProduct,
      UpdateProduct,
      DeleteProduct,
      RecordTransaction,
      ExpirationCheck,
    },
    data() {
      return {
        currentComponent: '',
        componentKey: 0,
      };
    },
    methods: {
      showProductList() {
        this.currentComponent = 'ProductList';
      },
      showAddProduct() {
        this.currentComponent = 'AddProduct';
      },
      showUpdateProduct() {
        this.currentComponent = 'UpdateProduct';
      },
      showDeleteProduct() {
        this.currentComponent = 'DeleteProduct';
      },
      showRecordTransaction() {
        this.currentComponent = 'RecordTransaction';
      },
      updateProductList() {
        this.componentKey += 1;
      },
    },
  };
  </script>
  
  <style>
  #app {
    font-family: 'Arial', sans-serif;
  }
  
  header {
    background-color: #006400; /* Dark Green */
    color: #ffffff;
    padding: 20px;
    text-align: center;
  }
  
  .app-title {
    margin: 0;
  }
  
  nav {
    background-color: #004d00; /* Darker Green */
    padding: 10px;
    text-align: center;
  }
  
  button {
    margin: 5px;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    color: #ffffff;
    background-color: #006400; /* Dark Green */
    cursor: pointer;
    font-size: 14px;
  }
  
  button:hover {
    background-color: #004d00; /* Darker Green on hover */
  }
  
  main {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px;
  }
  
  footer {
    text-align: center;
    padding: 20px;
    background-color: #d3ffd3; /* Light Green */
  }
  </style>
  
  
