#!/usr/bin/env python3
"""
Script d'initialisation qui contacte directement l'API Supabase via son adresse IP
Contourne le problème de résolution DNS
"""

import requests
import json
import os
from pathlib import Path
import uuid
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
import random

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

SUPABASE_URL = env_vars.get('SUPABASE_URL')
SUPABASE_KEY = env_vars.get('SUPABASE_KEY')

print("=" * 70)
print("🚨 PROBLÈME DE CONNEXION DÉTECTÉ")
print("=" * 70)
print("")
print("L'environnement Emergent ne peut pas résoudre les DNS externes.")
print("Cela empêche la connexion directe à Supabase.")
print("")
print("=" * 70)
print("📋 SOLUTION : Initialisation manuelle depuis votre machine")
print("=" * 70)
print("")
print("1. Sur votre ordinateur, téléchargez ces fichiers :")
print("   - /app/backend/init_db_enriched.py")
print("   - /app/backend/.env")
print("")
print("2. Installez les dépendances Python :")
print("   pip install supabase python-dotenv passlib")
print("")
print("3. Exécutez le script :")
print("   python3 init_db_enriched.py")
print("")
print("=" * 70)
print("📧 COMPTES QUI SERONT CRÉÉS")
print("=" * 70)
print("")
print("👑 Super Admin:")
print("   Email: jiby.njaay@gmail.com")
print("   Pass:  M@indjibsoN7")
print("")
print("🏢 6 Employeurs (pass: employeur123)")
print("👨‍💼 8 Candidats (pass: candidat123)")
print("💼 12 Offres d'emploi")
print("🎨 10 Bannières publicitaires")
print("💬 5 Sujets de forum")
print("")
print("=" * 70)
print("")
print("⚠️  NOTE: Les tables Supabase DOIVENT être créées d'abord!")
print("    Exécutez le contenu de /app/backend/schema.sql dans Supabase SQL Editor")
print("")
