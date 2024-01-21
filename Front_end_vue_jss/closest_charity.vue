<template>
  <div>
    <h2>Closest charities to you, Contact then and donate!</h2>
    <ul>
      <li v-for="charity in closestCharities" :key="charity.id">
        <strong>{{ charity.name }}</strong><br>
        Address: {{ charity.address }}<br>
        Contact Info: {{ charity.contact_info }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    closestCharities: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>

