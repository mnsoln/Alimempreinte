<template>
    <div>
        <v-btn color="#e3541a" @click="generatePDF">Télécharger RECETTE</v-btn>
    </div>
</template>

<script>
    import { jsPDF } from 'jspdf';

    export default {
    props: {
        mealName: String,
        nbPortions: Number,
        myIngredients: Array,
        recetteInfos: Object,
        Jaugesource: String,
    },
    methods: {
        generatePDF() {
            let doc = new jsPDF();
            doc.setFillColor(255, 116, 13);
            doc.roundedRect(10, 10, doc.internal.pageSize.width - 20, 20, 5, 5, 'F');
            doc.setFontSize(16);
            doc.text(this.mealName, doc.internal.pageSize.width / 2, 22, 'center');
            doc.setFontSize(12);
            doc.setTextColor(100);
            doc.text("Nombre de portions :", 20, 50);
            doc.setTextColor(0);
            doc.text(this.nbPortions.toString(), 20, 60);
            doc.setTextColor(100);
            doc.text("Ingrédients : ", 20, 70);
            doc.text("Grammage aliments : ", 95, 70);
            doc.text("CO2 : ", 150, 70);
            let align = 80;
            let lineHeight = 10;
            let totalHeight = 80;
            doc.setTextColor(0);
            const maxCO2 = Math.max(...this.myIngredients.map(ingredient => ingredient.co2));
            for (let i = 0; i < this.myIngredients.length; i++) {
                let name = this.myIngredients[i].name;
                let quantity = this.myIngredients[i].quantity > 1 ? this.myIngredients  [i].quantity + " grammes" : this.myIngredients[i].quantity + "    gramme";
                let co2 = this.myIngredients[i].co2;
                let nameLines = doc.splitTextToSize(name, 70);
                if (nameLines.length > 0) {
                doc.text("- " + nameLines[0], 20, align);
                doc.text(quantity, 95, align);
                    if (co2 === maxCO2) {
                        doc.setTextColor(255, 0, 0);
                    }
                doc.text(this.raccourcirNombre(co2,3) + " kg CO2", 150, align);
                doc.setTextColor(0);
                }
                for (let j = 1; j < nameLines.length; j++) {
                doc.text(nameLines[j], 20, align + (j * 8));
                }
            
              align += Math.max(nameLines.length, 1) * 8;
              totalHeight += Math.max(nameLines.length, 1) * lineHeight;
            }
            totalHeight += 5;
            doc.setFontSize(12);
            doc.setTextColor(100);
            doc.text("Informations nutritionnelles et carbone :", 20, totalHeight);
            totalHeight += lineHeight;
            doc.setTextColor(0);
            doc.text("Émissions de CO2 par portion :    " + this.raccourcirNombre   (this.recetteInfos.co2, 3) + " kg CO2 eq", 20, totalHeight);
            totalHeight += lineHeight + 5;
            doc.setTextColor(100);
            doc.text("Apports nutritionnels :", 20, totalHeight);
            totalHeight += lineHeight;
            doc.setTextColor(0);
            doc.text("Protéines :    " + this.raccourcirNombre(this.recetteInfos.   proteines, 2) + " g", 20, totalHeight);
            totalHeight += lineHeight;
            doc.text("Glucides :    " + this.raccourcirNombre(this.recetteInfos.    glucides, 2) + " g", 20, totalHeight);
            totalHeight += lineHeight;
            doc.text("Lipides :    " + this.raccourcirNombre(this.recetteInfos. lipides, 2) + " g", 20, totalHeight);
            totalHeight += lineHeight;
            doc.addImage(this.Jaugesource, 'JPEG', 20, totalHeight, 125, 50);
            doc.save(this.mealName + ".pdf");
        },
        raccourcirNombre(nombre, decimales) {
            const nombre2 = parseFloat(nombre);
            if (!isNaN(nombre2)) {
                return parseFloat(nombre2.toFixed(decimales));
            } else {
              return null; // En cas d'erreur de conversion
            }
        },
    },
};
</script>