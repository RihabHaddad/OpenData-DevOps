
import psycopg2
import os
import json


def get_connection():
    """Get database connection from environment variables ONLY."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def analyze():
    """Run analysis and export results."""
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n" + "="*60)
    print("JARDINS PARTAGÉS - ANALYSIS")
    print("="*60 + "\n")
    
    # Total count
    cur.execute("SELECT COUNT(*) FROM jardins_partages")
    total = cur.fetchone()[0]
    print(f" Total gardens: {total}\n")
    
   
    cur.execute("""
        SELECT 
            arrondissement,
            COUNT(*) as count
        FROM jardins_partages
        WHERE arrondissement IS NOT NULL
        GROUP BY arrondissement
        ORDER BY count DESC
    """)
    
    print("Distribution by arrondissement:")
    distribution = []
    for row in cur.fetchall():
        arr, count = row
        print(f"   {arr}: {count} gardens")
        distribution.append({"arrondissement": arr, "count": count})
    
    
    print("\n Sample garden names:")
    cur.execute("SELECT nom FROM jardins_partages LIMIT 10")
    for row in cur.fetchall():
        print(f"   - {row[0]}")
    
    print("\n" + "="*60 + "\n")
    
    
    os.makedirs("results", exist_ok=True)
    
    results = {
        "total_gardens": total,
        "distribution": distribution
    }
    
    with open("results/analysis.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(" Results exported to results/analysis.json\n")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    analyze()