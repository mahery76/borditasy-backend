CREATE VIEW list_stock AS
            SELECT * FROM 
                borditasyapp_stock s
            WHERE prix_vente is not null;


CREATE VIEW list_depense AS
            SELECT * FROM 
                borditasyapp_stock s
            WHERE prix_vente is null;


CREATE OR REPLACE VIEW ProductWithActualPrice AS
            SELECT p.id, p.nom_produit, s.prix_vente, s.prix_achat_dep
            FROM borditasyapp_Produit p
            JOIN (
                SELECT produit_id, prix_vente, prix_achat_dep
                FROM borditasyapp_Stock s1
                WHERE date_stock = (
                    SELECT MAX(date_stock)
                    FROM borditasyapp_Stock s2
                    WHERE s1.produit_id = s2.produit_id
                )
            ) s
            ON p.id = s.produit_id ORDER BY p.nom_produit;

CREATE VIEW stock_with_remaining AS
            SELECT 
                s.produit_id,
                COALESCE(s.total_stock, 0) - COALESCE(c.total_commande, 0) AS remaining_stock
            FROM 
                (SELECT produit_id, SUM(quantite_stock) AS total_stock
                FROM list_stock
                GROUP BY produit_id) s
            LEFT JOIN 
                (SELECT produit_id, SUM(qte_produit) AS total_commande
                FROM borditasyapp_commande
                GROUP BY produit_id) c
            ON s.produit_id = c.produit_id;


CREATE OR REPLACE VIEW ProductStatistics AS
SELECT 
    p.id AS produit_id,
    p.nom_produit,
    COALESCE(SUM(c.qte_produit), 0) AS total_quantity_sold,
    COALESCE(SUM(c.qte_produit * s.prix_vente), 0) AS total_profit
FROM 
    borditasyapp_Produit p
LEFT JOIN 
    borditasyapp_Commande c ON p.id = c.produit_id
LEFT JOIN 
    borditasyapp_Facture f on f.id=c.facture_id
LEFT JOIN 
    borditasyapp_Stock s ON p.id = s.produit_id 
    AND f.date_facture BETWEEN s.date_stock AND (
        SELECT MAX(date_stock) 
        FROM borditasyapp_Stock s2 
        WHERE s2.produit_id = s.produit_id 
        AND s2.date_stock >= f.date_facture
    )
GROUP BY 
    p.id, p.nom_produit;


CREATE OR REPLACE VIEW CommandePrice AS
            SELECT 
                c.id AS commande_id,
                c.produit_id,
                c.qte_produit,
                f.date_facture,
                s.prix_vente,
                s.prix_achat_dep,
                COALESCE(s.prix_vente * c.qte_produit, 0) AS total_price
            FROM 
                borditasyapp_Commande c
            JOIN 
                borditasyapp_Facture f ON c.facture_id = f.id
            LEFT JOIN 
                borditasyapp_Stock s ON c.produit_id = s.produit_id 
            and 
                s.date_stock = (
                    SELECT MAX(date_stock) 
                    FROM borditasyapp_Stock s2 
                    WHERE s2.produit_id = s.produit_id 
                    AND s2.date_stock <= f.date_facture
                );
