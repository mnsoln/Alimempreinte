<template>
    <div>
        <v-btn color="#e3541a" @click="telechargerImage" >Télécharger Jauge</v-btn>
    </div>
</template>

<script>

    export default {
    props: {
        mealName: String,
        nbPortions: Number,
        myIngredients: Array,
        recetteInfos: Object,
        Jaugesource: String,
    },
    methods: {
        telechargerImage() {
                let link = document.createElement('a');
                link.href = this.Jaugesource;
                link.download = this.mealName + '_jauge_CO2.png';
                link.click();
            },
    },
};
</script>