import sqlite3


DATABASE = 'final_database.sql'


def searchData():
    conn =  sqlite3.connect('final_database.sql')
    conn.row_factory = sqlite3.Row
    
    req = 'SELECT id, Nom, Groupe_aliment, kg_CO2 \
            FROM ingredient '
    
    data = conn.execute(req).fetchall()   
    result=[] 
    for d in data:
        result.append(dict(id=d[0],name=d[1],category=d[2],co2=d[3]))
    conn.close()

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
    return result

def saveData(kg_CO2,meal_name, proteines, glucides, sucres, lipides, ingredients):
    '''
    Enregistre une nouvelle instance dans la bd
    '''
    conn =  sqlite3.connect('final_database.sql')
    conn.row_factory = sqlite3.Row
    req = "CREATE TABLE IF NOT EXISTS result (id INTEGER PRIMARY KEY AUTOINCREMENT, kg_CO2 varchar(200), meal_name varchar(200), Proteines varchar(200), Glucides varchar(200), Sucres varchar(200), Lipides varchar(200), Ingredients varchar(2000)); "
    reqinsert = f"INSERT INTO result (kg_CO2, meal_name, Proteines, Glucides, Sucres, Lipides, Ingredients) VALUES('{round(float(kg_CO2), 3)}' ,'{meal_name}', '{round(float(proteines), 2)}','{round(float(glucides), 2)}','{round(float(sucres), 2)}','{round(float(lipides), 2)}','{ingredients}');"
    conn.execute(req)
    conn.execute(reqinsert)
    conn.commit()
    conn.close()

def saveCrousData(kg_CO2,meal_name, proteines, glucides, sucres, lipides, ingredients):
    '''
    Enregistre une nouvelle instance dans la bd
    '''
    conn =  sqlite3.connect('final_database.sql')
    conn.row_factory = sqlite3.Row
    req = "CREATE TABLE IF NOT EXISTS crous (id INTEGER PRIMARY KEY AUTOINCREMENT, kg_CO2 varchar(200), meal_name varchar(200), Proteines varchar(200), Glucides varchar(200), Sucres varchar(200), Lipides varchar(200), Ingredients varchar(2000)); "
    reqinsert = f"INSERT INTO crous (kg_CO2, meal_name, Proteines, Glucides, Sucres, Lipides, Ingredients) VALUES('{round(float(kg_CO2), 3)}' ,'{meal_name}', '{round(float(proteines), 2)}','{round(float(glucides), 2)}','{round(float(sucres), 2)}','{round(float(lipides), 2)}','{ingredients}');"
    conn.execute(req)
    conn.execute(reqinsert)
    conn.commit()
    conn.close()

def querySavedResults(): 
    '''
    Interroge la bd lors de l'arrivée sur la page d'accueil pour afficher les plats enregistrés.
    '''
    conn =  sqlite3.connect('final_database.sql')
    conn.row_factory = sqlite3.Row
    req = "CREATE TABLE IF NOT EXISTS result (id INTEGER PRIMARY KEY AUTOINCREMENT, kg_CO2 varchar(200), meal_name varchar(200), Proteines varchar(200), Glucides varchar(200), Sucres varchar(200), Lipides varchar(200), Ingredients varchar(2000)); "
    conn.execute(req)
    conn.commit()
    req = f'select * \
        from result;'
    
    data = conn.execute(req).fetchall()
    conn.close()
    result=[] 
    for d in data:
        result.append(dict(id=d[0], kg_CO2=d[1], meal_name=d[2], Proteines=d[3], Glucides=d[4], Sucres= d[5], Lipides=d[6], Ingredients=d[7]))
    conn.close()
    return result

def queryCrousResults(): 
    '''
    Interroge la bd lors de l'arrivée sur la page d'accueil pour afficher les plats enregistrés par le CROUS.
    '''
    conn =  sqlite3.connect('final_database.sql')
    conn.row_factory = sqlite3.Row
    req = "CREATE TABLE IF NOT EXISTS crous (id INTEGER PRIMARY KEY AUTOINCREMENT, kg_CO2 varchar(200), meal_name varchar(200), Proteines varchar(200), Glucides varchar(200), Sucres varchar(200), Lipides varchar(200), Ingredients varchar(2000)); "
    conn.execute(req)
    conn.commit()
    req = f'select * \
        from crous;'
    
    data = conn.execute(req).fetchall()
    conn.close()
    result=[] 
    for d in data:
        result.append(dict(id=d[0], kg_CO2=d[1], meal_name=d[2], Proteines=d[3], Glucides=d[4], Sucres= d[5], Lipides=d[6], Ingredients=d[7]))
    conn.close()
    return result


def querySavedResultsWithIds(ids):
    conn =  sqlite3.connect('final_database.sql')
    conn.row_factory = sqlite3.Row
    
    req = "select * from result where result.id in (%s);" % ','.join('?'*len(ids))
    data = conn.execute(req,list(ids)).fetchall()   
    result=[] 
    for d in data:
        result.append(dict(id=d[0],kg_CO2=float(d[1]),meal_name=d[2], Proteines=d[3], Glucides=d[4], Sucres= d[5], Lipides=d[6]))
    conn.close()
    return result

def removeSavedResultsWithIds(id):
    '''
    Suppresion de plats
    '''
    conn =  sqlite3.connect('final_database.sql')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM result WHERE id={id}")
    conn.commit()
    conn.close()      

