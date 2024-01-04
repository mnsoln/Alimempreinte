<!-- <template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    /* display: flex; */
    align-items: center;
  }
}
</style> -->

<template>
  <br>
<body style="font-family: Arial, sans-serif;margin: 0;padding: 0;background-color: #f5f5f5;color: #333;">
    <header style="background-color: #e3541a;color: white;text-align: center;padding: 20px;border-radius: 15px;">
        <h1 style="text-align: center;">À propos</h1>
    </header>
    <br>
    <div style="max-width: 800px;margin: 0 auto;padding: 20px;background-color: white;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
        <h2 style="color: #e3541a;">Présentation du site</h2>
        <p style="text-align: justify;margin-bottom: 20px;">
            Bienvenue sur notre site ! Ici, nous vous proposons un outil pour mieux comprendre l'impact environnemental de vos repas. Notre mission est de sensibiliser le public aux émissions de gaz à effet de serre liées à notre alimentation et de fournir des moyens concrets pour réduire notre empreinte carbone individuelle.
        </p>
        <h3 style="color: #e3541a;">Comment ça marche</h3>
        <p style="text-align: justify;margin-bottom: 20px;">
            Notre site vous permet de calculer l'empreinte carbone d'un repas en utilisant une recette. Il s'appuie sur des données de l'ADEME (Agence de la transition écologique) pour estimer ces émissions. Grâce à la précision des données et au détail des ingrédients, vous pouvez obtenir une estimation réaliste des émissions liées à votre repas.<br> <a style="color: #007bff;" href="#tuto">Voir le tuto du site en bas de page</a>
        </p>
        <h3 style="color: #e3541a;">Public cible</h3>
        <p style="text-align: justify;margin-bottom: 20px;">
            Notre outil s'adresse à un large public. Que vous soyez un individu soucieux de l'environnement cherchant à réduire votre empreinte carbone ou un professionnel de la restauration collective cherchant à optimiser vos recettes, notre site est conçu pour vous.
        </p>
        <h3 style="color: #e3541a;">Notre équipe</h3>
        <p style="text-align: justify;margin-bottom: 20px;">
          Ce projet a été réalisé par une équipe d'étudiants de l'Université Lyon 1 : Adrien Raimbault, Batiste Bonnal, Kuan Hua Tu, Solène Medina, Louis Sanglier et Jules Travard, sous la supervision d'un collectif de personnels Lyon1 pour qui la transition écologique est une priorité : Vincent Lacroix, Bastien Boussau, Anne-Laure Fougères, Nadine Badr, Marie Le Merrer, François Toche. Une première version avait été réalisée par Maude Gallimard, encadrée par Bastien Boussau et Mathilde Paris. La mise en place de ce service web a été rendue possible par Philippe Malbos, Gilles Rech, Guillaume Frambourg, Stéphane Delmotte et Julien Barnier.
        </p>
        <h3 style="color: #e3541a;">Ressources supplémentaires</h3>
        <br>
        <div class="d-flex flex-row">
          <v-img 
          src="..\..\static\img\alimentation_GES_V1_bonpote_page-0001.jpg"></v-img>
        </div>
        <br>
        <p style="text-align: center;margin-bottom: 20px;">Illustration provenant du site <a href="https://bonpote.com/les-infographies-bon-pote/" target="_blank" style="color: #007bff;">bonpote</a></p>
        <ul style="margin-left: 20px;">
            <li><a href="../../static/img/PresentationGTPSE_v2.pdf" target="_blank" style="color: #007bff;">Téléchargez la présentation faite par le groupe au GT PSE (Plan de Sobriété Énergétique) de l'Université Lyon 1 (PDF)</a></li>
            <li><a href="https://foad.univ-lyon1.fr/course/view.php?id=13&section=7" target="_blank" style="color: #007bff;text-decoration: none;">Accédez à la partie "Agriculture et Alimentation" du MOOC "Climat et Transitions" dispensée à tous les étudiants L1 Sciences de l'Université Lyon 1 (lien vers le MOOC)</a></li>
        </ul>
        <br>
        <h3 style="color: #e3541a;">Aide d'utilisation pour le site</h3>
        <br>
        <div  class="d-flex flex-row">
        <video id="tuto" style="max-width: 100%; height: auto;" controls>
      <source src="..\..\static\img\Demo_Alimempreinte.mp4" type=video/mp4>
    </video>
  </div>
    </div>
</body>
</template>
