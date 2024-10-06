CREATE VIEW prix_produit AS
SELECT p.*, pp.prix_produit
FROM Produit p
JOIN (
    SELECT produit_id, prix_produit, MAX(date_prix_produit) AS latest_date
    FROM PrixProduit
    GROUP BY produit_id, prix_produit
) pp
ON p.id = pp.produit_id
AND pp.date_prix_produit = (
    SELECT MAX(date_prix_produit)
    FROM PrixProduit
    WHERE produit_id = p.id
);
