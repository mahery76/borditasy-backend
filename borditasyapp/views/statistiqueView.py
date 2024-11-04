from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection



@api_view(['GET'])
def get_product_statistics(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    with connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT 
                    p.id AS produit_id,
                    p.nom_produit,
                    COALESCE(SUM(c.qte_produit), 0) AS total_quantity_sold,
                    COALESCE(SUM(c.qte_produit * c.prix_vente), 0) AS total_profit
                FROM 
                    borditasyapp_produit p
                LEFT JOIN 
                    commandePrice c ON p.id=c.produit_id
                    and 
                    c.date_facture BETWEEN %s AND %s
                GROUP BY 
                    p.id, p.nom_produit
                ORDER BY total_profit desc
            """,
            [start_date, end_date]
        )
        rows = cursor.fetchall()

    statistics = []
    for row in rows:
        statistics.append({
            'produit_id': row[0],
            'nom_produit': row[1],
            'total_quantity_sold': row[2],
            'total_profit': row[3],
        })

    return Response(statistics)



@api_view(['GET'])
def get_product_statistics_dashboard(request):
    product_id = request.GET.get('productId')
    year = request.GET.get('year')

    # Set start and end date for the specified year
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    with connection.cursor() as cursor:
        cursor.execute(
            """
            WITH months AS (
                SELECT generate_series(
                    DATE_TRUNC('month', %s::date), 
                    DATE_TRUNC('month', %s::date), 
                    '1 month'::interval
                ) AS month_start
            )
            SELECT 
                EXTRACT(MONTH FROM m.month_start) AS month,
                p.id AS produit_id,
                p.nom_produit,
                COALESCE(SUM(c.qte_produit), 0) AS total_quantity_sold,
                COALESCE(SUM(c.qte_produit * c.prix_vente), 0) AS total_profit
            FROM 
                months m
            LEFT JOIN 
                borditasyapp_produit p ON p.id = %s
            LEFT JOIN 
                commandePrice c ON p.id = c.produit_id 
                                 AND c.date_facture >= m.month_start 
                                 AND c.date_facture < (m.month_start + INTERVAL '1 month')
            GROUP BY 
                month, p.id, p.nom_produit
            ORDER BY 
                month;
            """,
            [start_date, end_date, product_id]
        )
        rows = cursor.fetchall()

    # Parse the results
    statistics = []
    for row in rows:
        statistics.append({
            'month': int(row[0]),  # Convert month to integer
            'produit_id': row[1],
            'nom_produit': row[2],
            'total_quantity_sold': row[3],
            'total_profit': row[4],
        })

    return Response(statistics)
