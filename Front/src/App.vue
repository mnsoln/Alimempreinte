<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
  <header>
    <!-- <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" /> -->

    <div class="wrapper">

      <nav style="position: static;">
        <RouterLink to="/">Accueil</RouterLink>
        <RouterLink to="/about">En savoir plus</RouterLink>
        <!-- <RouterLink to="/manual-input">Rentrer une recette</RouterLink> -->
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>

nav {
    display: flex;
    justify-content: center;
    width: 100%;
    /* font-size: 20px; */
    /* text-align: center; */
    /* margin-top: 2rem; */
  }

  nav a {
    text-decoration: none;
    padding: 15px 20px;
    position: relative;
    display: inline-block;
    /* background-color: #5e5e5e; */
    color: #5e5e5e;
    /* padding: 0 1rem; */
  }

  nav a::after {
    content: "";
    display: block;
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 3px;
    background-color: #e3541a; 
    transition: width 0.3s;
  }

  nav a:hover::after {
    width: 100%;
    height: 10%;
  }

header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

/* nav {
  width: 100%;
  font-size: 20px;
  text-align: center;
  margin-top: 2rem;
} */

/* nav a.router-link-exact-active {
  color: var(--color-text);
} */

/* nav a.router-link-exact-active:hover {
  background-color: transparent;
} */

/* nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
} */

/* nav a:first-of-type {
  border: 0;
} */
/* 
@media (max-width: 1024px) {
  header {
    line-height: 1.5;
    max-height: 100vh;
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: center;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
} */
</style>
