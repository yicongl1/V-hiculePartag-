#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 17:01:25 2024

@author: nf18p114

Spyder Editor

This is a script file.
"""

import psycopg2

HOST = "tuxa.sme.utc"
USER = "nf18p114"
PASSWORD = ""
DATABASE = "dbnf18p114"

#pour la creation de user, il faut check si le pseudo est pris
def check_pseudo_availability(connection, username):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Utilisateur WHERE pseudo = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            print("Le nom d'utilisateur est déjà pris.")
            return False
        else:
            print("Le nom d'utilisateur est disponible.")
            return True
    except psycopg2.Error as e:
        print("Erreur lors de la vérification de l'existence du nom d'utilisateur:", e)
        return False

#Verification de mot de passe
def login(connection, username, password):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Utilisateur WHERE pseudo = %s AND mot_de_passe = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            print("Connexion réussie")
            return user[2]  # Renvoyer le type d'utilisateur
        else:
            print("Nom d'utilisateur ou mot de passe incorrect")
            return None
    except psycopg2.Error as e:
        print("Échec de la connexion:", e)
        return None

#inserer nouveau proprietaire
def insert_new_proprietaire_with_input(connection, pseudo):
    try:
        cursor = connection.cursor()
        photo = input("Photo: ")
        telephone = input("Téléphone: ")
        email = input("Email: ")
        nom = input("Nom: ")
        prenom = input("Prénom: ")
        age = int(input("Age: "))
        insert_query = "INSERT INTO Proprietaire (pseudo, photo, telephone, email, nom, prenom, age) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(insert_query, (pseudo, photo, telephone, email, nom, prenom, age))
        connection.commit()
        print("Nouveau propriétaire inséré avec succès !")
    except psycopg2.Error as error:
        print("Erreur lors de l'insertion du nouveau propriétaire:", error)

#inserer nouveau locataire
def insert_new_locataire_with_input(connection, pseudo):
    try:
        cursor = connection.cursor()
        photo = input("Photo: ")
        telephone = input("Téléphone: ")
        email = input("Email: ")
        permis = input("Permis: ")
        validite = input("Validité: ")
        nom = input("Nom: ")
        prenom = input("Prénom: ")
        age = int(input("Age: "))
        insert_query = "INSERT INTO Locataire (pseudo, photo, telephone, email, permis, validite, nom, prenom, age) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(insert_query, (pseudo, photo, telephone, email, permis, validite, nom, prenom, age))
        connection.commit()
        print("Nouveau locataire inséré avec succès !")
    except psycopg2.Error as error:
        print("Erreur lors de l'insertion du nouveau locataire:", error)

#inserer nouvelle entreprise
def insert_new_entreprise_with_input(connection, pseudo):
   try:
       cursor = connection.cursor()
       photo = input("Photo: ")
       telephone = input("Téléphone: ")
       email = input("Email: ")
       nom = input("Nom: ")
       adresse = input("Adresse: ")
       ville = input("Ville: ")
       code_postal = input("Code postal: ")
       insert_query = "INSERT INTO Entreprise (pseudo, photo, telephone, email, nom, adresse, ville, code_postal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
       cursor.execute(insert_query, (pseudo, photo, telephone, email, nom, adresse, ville, code_postal))
       connection.commit()
       print("Nouvelle entreprise insérée avec succès !")
   except psycopg2.Error as error:
       print("Erreur lors de l'insertion de la nouvelle entreprise:", error)

#creation d’utilisateur
def create_user(connection):
    pseudo = input("Veuillez entrer un nom d'utilisateur : ")
    while not check_pseudo_availability(connection, pseudo):
        pseudo = input("Veuillez entrer un autre nom d'utilisateur : ")
    
    password = input("Veuillez entrer un mot de passe : ")
    confirm_password = input("Veuillez confirmer votre mot de passe : ")
    while password != confirm_password:
        print("Les mots de passe ne correspondent pas.")
        password = input("Veuillez entrer un mot de passe : ")
        confirm_password = input("Veuillez confirmer votre mot de passe : ")
    
    user_type = input("Veuillez entrer le type d'utilisateur (proprietaire/locataire/entreprise) : ")
    while user_type not in ["proprietaire", "locataire", "entreprise"]:
        print("Type d'utilisateur invalide.")
        user_type = input("Veuillez entrer le type d'utilisateur (proprietaire/locataire/entreprise) : ")
    
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Utilisateur (pseudo, mot_de_passe, type, actif) VALUES (%s, %s, %s, TRUE)", (pseudo, password, user_type))
        connection.commit()
        print("Utilisateur créé avec succès.")
        cursor.close()

        # Appeler la fonction correspondante en fonction du type d'utilisateur
        if user_type == "proprietaire":
            insert_new_proprietaire_with_input(connection, pseudo)
        elif user_type == "locataire":
            insert_new_locataire_with_input(connection, pseudo)
        elif user_type == "entreprise":
            insert_new_entreprise_with_input(connection, pseudo)
    except psycopg2.Error as e:
        print("Erreur lors de la création de l'utilisateur :", e)

#inserer nouvelle annonce
def insert_new_announcement_with_input(connection):
    try:
        cursor = connection.cursor()
        activite = input("Activité (True/False): ")
        intitule = input("Intitulé (Voiture à louer): ")
        nombre_signalement = 0
        note = float(input("Note (Entre 0 et 5): "))
        vehicule = input("Véhicule (AB-123-CD): ")
        insert_query = "INSERT INTO Annonce (activite, intitule, nombre_signalement, note, vehicule) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(insert_query, (activite, intitule, nombre_signalement, note, vehicule))
        connection.commit()
        print("Nouvelle annonce insérée avec succès !")
    except psycopg2.Error as error:
        print("Erreur lors de l'insertion de la nouvelle annonce:", error)

try:
    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
    print("Connexion à la BDD réussie")
    
    
    """choix = ''
    while (choix != 'oui' and choix != 'non') :
        print("choix invalide, veuillez recommencer")
        choix = str(input("Voulez vous faire une rehcerche par critères (oui/non)\n"))"""
    
    """#test existence pseudo
    pseudo_test = "Gagnos"
    check_pseudo_availability(conn, pseudo_test)
    pseudo_test = "NewPseudo"
    check_pseudo_availability(conn, pseudo_test)
    
    #test pouvoir se connecter
    pseudo_test = "Gagnos"
    print("Login: ", pseudo_test)
    password_test = str(input("Password: "))
    type_test = login(conn, pseudo_test, password_test)
    if (type_test != None):
        print("Vous êtes", type_test)
    
    #test ajouter une annonce
    print("Vous allez ajouter une annonce, veuillez renseigner les informations")    
    if (type_test == "proprietaire"):
        insert_new_announcement_with_input(conn)
    else:
        print("Vous n'êtes pas proprietaire, vous ne pouvez pas ajouter d'annonce !")"""
        
    #test ajouter un utilisateur
    print("Vous allez vous inscrire, veuillez renseigner les informations") 
    create_user(conn)
    
    
except Exception as error:
    print("Une exception s'est produite : ", error)
    print("Type D'Exception' : ", type(error))
    
    #écriture
    """cur = conn.cursor()
    cur.execute("")
    conn.commit()"""
    
    #lecture
    """cur.execute("")
    #cur.fetchone()
    cur.fetchall()"""
    
    #A faire sur Postgre : Création BDD et enregistrement fichier csv
    """cur.execute("DROP TABLE IF EXISTS dpt2;")
    cur.execute("CREATE TABLE dpt2(num INTEGER PRIMARY KEY, nom VARCHAR NOT NULL UNIQUE, population INTEGER  NOT NULL CHECK(population>0));")
    conn.commit()
    print("Création de table réussie")"""
    
    """cur.execute("\copy dpt2 (num, nom, population) FROM '/volsme/users/nf18p114/Documents/fichier.csv' WITH CSV HEADER DELIMITER ';';")     
    conn.commit()
    print("Chargement du fichier csv réussi")"""
    
    """"print(cur.fetchall())"""
    
    """ cur = conn.cursor()
    
    #chercher le login d'un utilisateur
    cur.execute("SELECT * FROM dpt2;")
                                                         
    #lecture ligne et affichage
    print("[N°] Nom (Population)")
    raw = cur.fetchone()
    while raw:
        print ("[0%i] %s (%i)" % (raw[0], raw[1], raw[2]))
        #print ("[",raw[0],"] ",raw[1]," (",raw[2],")")
        raw = cur.fetchone()
    #print("Visualisation de table réussie")
    
    #chercher les min-max population dans bdd
    cur.execute("SELECT MIN(population), MAX(population) FROM dpt2;")    
    raw = cur.fetchone()
    print ("Département le plus peuplé : %i\nDépartement le moins peuplé : %i" % (raw[1], raw[0]))
    
    #insérer new dpts dans bdd
    #sql = "INSERT INTO dpt2 VALUES ();"
    #cur.execute(sql)
    
    conn.close()"""
    
