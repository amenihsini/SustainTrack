<template>
  <div>
    <div class="expiration-messages">
      <div class="message" v-for="message in expiringMessages" :key="message">{{ message }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      expiringMessages: [],
    };
  },
  methods: {
    async checkExpirationDates() {
      try {
        const response = await axios.post('http://localhost:8000/check_expiration_dates');
        const logMessages = response.data.log_messages;
        this.expiringMessages.push(...logMessages);
      } catch (error) {
        console.error('Error fetching expiration dates:', error);
      }
    },
  },
  mounted() {
    this.checkExpirationDates();
  },
};
</script>

<style>
.expiration-messages {
  background-color: #990000; /* Darker red background color */
  padding: 10px;
  margin-top: 10px;
}

.message {
  color: #fff;
  margin-bottom: 5px;
}
</style>
