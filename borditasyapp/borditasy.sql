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