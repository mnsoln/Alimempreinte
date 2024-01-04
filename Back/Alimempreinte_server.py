from flask import Flask, render_template, request, Response, make_response, redirect, url_for, jsonify
import python3_libs.ecofood_lib as ecofood_lib
import python3_libs.SQL_queries as SQL_queries
import sqlite3
from io import BytesIO
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from kaleido.scopes.plotly import PlotlyScope
import plotly.io as pio
import plotly.offline as pyo

app = Flask(__name__, template_folder='template', static_folder='static')

'''
Page d'accueil
'''
@app.route('/', methods=['GET'])
def upload_form():
    data = SQL_queries.querySavedResults()
    return render_template('homepage.html', savedResults=data, public=True)

@app.route('/crous', methods=['GET'])
def upload_form_crous():
    data = SQL_queries.queryCrousResults()
    return render_template('homepage.html', savedResults=data, public=False)

@app.route('/admin', methods=['GET'])
def upload_form_admin():
    data = SQL_queries.querySavedResults()
    return render_template('homepage.html', savedResults=data, admin=True)

@app.route('/research', methods=["GET"])
def search():
    result = SQL_queries.queryData(request.args.get('query'))
    response = make_response( dict(result = result ), 200 )
    response.headers = {"Content-Type" : "application/json"}
    return response

@app.route('/logo', methods=['GET'])
def logo():
    co2 = request.args.get('eCO2')
    logoToComplete = "./static/img/logo-a-completer.png"
    logo = ecofood_lib.create_logo(logoToComplete, float(co2))
    buf = BytesIO()
    logo.save(buf, "png")   
    response = make_response(buf.getvalue())
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = 'inline'
    return response

@app.route('/download', methods=['GET', 'POST'])
def download():
    co2 = request.form.get('co2')
    meal_name = request.form.get('meal_name')
    buf = BytesIO()
    ecofood_lib.afficher_logo("./static/img/crous.png",buf,meal_name,float(co2),"./static/img/logo-a-completer.png")
    
    response = make_response(buf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment;filename={meal_name}.pdf'
    return response

@app.route('/download/multiple', methods=['GET', 'POST'])
def download2():
    data = request.form.get('data')
    ids = data.split(';')  # Diviser la chaîne en une liste d'identifiants
    results = SQL_queries.querySavedResultsWithIds(tuple(ids))
    buf = BytesIO()
    ecofood_lib.afficher_logo2("./static/img/finalcafet.png", buf, "./static/img/logo-a-completer.png", results)
    response = make_response(buf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=download.pdf'
    return response

'''
Suppression des plats enregistrés
'''
@app.route('/deleteCheckbox', methods=['POST'])
def delete_checkbox():
    checkbox_id = request.form.get('id')
    print(checkbox_id)
    SQL_queries.removeSavedResultsWithIds(checkbox_id)
    answer = redirect(url_for('upload_form'))
    print(answer)
    return answer


'''
Enregistrement des plats depuis la page de saisie manuelle
'''
@app.route('/save', methods=['GET'])
def save():
    kg_CO2 = request.args.get('kg_CO2')
    meal_name = request.args.get('meal_name')
    proteines = request.args.get('Proteines')
    glucides = request.args.get('Glucides')
    sucres = request.args.get('Sucres')
    lipides = request.args.get('Lipides')
    ingredients = request.args.get('Ingredients')
    SQL_queries.saveData(kg_CO2,meal_name, proteines, glucides, sucres, lipides, ingredients)
    return redirect(url_for('upload_form'))

'''
Enregistrement des plats depuis la page de saisie manuelle crous
'''
@app.route('/saveCrous', methods=['GET'])
def saveCrous():
    kg_CO2 = request.args.get('kg_CO2')
    meal_name = request.args.get('meal_name')
    proteines = request.args.get('Proteines')
    glucides = request.args.get('Glucides')
    sucres = request.args.get('Sucres')
    lipides = request.args.get('Lipides')
    ingredients = request.args.get('Ingredients')
    SQL_queries.saveCrousData(kg_CO2,meal_name, proteines, glucides, sucres, lipides, ingredients)
    return redirect(url_for('upload_form_crous'))

'''
Enregistrement des plats depuis la page de saisie manuelle admin
'''
@app.route('/saveAdmin', methods=['GET'])
def saveAdmin():
    kg_CO2 = request.args.get('kg_CO2')
    meal_name = request.args.get('meal_name')
    proteines = request.args.get('Proteines')
    glucides = request.args.get('Glucides')
    sucres = request.args.get('Sucres')
    lipides = request.args.get('Lipides')
    ingredients = request.args.get('Ingredients')
    SQL_queries.saveData(kg_CO2,meal_name, proteines, glucides, sucres, lipides, ingredients)
    return redirect(url_for('upload_form_admin'))

@app.route('/upload', methods=['POST'])
def upload():
    tree = getTree(request)
    response = make_response( tree, 200 )
    response.headers = {"Content-Type" : "application/json"}
    return response

def getTree(request):
    data = dict(request.form)
    files = dict(request.files)
    meal = data["meal"]
    nb_points = data["nb_points"]
    uploaded = files["fiche_technique"] 

    if not uploaded or not "application/pdf" == uploaded.content_type:
        return "Not authorized, bad request", 403
    ecofood_ademe = SQL_queries.searchData()

    supplierChain = ecofood_lib.PDFTemplateSupplierChain(uploaded)
    tree = supplierChain.extract_ingredient()
    resolveSuggestion(tree,ecofood_ademe)
    
    cleanParent(tree)
    tree["meal"]=meal
    tree["nb_points"]=nb_points
    return tree

@app.route('/upload/html', methods=['POST'])
def upload_html():
    tree = getTree(request)
    return render_template("result.html", tree=tree)

def cleanParent(node):
  if "parent" in node:  
    del node["parent"]
  for child in node["children"]:
    cleanParent(child)


####### methode de Levenshtein en jaro #########
####### https://maxbachmann.github.io/Levenshtein/levenshtein.html#jaro

# def addLevenshtein(ingredient,name):
#     return dict(
#         name = ingredient["name"], 
#         category= ingredient["category"], 
#         co2= ingredient["co2"], 
#         id= ingredient["id"], 
#         similarity= lev.jaro(name.lower(), ingredient["name"].lower()) ) 

def resolveSuggestion(node, liste):
    if "ingredient" in node and len(node["ingredient"])>0:  
        newListe = list(map(lambda ingredient : addLevenshtein(ingredient, node["ingredient"]),liste))
        newListe.sort(key = lambda x : x["similarity"], reverse=True)
        node["suggestion"] = newListe[0:10]
    for child in node["children"]:
        resolveSuggestion(child,liste)
     
'''
Accès à la page de saisie manuelle
'''
@app.route("/manual/input", methods=["POST"])
def saisieRecette():
    ingredients = request.form.getlist("ingredients")
    print(ingredients, type(ingredients))
    if ingredients != []:
        nbPortions = ingredients[0].split(";")[0].split(":")[1]
        listeIngredients=[]
        for elt in ingredients[0].split(";")[1:-1]:
            listeIngredients.append((elt.split(":")[0], elt.split(":")[1]))
        print(listeIngredients)
    else:
        nbPortions = 1
    return render_template("manualInput.html", meal_name=request.args.get("meal_name"), nbPortions=nbPortions)

'''
Accès à la page de saisie manuelle pour la version crous
'''
@app.route("/manual/input/crous", methods=["GET", "POST"])
def saisieCrous():
    ingredients = request.form.getlist("ingredients")
    print(ingredients, type(ingredients))
    if ingredients != []:
        nbPortions = ingredients[0].split(";")[0].split(":")[1]
        listeIngredients=[]
        for elt in ingredients[0].split(";")[1:-1]:
            listeIngredients.append((elt.split(":")[0], elt.split(":")[1]))
        print(listeIngredients)
    else:
        nbPortions = 1
    return render_template("manualInputCrous.html", meal_name=request.args.get("meal_name"), nbPortions=nbPortions)

'''
Accès à la page de saisie manuelle pour la version admin
'''
@app.route("/manual/input/admin", methods=["GET", "POST"])
def saisieAdmin():
    ingredients = request.form.getlist("ingredients")
    print(ingredients, type(ingredients))
    if ingredients != []:
        nbPortions = ingredients[0].split(";")[0].split(":")[1]
        listeIngredients=[]
        for elt in ingredients[0].split(";")[1:-1]:
            listeIngredients.append((elt.split(":")[0], elt.split(":")[1]))
        print(listeIngredients)
    else:
        nbPortions = 1
    return render_template("manualInputAdmin.html", meal_name=request.args.get("meal_name"), nbPortions=nbPortions)



@app.route("/importForm", methods=["POST"])
def importIngredient():
    results = request.form.getlist("choix")
    for result in results:
        values = result.split("|")
        co2 = values[0]
        nom = values[1]
        categorie = values[2]
        ciqual = values[3]
        SQL_queries.importIngredient(co2, nom, categorie, ciqual)
    return Response(status=201)

'''
Création de la jauge
'''
@app.route("/gauge", methods=['POST'])
def jauge():
    form_data = request.form.getlist('result')
    tickvals = [0,20,40,60,80,100]
    ticktext = ['0','20','40','60','80','100']
    steps = [
            {'range': [0, 20], 'color': 'seagreen'},
            {'range': [20, 40], 'color': 'yellowgreen'},
            {'range': [40, 60], 'color': 'gold'},
            {'range': [60, 80], 'color': 'crimson'},
            {'range': [80, 100], 'color': 'darkred'}
            ]

    for entry in form_data:
        steps.append({'color': 'black', 'line': {'color': "black", 'width':3}, 'thickness': 1, 'range': [float(entry.split(',')[2]), float(entry.split(',')[2])]})
        ticktext.append(entry.split(',')[1].replace(' ','\n'))
        tickvals.append(entry.split(',')[2])

        
    fig = go.Figure(go.Indicator(
        mode = "gauge",
        title = {'text': "Empreinte carbone (% du budget quotiden)", 'align': 'left', 'font': {'size': 30}},
        gauge = {
            'axis': {'range': [0, 100], 
            'tickmode': 'array',
            'tickvals': tickvals,
            'ticktext': ticktext,
            'tickwidth': 3,
            'tickfont': {'size': 25}
            },
            'bar': {
            'thickness' : 0.5
            },
            'borderwidth': 1,
            'bordercolor': "white",
            'steps': steps
        }))
    fig.update_layout(paper_bgcolor = "white", font = {'color': "black", 'family': "Arial"}, xaxis = dict(tickmode = "linear", tick0 = 0, dtick = 20))
    # scope = PlotlyScope(plotlyjs="https://cdn.plot.ly/plotly-latest.min.js")
    # print(scope.transform(fig, format= 'svg'))
    pio.write_image(fig, 'static/img/jauge.svg')
    # pyo.plot(fig, filename='static/img/jauge_test.html')
    # return render_template('jauge.html')
    return redirect(url_for('upload_form'))
