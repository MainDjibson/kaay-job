# 🚀 Guide de démarrage rapide kaay-job

## ✅ Ce qui fonctionne déjà

L'application est **prête et fonctionne** ! Vous pouvez voir :
- ✅ Interface complète avec design futuriste
- ✅ Navigation fonctionnelle
- ✅ Backend API opérationnel
- ✅ Toutes les pages créées

## ⚠️ Étape finale : Créer les tables Supabase

Pour activer toutes les fonctionnalités (authentification, offres d'emploi, etc.), vous devez créer les tables dans Supabase :

### 📋 Étapes simples :

1. **Ouvrez votre dashboard Supabase** :
   - URL : https://supabase.com/dashboard/project/zlgxkhgvkslyksfjjqod
   - Ou allez sur https://supabase.com et connectez-vous

2. **Accédez à l'éditeur SQL** :
   - Cliquez sur "SQL Editor" dans le menu latéral gauche

3. **Copiez le schéma SQL** :
   - Ouvrez le fichier `/app/backend/schema.sql`
   - Copiez tout le contenu

4. **Exécutez le SQL** :
   - Collez le contenu dans l'éditeur SQL Supabase
   - Cliquez sur "Run" (ou appuyez sur Ctrl+Enter)
   - Attendez que "Success!" apparaisse

5. **Créez les buckets de stockage** :
   - Allez dans "Storage" dans le menu latéral
   - Créez un nouveau bucket nommé `cvs` (cochez "Public")
   - Créez un autre bucket nommé `avatars` (cochez "Public")

6. **Initialisez les données de test** :
   ```bash
   cd /app/backend
   python3 init_db.py
   ```

## 🎉 C'est tout !

Votre application kaay-job est maintenant 100% fonctionnelle avec :

- 3 comptes de test créés
- 5 bannières publicitaires
- 5 catégories de forum
- 2 offres d'emploi d'exemple

## 👤 Comptes de test

Connectez-vous avec :

**Admin** (gestion complète)
- Email: `admin@kaay-job.sn`
- Mot de passe: `admin123`

**Employeur** (publier des offres)
- Email: `recruteur@tech-dakar.sn`
- Mot de passe: `recruteur123`

**Candidat** (postuler aux offres)
- Email: `candidat@example.sn`
- Mot de passe: `candidat123`

## 🔗 Liens utiles

- **Application** : https://recruit-link-2.preview.emergentagent.com
- **API Backend** : https://recruit-link-2.preview.emergentagent.com/api
- **Documentation complète** : Voir `/app/README.md`

## ❓ Besoin d'aide ?

Si vous rencontrez un problème :
1. Vérifiez que les tables sont créées dans Supabase
2. Vérifiez que les buckets de stockage existent
3. Consultez les logs : `tail -f /var/log/supervisor/backend.err.log`

---

**🎨 Design** : Interface futuriste avec gradients cyan/bleu/violet
**🔧 Stack** : React + FastAPI + Supabase PostgreSQL
**✨ Fonctionnalités** : Profils, CV, Offres, Candidatures, Messages, Forum, Bannières pub
