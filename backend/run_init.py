#!/usr/bin/env python3
"""
Script de vérification et d'initialisation automatique pour kaay-job
"""

import os
import sys
from pathlib import Path

# Charger les variables d'environnement
env_file = Path("/app/backend/.env")
env_vars = {}

if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value.strip('"').strip("'")
                os.environ[key] = env_vars[key]

print("╔══════════════════════════════════════════════════════════════╗")
print("║         🚀 Initialisation de kaay-job                        ║")
print("╚══════════════════════════════════════════════════════════════╝")
print("")
print("🔍 Vérification de la connexion à Supabase...")
print("")

try:
    from supabase import create_client
    
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Variables d'environnement Supabase manquantes")
        print("")
        print("Vérifiez /app/backend/.env")
        sys.exit(1)
    
    print(f"   URL: {supabase_url}")
    print("")
    
    supabase = create_client(supabase_url, supabase_key)
    
    # Tester si les tables existent
    try:
        result = supabase.table('users').select('id').limit(1).execute()
        print("✅ Connexion Supabase réussie")
        print("✅ Tables détectées")
        print("")
        
        # Lancer l'initialisation
        print("═" * 62)
        print("✨ Lancement de l'initialisation des données...")
        print("═" * 62)
        print("")
        
        # Importer et exécuter le script d'initialisation
        sys.path.insert(0, '/app/backend')
        
        # Exécuter init_db_enriched.py
        exec(open('/app/backend/init_db_enriched.py').read())
        
    except Exception as e:
        error_msg = str(e).lower()
        
        if 'does not exist' in error_msg or 'relation' in error_msg or 'table' in error_msg:
            print("⚠️  Connexion OK mais tables manquantes")
            print("")
            print("═" * 62)
            print("📋 CRÉEZ LES TABLES DANS SUPABASE D'ABORD")
            print("═" * 62)
            print("")
            print("1. Ouvrez votre dashboard Supabase :")
            print("   https://supabase.com/dashboard/project/zlgxkhgvkslyksfjjqod")
            print("")
            print("2. Allez dans 'SQL Editor'")
            print("")
            print("3. Créez une nouvelle requête et collez le contenu de :")
            print("   /app/backend/schema.sql")
            print("")
            print("4. Exécutez (Run) le SQL")
            print("")
            print("5. Dans 'Storage', créez 2 buckets publics :")
            print("   - cvs")
            print("   - avatars")
            print("")
            print("6. Relancez ce script :")
            print("   python3 /app/backend/run_init.py")
            print("")
            sys.exit(0)
        else:
            print(f"❌ Erreur SQL : {e}")
            sys.exit(1)
            
except Exception as e:
    print(f"❌ Erreur de connexion : {e}")
    print("")
    print("Vérifiez :")
    print("  1. Que Supabase est accessible depuis internet")
    print("  2. Que vos credentials sont corrects dans /app/backend/.env")
    print("")
    sys.exit(1)
