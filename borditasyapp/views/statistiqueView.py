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
