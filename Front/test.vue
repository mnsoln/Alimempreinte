<template>
  <div class="container">
    <h1 style="text-align: center">Nom de la recette : {{ meal_name }}</h1>
    <div class="portions">
      <div class="byWeight">
        <v-text-field
          v-model="nbPortions"
          label="Nombre de portions"
          type="number"
          placeholder="Portions"
          min="1"
          value="1"
        ></v-text-field>
      </div>
    </div>

    <div class="ingredients">
      <v-form @submit.prevent="addIngredient">
        <v-autocomplete
          v-model="newIngredient.name"
          label="Saisissez un ingrédient ici"
          ref="newIngredientRef"
          :items="resData"
          @change="autoCompleteInput(newIngredient.name)"
        ></v-autocomplete>
        <v-text-field
          v-model="quantity"
          label="Quantité"
          type="number"
          placeholder="Poids en gramme"
          suffix="grammes"
          min="0"
        ></v-text-field>

        <v-btn
          color="light-green"
          @click="addIngredient"
        >
          Ajouter un ingrédient
        </v-btn>
      </v-form>

      <v-card class="pa-2 mt-4">
        Ingrédient(s) : {{ ingredientsCount }} 
        <v-list>
          <v-list-item
            v-for="(ingredient, index) in myIngredients"
            :key="ingredient.name"
          >
            <v-list-item-content>
              <v-list-item-title>
                Nom : {{ ingredient.name }} ; Quantité : {{ ingredient.quantity }} g
              </v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn @click="removeIngredient(index)" color="red"> Supprimer </v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-card>
    </div>
    
    <div class="portions">
      <div class="byWeight">
        Nombre de grammes par portion :
        <v-text-field
          type="number"
          placeholder="Remplissage automatique"
          suffix="grammes"
          disabled
        ></v-text-field>
      </div>
    </div>
    
    <v-card v-if="ingredientCo2">
      <p>
        Émissions de CO2 par portion: 
      </p>
      <p>Apports nutritionnels:<br>
        · Protéines: {{ ingredientProteines.toFixed(2) }} g<br>
        · Glucides: {{ ingredientGlucides.toFixed(2) }} g, dont sucres: {{ ingredientSucres.toFixed(2) }} g<br>
        · Lipides: {{ ingredientLipides.toFixed(2) }} g
      </p>
    </v-card>
  </div>
</template>



<script>
import { computed, onMounted, ref } from "vue";
export default {
  setup() {
    const newIngredientRef = ref("");
    const newIngredient = ref({ name: "" });
    const quantity = ref(0); 
    const myIngredients = ref([]);
    const errorMessage = ref("");

    onMounted(() => {
      newIngredientRef.value.focus();
    });

    const ingredientsCount = computed(() => myIngredients.value.length);

    function removeIngredient(index) {
      myIngredients.value.splice(index, 1);
    }

    function addIngredient() {
      if (newIngredient.value.name !== "" && quantity.value > 0) {
        myIngredients.value.unshift({ name: newIngredient.value.name, quantity: quantity.value });
        newIngredient.value.name = "";
        quantity.value = 0;
      } else {
        errorMessage.value = "La quantité doit être supérieure à zéro.";
  }
}

    return {
      myIngredients,
      newIngredient,
      removeIngredient,
      addIngredient,
      newIngredientRef,
      ingredientsCount,
      quantity, 
    };
  },
  methods: {
    autoCompleteInput(ingredientName) {
        console.log('wo',ingredientName);
        this.axios.post('/api/ingredient', {"inputName" : ingredientName})
          .then((res) => {
            console.log(ingredientName)
            this.ingredientInfos = res.data.result ;
            console.log('res',res, 'prot:',this.ingredientInfos.Proteines);
            this.ingredientProteines = this.ingredientInfos.Proteines;
            this.ingredientGlucides = this.ingredientInfos.Glucides;
            this.ingredientSucres = this.ingredientInfos.Sucres;
            this.ingredientLipides = this.ingredientInfos.Lipides;
            this.ingredientCo2 = this.ingredientInfos.co2;
          })
            .catch((error) => {
          console.log(error);
          })
      
    },
  },
  created() {
    console.log('je suis créé')
    this.meal_name = this.$route.query.meal_name;
    this.axios.get('/api/ingredient', {responseEncoding: "latin2"})
        .then((res) => {
          console.log(res)
          this.resData = res.data
          }
        )
        .catch((error) => {
          console.error(error);
          console.error("Echec de la connexion au backend /api/ingredient")
        })
  }
};
</script>
