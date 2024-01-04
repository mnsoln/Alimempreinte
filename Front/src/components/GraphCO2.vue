<template>
    <Pie aria-label="yo"  aria-describedby="yess"   :data="chartData" :options="options" />
</template>

<script>
    import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js/auto'
    import { Pie } from 'vue-chartjs'
    import { ref, computed } from 'vue'
    ChartJS.register(ArcElement, Tooltip, Legend)
    
    export default {
        props: {
            nbPortions: Number,
            myIngredients: Array,
        },
        components: {
            Pie
        },
        data() {
            return {
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
            title: {
                display: true,
                text: 'Parts du total carbone des 4 ingrédients les plus polluants',
                fullSize: true,
            }
        }
                },
                chartData: { labels: [], datasets: [] }
            }
        },
            computed: {
            sortedIngredients() {
                return this.myIngredients.slice().sort((a, b) => b.co2 - a.co2);
                },
            topFourIngredients() {
                return this.sortedIngredients.slice(0, 4);
                },
            },
            watch: {
                topFourIngredients: {
                handler() {
                    this.updateChartData();
                },
                deep: true,
                immediate: true,
                }
            },
            methods: {
                updateChartData() {
                    this.chartData = {
                    labels: this.topFourIngredients.map(top => top.name),
                    datasets: [
                    {
                        backgroundColor: ['#DC143C', '#E9967A', '#FFFACD', '#ADD8E6'],
                        data: this.topFourIngredients.map(top => top.co2),
                    }
                    ]
                    };
            }
        }
    }
</script>