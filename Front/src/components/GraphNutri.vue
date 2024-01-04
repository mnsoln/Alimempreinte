<template>
    <Radar :data="chartData" :options="options" />
  </template>
  
  <script>
  import { Radar } from 'vue-chartjs';
  
  export default {
    props: {
      nbPortions: Number,
      myIngredients: Array,
    },
    components: {
      Radar,
    },
    data() {
      return {
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: 'Parts du total carbone',
              fullSize: true,
            },
          },
        },
        chartData: {
          labels: ['Protéines', 'Glucides', 'Sucres', 'Lipides'],
          datasets: [],
        },
      };
    },
    watch: {
      myIngredients: {
        handler(newIngredients) {
          console.log('myIngredients updated:', newIngredients);
          this.updateChartData();
        },
        deep: true,
        immediate: true,
      },
    },
    methods: {
      updateChartData() {
        const recipeData = this.calculateRecipeData();
        console.log('recipe', recipeData);
        console.log('ing1', this.myIngredients);
  
        if (!this.myIngredients) {
          // Handle the case where myIngredients is undefined
          return;
        }
  
        this.chartData.datasets = [
          {
            label: 'Apports recommandés',
            backgroundColor: 'rgba(179,181,198,0.2)',
            borderColor: 'rgba(179,181,198,1)',
            pointBackgroundColor: 'rgba(179,181,198,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(179,181,198,1)',
            data: [50, 260, 90, 70],
          },
          {
            label: 'Votre recette',
            backgroundColor: 'rgba(220,20,60,0.2)',
            borderColor: 'rgba(220,20,60,1)',
            pointBackgroundColor: 'rgba(220,20,60,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(220,20,60,1)',
            data: recipeData,
          },
        ];
      },
      calculateRecipeData() {
        console.log('here');
        console.log('ing', this.myIngredients);
  
        if (!this.myIngredients || this.myIngredients.length === 0) {
          return [0, 0, 0, 0];
        }
  
        const sumProteins = this.myIngredients.reduce((acc, ingredient) => acc + (ingredient.proteines || 0), 0);
        const sumGlucids = this.myIngredients.reduce((acc, ingredient) => acc + (ingredient.glucides || 0), 0);
        const sumSucres = this.myIngredients.reduce((acc, ingredient) => acc + (ingredient.sucres || 0), 0);
        const sumLipides = this.myIngredients.reduce((acc, ingredient) => acc + (ingredient.lipides || 0), 0);
        console.log(sumProteins, sumGlucids, sumSucres);
  
        return [sumProteins, sumGlucids, sumSucres, sumLipides];
      },
    },
  };
  </script>