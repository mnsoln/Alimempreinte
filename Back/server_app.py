from flask import Flask, request, make_response
import sqlite3
import ecofood_lib as ecofood_lib
import SQL_queries as SQL_queries
import logging as log
from io import BytesIO
import json
import sys


app = Flask(__name__, static_folder='static')


def set_log_level(verbosity: str):
    verbosity = verbosity.lower()
    configs = {
        "debug": log.DEBUG,
        "info": log.INFO,
        "warning": log.WARNING,
        "error": log.ERROR,
        "critical": log.CRITICAL,
    }
    if verbosity not in configs.keys():
        raise ValueError(
            f"Unknown verbosity level: {verbosity}\nPlease use any in: {configs.keys()}"
        )
    log.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=configs[verbosity],
    )


set_log_level("debug")

"""  POUR PRINT LES VARIABLES DANS LE TERMINAL UTILISER :
log.debug(variable) """



def translate_accents(result,accentsalready:bool):
    if not accentsalready:
        final=[]
        for line in result:
            line = line.replace('Ã´','ô')
            line = line.replace('Ã©','é')
            line = line.replace('Ãª','ê')
            line = line.replace('Ã»','û')
            line = line.replace('Ã¢','â')
            line = line.replace('Ã¨','è')
            line = line.replace('Ã\xa0','à')
            line = line.replace('Å“','œ')
            line = line.replace('Ã®','î')
            line = line.replace('Ã«','ë')
            line = line.replace('Ã¯','ï')
            line = line.replace('Ã§','ç')
            
            
            final.append(line)

        return final
    
    elif accentsalready:
            result = result.replace('ô','Ã´')
            result = result.replace('é','Ã©')
            result = result.replace('ê','Ãª')
            result = result.replace('û','Ã»')
            result = result.replace('â','Ã¢')
            result = result.replace('è','Ã¨')
            result = result.replace('à','Ã\xa0')
            result = result.replace('œ','Å“')
            result = result.replace('î','Ã®')
            result = result.replace('ë','Ã«')
            result = result.replace('ï','Ã¯')
            result = result.replace('ç','Ã§')
            return result


def queryData(query):
    '''
    Permet l'interrogation de la bd lors de la recherche par l'utilisateur d'un ingrédient au moment de la saisie de la recette
    '''
    conn =  sqlite3.connect('final_database.sql')
    conn.row_factory = sqlite3.Row
    
    req = f'select id, Nom, kg_CO2, Proteines, Glucides, Sucres, Lipides \
            from ingredient \
            where lower(Nom) collate Latin1_General_CI_AI like lower(\'%{query}%\') collate Latin1_General_CI_AI \
            order by Nom asc '
    data = conn.execute(req).fetchall()
    result=[] 
    for d in data:
        result.append(dict(id=d[0], name=d[1], co2=d[2], Proteines=d[3], Glucides=d[4], Sucres= d[5], Lipides=d[6]))
    conn.close()
    result['charset']='utf-8'
    return result


@app.route('/api/ingredient', methods=['GET','POST'])
def search():
    my_os = sys.platform
    if request.method == "GET":

        """ On renvoie tous les noms des ingredients de la base"""

        conn =  sqlite3.connect('final_database.sql')
        conn.row_factory = sqlite3.Row
        req = 'SELECT Nom, kg_cO2 FROM ingredient '
        data = conn.execute(req).fetchall()   
        result=[] 
        co2=[]
        for d in data:
            result.append(d[0])
            co2.append(d[1])
        conn.close()
        if result:
            if "win" in my_os:
                
                result = translate_accents(result,False)

            for i in range (len(result)):
                result[i]=result[i] + ' [ '+ co2[i][:-4] + ' kg CO2 eq/kg ] '

            return result
        else :
            raise TypeError
    if request.method == "POST":
        
        """ On cherche les infos dans la base du nom d'ingrédient donné """

        post_data = request.get_json()
        if post_data['inputName'] is not None :
            post_data['inputName'] = post_data['inputName'].split(' [')[0]
            if "win" in my_os:
                input_name = translate_accents(post_data['inputName'],True)
    
            else :
                input_name = post_data['inputName']
            result = SQL_queries.queryData(input_name)

            # on prend l'entrée la plus courte (=exacte)
            result = min(result, key=lambda d: len(d["name"]))
            response = make_response( dict(result  = result  ), 200 )
            response.headers = {"Content-Type" : "application/json"}
            return response
        else : return {"status": "missing"}



""" On crée et renvoie la jauge """

@app.route('/api/jauge', methods=['POST','GET'])
def logo():
    co2 = request.args.get('eCO2')
    logoToComplete = "./static/img/logo-a-completer.png"
    logo, color = ecofood_lib.create_logo(logoToComplete, float(co2))
    buf = BytesIO()
    logo.save(buf, "png")   
    response = make_response(buf.getvalue())
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = 'inline'
    return response


""" On crée et renvoie la couleur de la jauge """
@app.route('/api/jauge-color', methods=['POST','GET'])
def logo_color():
    co2 = request.args.get('eCO2')
    logoToComplete = "./static/img/logo-a-completer.png"
    logo, color = ecofood_lib.create_logo(logoToComplete, float(co2))
    return color


'''
Enregistrement des plats depuis la page de saisie manuelle
'''

@app.route("/api/recipes-admin", methods=["GET", "POST"])
def recipes_admin():
    if request.method == "POST": #on sauvegarde
        post_data = request.get_json()

        # Charger les données existantes depuis le fichier
        try: 
            with open('recipes/admin.json', "r") as recipes:
                all_recipes = json.load(recipes)
            
        except: #si le fichier n'existe pas
            all_recipes=[]
        # Enlever l'objet qu'on ajoute si il existe déjà (écraser)
        right_recipes= [plat for plat in all_recipes if plat["name"] != post_data[0]["name"]]


        right_recipes.extend(post_data)

        with open('recipes/admin.json', "w") as recipes:
            json.dump(right_recipes, recipes)
        return {"status": "success"}

    elif request.method == "GET": #on cherche les recettes sauvegardées
        try:
            with open('recipes/admin.json', "r") as recipes:
                data = recipes.read()
        except:
            data=[]
        return data

    else:
        raise NotImplementedError("Only GET and POST requests implemented")
    

@app.route("/api/recipes-crous", methods=["GET", "POST"])
def recipes_crous():
    if request.method == "POST": #on sauvegarde
        post_data = request.get_json()

        # Charger les données existantes depuis le fichier
        try:
            with open('recipes/crous.json', "r") as recipes:
                all_recipes = json.load(recipes)
        except: #si le fichier n'existe pas
            all_recipes=[]

        right_recipes= [plat for plat in all_recipes if plat["name"] != post_data[0]["name"]]
        right_recipes.extend(post_data)
        # Écrire la liste complète dans le fichier
        with open('recipes/crous.json', "w") as recipes:
            json.dump(right_recipes, recipes)

        return {"status": "success"}

    elif request.method == "GET": #on cherche les recettes sauvegardées
        try:
            with open('recipes/crous.json', "r") as recipes:
                data = recipes.read()
        except:
            data=[]
        return data

    else:
        raise NotImplementedError("Only GET and POST requests implemented")
    



@app.route("/api/delete-recipes", methods=["POST"])
def delete_recipes_admin():
    if request.method == "POST":
        post_data = request.get_json()
        

        if post_data['droits'] == 'crous':
            filename = 'recipes/crous.json'
        else : filename = 'recipes/admin.json'

        #récupérer le nom de la recette à supprimer
        to_delete = post_data["recette"]["name"]

        #récupérer toutes les recettes
        with open(filename, "r") as recipes:
            all_recipes = json.load(recipes)

        #supprimer la recette
        for i in range(len(all_recipes)):
            if all_recipes[i-1]["name"]==to_delete:
                all_recipes.pop(i-1)

        #réecrire le fichier
        with open(filename, "w") as recipes:
            json.dump(all_recipes, recipes)
        return {"status": "success"}


    else:
        raise NotImplementedError("Only GET and POST requests implemented")
    


"""Chercher les ingredients d'une recette"""

@app.route("/api/search-recipe", methods=["POST"])
def search_recipe():
    res = {"status": "missing"}
    post_data = request.get_json()
    
    # Charger les données existantes depuis le fichier
    with open('recipes/admin.json', "r") as recipes:
        all_recipes = json.load(recipes)

    for recipe in all_recipes:
        if recipe["name"] == post_data["name"]:
            res = {"portions" : recipe['portions'], "ingredients": recipe["ingredients"]}
            break

    return res

@app.route("/api/search-recipe-crous", methods=["POST"])
def search_recipe_crous():
    res = {"status": "missing"}
    post_data = request.get_json()
    
    # Charger les données existantes depuis le fichier
    with open('recipes/crous.json', "r") as recipes:
        all_recipes = json.load(recipes)

    for recipe in all_recipes:
        if recipe["name"] == post_data["name"]:
            res = {"portions" : recipe['portions'], "ingredients": recipe["ingredients"]}
            break

    return res
