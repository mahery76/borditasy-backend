# Generated by Django 5.1 on 2024-10-08 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('borditasyapp', '0007_create_view_list_stock_and_list_depense'),
    ]

    operations = [
        migrations.RunSQL(
            """
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
            """,
            reverse_sql="DROP VIEW IF EXISTS stock_with_remaining;"
        ),
    ]
