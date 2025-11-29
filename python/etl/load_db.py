import os
import psycopg2
import hashlib


def get_connection():
    """Get database connection from environment variables ONLY."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def create_table():
    """Create table if not exists."""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS jardins_partages (
                id TEXT PRIMARY KEY,
                nom TEXT,
                arrondissement TEXT,
                adresse TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes
        cur.execute("CREATE INDEX IF NOT EXISTS idx_nom ON jardins_partages(nom)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_arr ON jardins_partages(arrondissement)")
        
        conn.commit()
        print("✅ Table created/verified")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Table creation failed: {e}")
        raise
    finally:
        cur.close()
        conn.close()

def insert_data(records):
    """Insert data into database."""
    if not records:
        print("⚠️ No records to insert")
        return
    
    conn = get_connection()
    cur = conn.cursor()
    
    inserted = 0
    errors = 0
    
    try:
        for record in records:
            try:
                nom = record.get("nom_ev")
                
                if not nom:
                    continue
                
                # Generate unique ID
                record_id = hashlib.md5(
                    f"{nom}{record.get('adresse', '')}".encode()
                ).hexdigest()
                
                # Insert record
                cur.execute("""
                    INSERT INTO jardins_partages (id, nom, arrondissement, adresse)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (
                    record_id,
                    nom,
                    record.get("arrondissement"),
                    record.get("adresse")
                ))
                
                if cur.rowcount > 0:
                    inserted += 1
                    
            except Exception as e:
                errors += 1
                print(f"⚠️ Failed to insert record: {e}")
                continue
        
        conn.commit()
        print(f" {inserted} records processed successfully")
        
        if errors > 0:
            print(f"⚠️ {errors} records had errors")
            
    except Exception as e:
        conn.rollback()
        print(f" Data insertion failed: {e}")
        raise
    finally:
        cur.close()
        conn.close()