<template>
  <div>
    <h2>Charities List</h2>
    <ul>
      <li v-for="charity in charities" :key="charity.id">
        {{ charity.name }} - {{ charity.address }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    charities: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>

