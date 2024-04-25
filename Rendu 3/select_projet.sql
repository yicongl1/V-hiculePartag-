--Moyenne d’âge : 
SELECT AVG(annee_mise_circulation) AS moyenne_age
FROM Vehicule;

--Kilométrage total
SELECT AVG(kilometrage) AS _kilometrage
FROM Vehicule;

--Catégories les plus utilisées : 
SELECT categorie, COUNT(*) AS nombre_annonces
FROM Vehicule V
JOIN Annonce A ON V.immatriculation = A.vehicule
GROUP BY categorie
ORDER BY nombre_annonces DESC;

