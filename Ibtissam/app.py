from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np

# Initialisation de l'application Flask
app = Flask(__name__)

# Charger le modèle
with open('C:\\Users\\t14\\Desktop\\Doctorat\\Ibtissam\\Ibtissam\\modele_cancer_colon.pkl', 'rb') as fichier:
    modele = pickle.load(fichier)

# Route principale - page d'accueil
@app.route('/')
def accueil():
    return render_template('index.html')

# Route pour la prédiction
@app.route('/predire', methods=['POST'])
def predire():
    # Récupération des données du formulaire
    try:
        age = float(request.form['age'])
        niveau_cea = float(request.form['niveau_cea'])
        taille_polype = float(request.form['taille_polype'])
        grade_tumeur = float(request.form['grade_tumeur'])
        
        resultat_coloscopie = request.form['resultat_coloscopie']
        antecedents_familiaux = request.form['antecedents_familiaux']
        resultat_biopsie = request.form['resultat_biopsie']
        implication_ganglions = request.form['implication_ganglions']
        obstruction_intestinale = request.form['obstruction_intestinale']
        tabagisme = request.form['tabagisme']
        
        # Préparation des données pour la prédiction
        donnees_patient = {
            'AGE': age,
            'CEA Level': niveau_cea,
            'Polyp Size (mm)': taille_polype,
            'Tumor Grade': grade_tumeur,
            'Colonoscopy Result_Normal': 1 if resultat_coloscopie == 'Normal' else 0,
            'Family History_Yes': 1 if antecedents_familiaux == 'Oui' else 0,
            'Biopsy Result_Positive': 1 if resultat_biopsie == 'Positif' else 0,
            'Lymph Node Involvement_Yes': 1 if implication_ganglions == 'Oui' else 0,
            'Bowel Obstruction_Yes': 1 if obstruction_intestinale == 'Oui' else 0,
            'Smoking History_Smoker': 1 if tabagisme == 'Fumeur' else 0
        }
        
        # Conversion en DataFrame
        patient_df = pd.DataFrame([donnees_patient])
        
        # Prédiction
        prediction = modele.predict(patient_df)[0]
        
        # Détermination du type de cancer
        type_cancer = ""
        caracteristiques = ""
        
        if prediction == 0:
            type_cancer = "Cancer de Type 1: Adénocarcinome"
            caracteristiques = "Le type le plus courant. Se forme dans les glandes qui tapissent le côlon."
        elif prediction == 1:
            type_cancer = "Cancer de Type 2: Adénocarcinome mucineux"
            caracteristiques = "Contient au moins 50% de mucine, souvent plus agressif."
        elif prediction == 2:
            type_cancer = "Cancer de Type 3: Carcinome à cellules en bague à chaton"
            caracteristiques = "Forme rare et agressive, les cellules ressemblent à des bagues à chaton."
        
        # Renvoyer le résultat
        return render_template('resultat.html', 
                              prediction=int(prediction),
                              type_cancer=type_cancer, 
                              caracteristiques=caracteristiques)
    
    except Exception as e:
        return jsonify({'erreur': str(e)})

# Point d'entrée de l'application
if __name__ == '__main__':
    app.run(debug=True)