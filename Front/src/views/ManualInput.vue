<template>
  <Message v-if="this.warning" severity="warn">{{ this.errorMessage }}</Message>


  <div>
    <h1 style="text-align: center">Nom de la recette : {{ meal_name }}</h1>
    <br>

    <div>
        <v-text-field
          v-model="nbPortions"
          label="Nombre de portions"
          type="number"
          placeholder="Portions"
          min=1
          @update:modelValue="updateIngredientInfos()"
        ></v-text-field>
    </div>

    <div class="ingredients">
      <v-form @submit.prevent="addIngredient">
        <v-autocomplete
          v-model="newIngredient.name"
          label="Saisissez un ingrédient ici"
          ref="newIngredientRef"
          :items="filteredItems"
          :custom-filter="customFilter"
          auto-select-first
          @update:modelValue="autoCompleteInput(newIngredient.name)"
        ></v-autocomplete>

        <v-text-field
          v-model="quantity"
          label="Quantité en grammes"
          type="number"
          placeholder="Poids en gramme"
          suffix="grammes"
          min=1
        ></v-text-field>

        <div class="d-flex flex-column flex-md-row">
          <v-btn
            color="#e3541a"
            @click="addIngredient"
          >
            Ajouter un ingrédient
          </v-btn>
          &nbsp;&nbsp;&nbsp;&nbsp;

          <div class="d-flex flex-row">
            <p style="font-size: 1.1em;">
              Tableaux pour aider à la saisie de la quantité :
              <a style="color: #e3541a; display: flex;" href="../static/img/Tableau du poids moyen de Fruits et Légumes PDF.pdf" target="_blank">- Tableau du poids moyen de différents fruits  et     légumes</a>
              <a style="color: #e3541a; display: flex;" href="../static/img/grammage-des-portions-daliments.pdf" target="_blank">- Tableau de la portion moyenne d'aliments</a>
            </p>
          </div>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <v-tooltip text="Lors du choix d'ingrédient, privilégier l'ingrédient 'cru' et ne pas rajouter le sel et le poivre">
            <template v-slot:activator="{ props }">
              <v-btn v-bind="props">AIDE</v-btn>
            </template>
          </v-tooltip>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <v-btn color="#e3541a" @click="openVideo">Tutoriel Vidéo</v-btn>

        </div>

        <v-btn
        v-if="displayNutrition && this.droits=='admin' || displayNutrition && this.droits=='crous'"
          color="#e3541a"
          @click="this.dialogSave = true"
          style="float: right;"
        >
          Sauvegarder
        </v-btn>
      </v-form>

      <v-card class="pa-2 mt-4" style="width:100%;" v-if="displayNutrition && myIngredients">

        <v-card-title style="width:49%;"> Liste d'ingrédients pour {{ meal_name }}</v-card-title> 
        <v-btn v-if="selectedIngredient.length > 0" @click="removeIngredient()" color="#5e5e5e" > Supprimer </v-btn>
        <div class="d-flex flex-column flex-md-row align-items-center" style="width: 100%;max-height: 400px;">

          <DataTable class="flex-grow-1" style="width:100%;overflow-y: auto;max-height: 200px;min-width: 250px;" :value="this.myIngredients" v-model:editingRows="editingRows"
            tableClass="editable-cells-table" dataKey="name"   editMode="row"   @row-edit-save="onRowEditSave()"
            v-model:selection="this.selectedIngredient"> 
            <template #empty> Pas de recettes trouvées. </template>
            <Column selectionMode="multiple" ></Column>
            <Column field="name" header ="Ingrédient" style="width: 60%; padding-left: 2%;"></Column>
            <Column field="quantity" header ='Quantité (g)' style="width: 40%" :editable="true">
              <template #editor="{ data, field }">
                <v-text-field
                  v-model="data[field]"
                  label="Quantité en grammes"
                  type="number"
                  placeholder="Poids en gramme"
                  suffix="grammes"
                  min=1
                ></v-text-field>
              </template>
            </Column>
          </DataTable>

          <br>
          <img v-if="this.displayNutrition" class="img-fluid" style="max-width: 800px;flex: auto; padding-left: 5%; padding-right: 3%;" :src=this.Jaugesource />
        </div>
      </v-card>

    </div>
  
    <br>
    <v-card v-if="displayNutrition" style="text-align: left;">
      <p style="font-size: 16px;color: #333;margin: 0;">Pour cette recette, une portion vaut : 
        <span style="color: red;font-family: Arial, sans-serif;font-size: 1.1em;">{{ gramPerPortion }}</span>  grammes
      </p>
    </v-card>
    <br>
    <v-card v-if="this.displayNutrition">
      <v-card-title>Informations nutritionnelles et carbone :</v-card-title>
      <div class="container-fluid">
        <div class="row">
          <div class="col-md-6">
            <table style="width: 100%;">
              <tr>
                <td style="width: 30%;"><b>Émissions de CO2 par portion: </b></td>
                <td>
                  <div class="d-flex align-items-center">
                    <span style="color: red;font-family: Arial, sans-serif;font-size: 1.1em;">{{ this.raccourcirNombre(this.recetteInfos.co2, 3) }}</span> &nbsp;&nbsp;
                    <span style="text-size-adjust: 100%; font-family: Arial, sans-serif; color: black; font-size: 1em;"> kg CO<sub>2</sub> eq</span>
                  </div>
                </td>
              </tr>
            </table>
          </div>
          <div class="col-md-6">
            <div class="d-flex justify-content-end">
              <PngGenerator v-if="this.displayNutrition" :Jaugesource="this.Jaugesource" :mealName="this.meal_name"/>
            </div>
          </div>
        </div>
        <div class="row mt-4">
          <div class="col-md-6">
            <b>Apports nutritionnels:</b>
          </div>
          <div class="col-md-6">
            <ul style="list-style-type: none; padding: 0;">
              <li>· Protéines: <span style="color: red;font-family: Arial, sans-serif;font-size: 1.1em;">{{ this.raccourcirNombre(this.recetteInfos.proteines, 2) }}</span> g</li>
              <li>· Glucides: <span style="color: red;font-family: Arial, sans-serif;font-size: 1.1em;">{{ this.raccourcirNombre(this.recetteInfos.glucides, 2) }}</span> g, dont sucres: <span     style="color: red;font-family: Arial, sans-serif;font-size: 1.1em;">{{ this.raccourcirNombre(this.recetteInfos.sucres, 2) }}</span> g</li>
              <li>· Lipides: <span style="color: red;font-family: Arial, sans-serif;font-size: 1.1em;">{{ this.raccourcirNombre(this.recetteInfos.lipides, 2) }}</span> g</li>
            </ul>
          </div>
        </div>
      </div>
      <div class="d-flex flex-column flex-md-row align-items-center mt-4">
        <GraphCO2 v-if="this.displayNutrition" :nb-portions="parseInt(this.nbPortions)" :myIngredients="this.myIngredients" />
      </div>
    </v-card>

  </div>
  <br>
    <PdfGenerator v-if="this.displayNutrition"
      :mealName="this.meal_name"
      :nbPortions=parseInt(this.nbPortions)
      :myIngredients="this.myIngredients"
      :recetteInfos="this.recetteInfos"
      :Jaugesource="this.Jaugesource"
    />

    <v-dialog v-model="this.dialogSave" width="50%" >
      <v-card>
        <v-card-title
          class="headline grey lighten-2"
          primary-title>
          Confirmation
        </v-card-title>

        <v-card-text>
          Êtes-vous sûr de sauvegarder cette recette et quitter cette page ?
        </v-card-text>

        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="red darken-1" flat @click="this.dialogSave = false" > Non </v-btn> <v-btn color="green darken-1"  @click="saveRecipes" > Oui </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

</template>

<script>
import { ref } from 'vue';
import SaveToPDF from '../components/SaveToPDF.vue';
import SaveToPNG from '../components/SaveToPNG.vue';
import GraphCO2 from '../components/GraphCO2.vue';


export default {
  data() {
    return {
      newIngredient: { name: "" },
      quantity: 0,
      nbPortions: ref('1'),
      ingredients: ref([
        { name: "", quantity: "" }
      ]),
      ingredient :ref({ name: "", quantity: "" }),
      resData : ref([]),
      myIngredients : ref([]),
      errorMessage : ref(""),
      ingredientCo2 : ref(""),
      ingredientProteines : ref(""),
      ingredientProteines : ref(""),
      displayNutrition : ref(false),
      warning: ref(false),
      recetteInfos : ref([]),
      jaugeImage : ref({src:""}),
      Jaugesource:ref(""),
      droits: "",
      editingRows: [],
      selectedIngredient: ref([]),
      gramPerPortion : ref(0),
      dialogSave : ref(false),
      queryText: '',
      notFoundText: 'No Data Available',
    };
  },
  components: {
    PdfGenerator : SaveToPDF,
    PngGenerator : SaveToPNG,
    GraphCO2 : GraphCO2,
  },
  methods: {
    focusInput() {
      this.$refs.newIngredientRef.focus();
    },

    customFilter(itemTitle, queryText, item) {
      this.queryText = queryText
      return true
    },

    removeAccents(str) {
      return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    },

    removeIngredient() {
      for (let ingredientToRemove of this.selectedIngredient) {
      this.myIngredients = this.myIngredients.filter(obj => obj["name"] !== ingredientToRemove.name);
      };
      this.updateIngredientInfos();
    },

    addIngredient() {
      if (this.newIngredient.name !== "" && this.quantity > 0) { //si correct
        this.warning=false;
        this.myIngredients.unshift({ name: this.newIngredient.name, quantity: this.quantity, proteines: this.ingredientProteines/1000*this.quantity, glucides: this.ingredientGlucides/1000*this.quantity, sucres: this.ingredientSucres/1000*this.quantity, co2: this.ingredientCo2/1000*this.quantity, lipides: this.ingredientLipides });
        this.updateIngredientInfos();
        this.newIngredient.name = "";
        this.quantity = 0;

      } else if (this.quantity == 0){
        this.errorMessage = " La quantité doit être supérieure à zéro.";
        this.warning=true;
      }
      else if (this.newIngredient.name == ""){
        this.errorMessage = "L'ingrédient ne doit pas être vide.";
        this.warning=true;
      }
    },

    // remplir les infos de la recette
    updateIngredientInfos() {
      if (this.myIngredients.length ==0){
        this.displayNutrition = false;
      }
      else if (this.myIngredients.length ==1){

        //si on vient de supprimer qqch
        if (this.quantity == 0 && this.newIngredient.name == "") {
          
          this.recetteInfos = { 
            proteines : this.myIngredients[0].proteines/this.nbPortions, 
            glucides : this.myIngredients[0].glucides/this.nbPortions, 
            sucres: this.myIngredients[0].sucres/this.nbPortions, 
            lipides : this.myIngredients[0].lipides/this.nbPortions, 
            co2 : this.myIngredients[0].co2/this.nbPortions}
        }

        //si on vient d'ajouter qqch
        else {
        this.displayNutrition = true;
        this.recetteInfos = { 
          proteines : this.ingredientProteines/1000*this.quantity/this.nbPortions, 
          glucides : this.ingredientGlucides/1000*this.quantity/this.nbPortions, 
          sucres: this.ingredientSucres/1000*this.quantity/this.nbPortions, 
          lipides : this.ingredientLipides/1000*this.quantity/this.nbPortions, 
          co2 :this.ingredientCo2/1000*this.quantity/this.nbPortions}
        }
      }

      //si il y a plusieurs ingredients, on recalcule
      else if (this.myIngredients.length >1){
        // this.recetteInfos = this.viderArray(this.recetteInfos)
        this.recetteInfos  = {
        proteines: 0,
        glucides: 0,
        sucres: 0,
        lipides: 0,
        co2: 0
        };
        for (let ing of this.myIngredients) {
          
          
          // Convertir en nombre
          let proteines = parseFloat(ing.proteines);
          let glucides = parseFloat(ing.glucides);
          let sucres = parseFloat(ing.sucres);
          let lipides = parseFloat(ing.lipides);
          let co2 = parseFloat(ing.co2); 
          if (!isNaN(proteines)) {
            this.recetteInfos.proteines += proteines/this.nbPortions; // Additionner
            this.recetteInfos.glucides += glucides/this.nbPortions;
            this.recetteInfos.sucres += sucres/this.nbPortions;
            this.recetteInfos.lipides += lipides/this.nbPortions;
            this.recetteInfos.co2 += co2/this.nbPortions;
          }
        } 
      }
      this.getJauge();
      this.getgramPerPortion();
      
    },

      // enregistrer les infos de l'ingrédient ajouté
    autoCompleteInput(ingredientName) {
      this.axios.post('/api/ingredient', { "inputName": ingredientName })
        .then((res) => {
          if (res.data.status !== "missing") {
          this.ingredientInfos = res.data.result;
          this.ingredientProteines = this.ingredientInfos.Proteines;
          this.ingredientGlucides = this.ingredientInfos.Glucides;
          this.ingredientSucres = this.ingredientInfos.Sucres;
          this.ingredientLipides = this.ingredientInfos.Lipides;
          this.ingredientCo2 = this.ingredientInfos.co2;
          // this.updateIngredientInfos()
        }
        })
        .catch((error) => {
          console.error(error);
        })

    },

    // Chercher si la recette existe déjà, si oui l'obtenir
    get1Recipe(){
      let path = ""
      if (this.droits ==="crous"){
        path = "/api/search-recipe-crous"
      }
      else {
        path = "/api/search-recipe"
      }
      this.axios.post(path, { "name": this.meal_name })
        .then((res) => {
          if (res.data.status === "missing"){
            return null
          }
          else{
            this.myIngredients = res.data.ingredients
            this.nbPortions = res.data.portions
            this.displayNutrition = true
            this.getgramPerPortion()
            this.updateIngredientInfos()
          }
            })
        .catch((error) => {
          console.error(error);
        })
      
    },
    raccourcirNombre(nombre, decimales) {
    const nombre2 = parseFloat(nombre);
    if (!isNaN(nombre2)) {
        return parseFloat(nombre2.toFixed(decimales));
    } else {
        return null; // En cas d'erreur de conversion
    }
    },
    viderArray(arrayPlein){
      for (let attribut in arrayPlein) {
        if (arrayPlein.hasOwnProperty(attribut)) {
            arrayPlein[attribut] = 0;
        }
      }
    return arrayPlein

    },
    // Calculer la quantité de grammes par portion
    getgramPerPortion() {
      let gramSum = 0;
      for (let ing of this.myIngredients){
        const quantity = parseFloat(ing.quantity);
        gramSum += quantity;
      }
      this.gramPerPortion = gramSum/this.nbPortions
    },

  // Obtenir la jauge trace carbone
    getJauge(){
      this.Jaugesource = "/api/jauge?eCO2=" + this.recetteInfos.co2
    },
      
        // savoir si public, crous ou admin
    getRights(){
      let url = window.location.href;
      if (url.includes('/admin')){
        this.droits = "admin";
      }
      else if (url.includes('/crous')){
        this.droits = "crous";
      }
      else {
        this.droits = "public";
      }
    },

    //sauvegarder les recettes dans la base
    saveRecipes() {
      //ajouter le total de la recette

      let myRecette = [{name: this.meal_name, proteines: this.raccourcirNombre(this.recetteInfos.proteines,3), co2: this.raccourcirNombre(this.recetteInfos.co2,3), portions: this.nbPortions,  ingredients : [] }]

      //ajouter les ingredients et leurs valeurs
      for (let ing of this.myIngredients){
        myRecette[0].ingredients.push(ing)
      }
      const payload = JSON.parse(JSON.stringify(myRecette));
      let path;
      let out;
      if (this.droits == 'crous'){
        path='/api/recipes-crous'
        out = "/crous"
      }
      else {
        path = '/api/recipes-admin'
        out = "/admin"
      }
      this.axios.post(path, payload)
        .then(() => {
          this.$router.push({
            path: out
          },
        );
        })
        .catch((error) => {
          console.error(error)
        });
    },

    openVideo() {
      window.open('/static/img/Demo_Alimempreinte.mp4', '_blank');
    }
    },
  computed: {
    ingredientsCount() {
      return this.myIngredients.length;
    },

    // filtre pour autocomplete
    filteredItems() {
      if (!this.resData || !this.resData.length) return []

      const searchText = this.removeAccents(
        this.queryText ? this.queryText.toLowerCase() : ''
      )

      if (searchText === '') {
        return this.resData
      }
    
      const startsWithSearch = []
      const containsSearch = []
    
      this.resData.forEach(item => {
        const textOne = this.removeAccents(item.toLowerCase())
        if (textOne.startsWith(searchText)) {
          startsWithSearch.push(item)
        } else if (textOne.includes(searchText)) {
          containsSearch.push(item)
        }
      })
    
      // Tri des listes en fonction de la longueur
      startsWithSearch.sort((a, b) => a.length - b.length)
      containsSearch.sort((a, b) => a.length - b.length)
    
      const filtered = startsWithSearch.concat(containsSearch)

      if (filtered.length === 0) {
        return [this.notFoundText]
      }
    
      return filtered
    },
  },
  created() {
    this.getRights()
    this.meal_name = this.$route.query.meal_name;
    this.axios.get('/api/ingredient', { responseEncoding: "latin2" })
      .then((res) => {
        this.resData = res.data
      }
      )
      .catch((error) => {
        console.error(error);
        console.error("Echec de la connexion au backend /api/ingredient")
      })
    this.get1Recipe()
  }


};
</script>
