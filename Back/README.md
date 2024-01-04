# ../alimenpreinte_server

<p>Alimempreinte est un site web réalisé dans le cadre du projet "Amélioration d'un logiciel de calcul du bilan carbone de notre alimentation" du master Bioinformatique de l'université Lyon 1. Il s’inscrit dans un contexte écologique de plus en plus crucial et important, axé sur la réduction des émissions de carbone associées à l'alimentation. </p>
 <p><b>Ce site a pour principale fonction le calcul de l'empreinte carbone de recettes soumises par les utilisateur, ainsi que des informations nutritionnelles, afin de manger correctement et responsablement. </b></p>

<p> Alimempreinte is a French website created as part of the project "Improving software to calculate the carbon footprint of our food" of the Bioinformatics Master of Lyon, France. It is part of an increasingly crucial and important ecological context, focused on the reduction of carbon emissions associated with food.</p>
<p> <b>The site's main function is to calculate the carbon footprint of recipes submitted by users, as well as providing nutritional information to help them eat correctly and responsibly. </b></p>


## Database creation

Download the two newer databases versions to merge : 
- Agribalyse : https://doc.agribalyse.fr/documentation/utiliser-agribalyse/acces-donnees
- Ciqual : https://ciqual.anses.fr/#/cms/telechargement/node/20

Use create_database.py script to merge the databases into final_database.sql: 
```sh
pip install openpyxl
pip install xlrd
python create_database.py -AD "AGRIBALYSE3.1.1_produits_alimentaires.xlsx" -AN "Table_Ciqual_2020_FR_2020_07_07.xls"
```
(replace the files with the names of the files you downloaded)
# Launch

To launch this backend you will need to use the commands :
```sh
pip install -r requirements.txt
```
Then launch the app.py :
```sh
python ./app.py
```

# Frontend needed

The front of this website is in http://pedago-service.univ-lyon1.fr:2325/smedina/alimempreinte/-/tree/VueJS. Next is the way to install the front end.



## Get Node and npm

https://nodejs.org/en/download 
⚠️ **Warning:** : Choose the Node version > 16.16.0 for an Ubuntu environment (nvm install 16.16.0 and nvm use 16.16.0)

## Project Setup

```sh
npm install
npm install chart.js@3.7.0 vue-chartjs@3.5.0
npm install vue-chartjs@latest chart.js@latest
```


## Compile and Hot-Reload for Development

```sh
npm run dev
```

#### Error
You might get an error if your 5000(backend) port is already in use. To fix it you can change those ports like explained next.

- change the port in the alimempreinte/vite;config.js
- add the port you want to alimenpreinte_server/app.py . It will look like app.run(debug=True, port=the_port_you_want)

