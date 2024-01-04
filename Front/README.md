# ../alimempreinte

# Backend needed

## Database creation

This repository contains only the front of the alimempreinte website. Please also use the backend in http://pedago-service.univ-lyon1.fr:2325/smedina/alimenpreinte_server . Then:

Download the two databases to merge : 
- Agribalyse : https://doc.agribalyse.fr/documentation/utiliser-agribalyse/acces-donnees
- Ciqual : https://ciqual.anses.fr/#/cms/telechargement/node/20

Use create_database.py script in the backend repository to merge the databases into final_database.sql: 
```sh
pip install openpyxl
pip install xlrd
python create_database.py -AD "AGRIBALYSE3.1.1_produits_alimentaires.xlsx" -AN "Table_Ciqual_2020_FR_2020_07_07.xls"
```
(replace the files with the names of the files you downloaded)

```sh
pip install -r requirements.txt
```
```sh
python ./app.py
```



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

