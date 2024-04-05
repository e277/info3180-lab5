<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
</script>

<template>
  <AppHeader />

  <main>
    <RouterView />
  </main>
  
  <AppFooter />
</template>

<style>
body {
  padding-top: 75px;
}

form {
  padding: 50px;
}
form label {
  display: block;
  margin-bottom: 10px;
}
form input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
}
form textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  height: 200px;
}
form p,
form li {
  padding: 4px;
  font-weight: 600;
  font-size: 1.2em;
}
form li {
  margin-left: 16px;
}
</style>