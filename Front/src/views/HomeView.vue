<template>
  
  <body>
    <br>
    <hr>
    <br>
    <div>
      <!-- Bouton pour ouvrir la fenêtre de présentation -->
      <button @click="togglePresentation"><h2>Présentation du site</h2></button>
      <!-- Fenêtre présentation -->
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <p style="font-size: 1.1em;">
            Utilisez notre outil peut vous aider à évaluer et réduire votre empreinte carbone alimentaire. Pour en savoir plus sur notre mission, notre équipe et nos objectifs, visitez notre page <a style="color: #e3541a;" href="/about">En savoir plus</a>.
            <br>
            <br>
            <v-btn color="#e3541a" @click="openVideo">Tutoriel Vidéo</v-btn>
          </p>
        </div>
      </div>
  
      </div>
      <br>
      <hr>
      <br>
      <div class="container-fluid">
        <div class="row">     
            <div style="flex-direction: column">
                <div class="col-6 manualInput text-center">
                    <h1>Calculer l'empreinte carbone d'une nouvelle recette</h1>
                    <form method="GET" action="/manual/input" @submit.prevent="confirmRecipe">
                        <br/>
                        <label for="principal" style="font-size: 25px;">Nom de la recette (max. 50 caractères) :</label><br />
                        <br/>
                        <v-text-field
                          v-model="meal_name"
                          label="Saisie de la recette"
                          placeholder="exemple: Ratatouille"
                          required
                          ></v-text-field>
                          <v-btn color="#e3541a" type="submit">Confirmer</v-btn>
                          <v-alert v-if="recipeNameError" type="error">{{ recipeNameError }}</v-alert>
                    </form>
                    
                
                </div>
            </div>
        </div>
        <br>
        <hr>
        <br>
        <div style="display: flex;flex-wrap: wrap;justify-content: space-between;">
          <div style="flex: auto; min-width: 311px; width: 42.5%; max-width: 60%; margin: 0 auto;">
            <h4 style="text-align: center;">Comparaison de l'empreinte carbone des plats suivants exprimée en % du budget carbone quotidien: risotto de crozets, poisson pané, saucisse de Toulouse, bavette de flanchet</h4>
            <v-img 
            src="..\..\static\img\Graphe page d'accueil.jpg"
            max-height="400"
            max-width="500"
            style="margin: 0 auto;"></v-img>
          </div>
          <div style="flex:auto;min-width: 300px;">
            <div style="text-align: center;">
              <h2 class="display-4" style="margin: 0 auto;">Exemples d'empreintes carbone de plats</h2> <h5 style="margin: 0 auto;">(% du budget carbone quotidien par personne à ne pas dépasser pour atteindre l'objectif des 2°C fixé par la COP21 en  2015)</h5>
            </div>
            <div style="flex: auto;max-width: 850px; overflow-y: auto;min-width: 300px;margin: 0 auto;">
              

            
            <v-card>
              <v-card-title >
                <DataTable :value="this.recipesToDisplay" paginator :rows="5" filterDisplay="row" v-model:selection="this.selectedRecipe"
                tableStyle="min-width: 50rem">
                  <template #empty> Pas de recettes trouvées. </template>
                  <Column selectionMode="single" headerStyle="width: 3rem"></Column>
                  <Column field="name" header ='Recette' style="width: 40%; font-weight: 500;" ></Column>
                  <Column field="proteins" header ="Protéines (g)" style="width: 25%"></Column>
                  <Column field="co2" header ='Emissions de carbones kg CO2' style="width: 25%;"></Column>
                </DataTable>
              </v-card-title> 
            </v-card>

            <br>
              <v-btn v-if="this.selectedRecipe" color="warning" @click="viewRecipe"> Visionner la recette </v-btn>
              &nbsp;&nbsp;
              <v-btn v-if="this.admin && this.selectedRecipe || this.crous && this.selectedRecipe" color="error" @click="this.dialogDelete = true">Supprimer la recette sélectionnée </v-btn>
            </div>
          </div>
      </div>
      <v-dialog v-model="dialogDelete" width="50%" >
        <v-card>
          <v-card-title
          class="headline grey lighten-2"
            primary-title
          >
          Confirmation</v-card-title>
        <v-card-text>
          Êtes-vous sûr de supprimer définitivement cette recette ?
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="red darken-1" flat @click="this.dialogDelete = false" > Non </v-btn> <v-btn color="green darken-1"  @click="deleteRecipe()" > Oui </v-btn>
        </v-card-actions>
        </v-card>
      </v-dialog>
    
      <br>
      <hr>
      <br>
      <br>
      <div style="display: flex;padding-left: 10%;padding-right: 10%;">
  
        <div style="flex: 1;">
          <img src="/UCBL.png" width="100%" style="object-fit: cover">
        </div>
        &nbsp;&nbsp;&nbsp;&nbsp;
        <div style="flex: 0.25;">
          <img src="/CNRS.jpg" width="100%" style="object-fit: cover">
        </div>
        &nbsp;&nbsp;&nbsp;&nbsp;
        <div style="flex: 1;">
          <img src="/LBBE.png" width="100%" style="object-fit: cover;">
        </div>
        &nbsp;&nbsp;&nbsp;&nbsp;
        <div style="flex: 0.25;">
          <img src="/ICJ.png" width="100%" style="object-fit: cover;">
        </div>
      </div> 
    </div>

  </body>  

</template>

<script>
import { ref } from 'vue';

export default {
  data() {
    return {
      meal_name: '',
      admin: false,
      public: false,
      crous : false,
      confirmUrl :"/manual-input/",
      recipeNameError: '', // Error message
      showModal: true, // Ajout de la variable showModal pour contrôler la fenêtre modale
      search: '',
      headers: [
          {
            align: 'start',
            key: 'name',
            sortable: false,
            title: 'Recette',
          },
          { key: 'proteins', title: 'Protéines (g)' },
          { key: 'co2', title: 'Emissions de carbone (kg CO2 eq)' },
        ],
      recipesToDisplay : ref([]),
      selectedRecipe : ref(),
      dialogDelete : ref(false),
      droits : "",
    };

    
  },
  methods: {

    //creer une nouvelle recette
    confirmRecipe() {
      // Get the value of the recipe name input field
      let recipeName = this.meal_name.trim();
      if (recipeName === "") {
        this.recipeNameError = "Veuillez saisir un nom de recette."; // Set the error message
      } else {
        this.recipeNameError = ''; // Clear the error message
      if (this.admin){
      this.confirmUrl = "/manual-input/admin";
      }
      else if (this.crous){
        this.confirmUrl = "/manual-input/crous";
      }
      else {
        this.confirmUrl = "/manual-input/";
      }
      this.$router.push({
          path: this.confirmUrl,
          query: { meal_name: recipeName }
        },
      );
      }
    },

    //ouvrir la recette selectionnee
    viewRecipe(){
      let recipeName = this.selectedRecipe.name
      if (this.admin){
      this.confirmUrl = "/manual-input/admin";
      }
      else if (this.crous){
        this.confirmUrl = "/manual-input/crous";
      }
      else {
        this.confirmUrl = "/manual-input/";
      }
      this.$router.push({
          path: this.confirmUrl,
          query: { meal_name: recipeName }
        },
      );

    },
    clearRecipeNameError() {
      this.recipeNameError = ''; // Clear the error message when the user starts typing
    },
    togglePresentation() {
    this.showModal = !this.showModal;
  },

  // savoir si public, crous ou admin
    getRights(){
      let url = window.location.href;
      if (url.endsWith('admin') || url.endsWith('admin/')){
        this.admin = true;
        this.droits = "admin";
      }
      else if (url.endsWith('crous') || url.endsWith('crous/')){
        this.crous = true;
        this.droits = "crous";
      }
      else {
        this.public = true;
        this.droits = "public";
      }
    },

    // obtenir les recettes enregistrées
    getTable() {
      this.recipesToDisplay = [];
      let path;
      if (this.crous) {
        path = '/api/recipes-crous'
      }
      else {
        path = '/api/recipes-admin'
      }
      this.axios.get(path)
      .then((res) => {
        const resData = res.data;
        for (let recette of resData ){
          this.recipesToDisplay.push({
            name: recette.name,
            proteins: recette.proteines,
            co2: recette.co2,
    });
        }
      }
      )
      .catch((error) => {
        console.error(error);
        console.error("Echec de la connexion au backend /api/recipes-admin");
      })
    },

    //suprimer recette si admin/crous
    deleteRecipe() {
      this.dialogDelete = false;
      this.axios.post("/api/delete-recipes", {"droits":this.droits, "recette": this.selectedRecipe})
      .then(() => {
        this.getTable();
        this.selectedRecipe = "";
      })
      .catch((error) => {
        console.error('deleterecipe',error)
      });
    },
    openVideo() {
      window.open('/static/img/Demo_Alimempreinte.mp4', '_blank');
    },
    getColorClass(rowData) {
      const co2 = rowData.co2;
      if (co2 >= 0 && co2 < 1.06) {
        return 'green-dark';
      } else if (co2 >= 1.06 && co2 < 2.16) {
        return 'green-light';
      } else if (co2 >= 2.16 && co2 < 3.25) {
        return 'yellow';
      } else if (co2 >= 3.25 && co2 < 4.35) {
        return 'red-light';
      } else {
        return 'red-dark';
      }
    },
  },
  created() {
    this.getRights();
    this.getTable();
  }
}
</script>

<style scoped>
.green-dark {
  background-color: darkgreen;
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.green-light {
  background-color: lightgreen;
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.yellow {
  background-color: yellow;
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.red-light {
  background-color: lightcoral;
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.red-dark {
  background-color: darkred;
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

</style>