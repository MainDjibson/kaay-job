#!/bin/bash

# Script de vérification et d'initialisation de kaay-job

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         🚀 Initialisation de kaay-job                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Vérifier la connexion à Supabase
echo "🔍 Vérification de la connexion à Supabase..."
echo ""

cd /app/backend

python3 << 'PYTHON_CHECK'
from supabase import create_client
import os
from dotenv import load_dotenv
import sys

load_dotenv()
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

if not supabase_url or not supabase_key:
    print("❌ Variables d'environnement Supabase manquantes")
    sys.exit(1)

try:
    supabase = create_client(supabase_url, supabase_key)
    
    # Tester si les tables existent
    result = supabase.table('users').select('id').limit(1).execute()
    print("✅ Connexion Supabase réussie")
    print("✅ Tables détectées")
    sys.exit(0)
    
except Exception as e:
    error_msg = str(e).lower()
    
    if 'does not exist' in error_msg or 'relation' in error_msg:
        print("⚠️  Connexion OK mais tables manquantes")
        print("")
        print("📋 ÉTAPES REQUISES :")
        print("")
        print("1. Ouvrez votre dashboard Supabase :")
        print("   https://supabase.com/dashboard/project/zlgxkhgvkslyksfjjqod")
        print("")
        print("2. Allez dans SQL Editor")
        print("")
        print("3. Copiez et exécutez le contenu de :")
        print("   /app/backend/schema.sql")
        print("")
        print("4. Créez les buckets de stockage :")
        print("   - Storage → New bucket → 'cvs' (Public)")
        print("   - Storage → New bucket → 'avatars' (Public)")
        print("")
        print("5. Relancez ce script")
        print("")
        sys.exit(2)
    else:
        print(f"❌ Erreur de connexion : {e}")
        print("")
        print("Vérifiez vos credentials Supabase dans /app/backend/.env")
        sys.exit(1)
PYTHON_CHECK

RESULT=$?

echo ""

if [ $RESULT -eq 0 ]; then
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✨ Prêt à initialiser les données !${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Lancement de l'initialisation..."
    echo ""
    
    python3 init_db_enriched.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}🎉 Données créées avec succès !${NC}"
        echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${BLUE}📧 Comptes disponibles :${NC}"
        echo ""
        echo -e "${YELLOW}👑 Super Admin :${NC}"
        echo "   Email : jiby.njaay@gmail.com"
        echo "   Pass  : M@indjibsoN7"
        echo ""
        echo -e "${YELLOW}🏢 Employeurs (pass: employeur123) :${NC}"
        echo "   - recrutement@tech-dakar.sn"
        echo "   - rh@afribank.sn"
        echo "   - jobs@sonacosmetics.sn"
        echo "   - contact@agritech-solutions.sn"
        echo "   - recrutement@educare-africa.com"
        echo "   - hr@constructbtp.sn"
        echo ""
        echo -e "${YELLOW}👨‍💼 Candidats (pass: candidat123) :${NC}"
        echo "   - amadou.diallo@gmail.com"
        echo "   - fatou.sall@gmail.com"
        echo "   - ousmane.ndiaye@gmail.com"
        echo "   - aissatou.ba@gmail.com"
        echo "   - moussa.fall@gmail.com"
        echo "   - marieme.diop@gmail.com"
        echo "   - ibrahima.sarr@gmail.com"
        echo "   - awa.niang@gmail.com"
        echo ""
        echo -e "${BLUE}📚 Documentation complète : /app/COMPTES_TEST.md${NC}"
        echo ""
    else
        echo ""
        echo -e "${RED}❌ Erreur lors de l'initialisation${NC}"
        echo ""
    fi
    
elif [ $RESULT -eq 2 ]; then
    echo -e "${YELLOW}⏸️  Initialisation en pause${NC}"
    echo ""
    echo "Suivez les étapes ci-dessus puis relancez :"
    echo "  bash /app/backend/init_kaay_job.sh"
    echo ""
else
    echo -e "${RED}❌ Impossible de se connecter à Supabase${NC}"
    echo ""
    echo "Vérifiez votre configuration dans /app/backend/.env"
    echo ""
fi
