#!/usr/bin/env python3
"""Script pour créer 10 bannières publicitaires de test"""

# Liste de 10 bannières publicitaires de test variées
TEST_BANNERS = [
    {
        "titre": "Formation Développeur Web - Bootcamp 2025",
        "texte": "Devenez développeur web en 6 mois. Programme intensif avec stages garantis.",
        "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&h=400&fit=crop",
        "telephone": "+221770001111",
        "mail": "contact@bootcampdev.sn",
        "url": "https://bootcampdev.sn",
        "is_active": True
    },
    {
        "titre": "Boutique Kaay-Tech - Matériel Informatique",
        "texte": "Ordinateurs, smartphones, accessoires tech à prix imbattables. Livraison gratuite.",
        "image": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=800&h=400&fit=crop",
        "telephone": "+221770002222",
        "mail": "support@kaaytech.sn",
        "url": "https://kaaytech.sn",
        "is_active": True
    },
    {
        "titre": "Cabinet RH Talents Plus - Recrutement PME",
        "texte": "Nous trouvons les meilleurs talents pour votre entreprise. Service personnalisé.",
        "image": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=800&h=400&fit=crop",
        "telephone": "+221770003333",
        "mail": "contact@talentsplus.sn",
        "url": "https://talentsplus.sn",
        "is_active": True
    },
    {
        "titre": "Coworking Dakar Center - Espace Pro",
        "texte": "Bureaux équipés, wifi haut débit, salles de réunion. À partir de 50k/mois.",
        "image": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&h=400&fit=crop",
        "telephone": "+221770004444",
        "mail": "info@coworkdakar.sn",
        "url": "https://coworkdakar.sn",
        "is_active": True
    },
    {
        "titre": "Kaay-Jang E-learning - Cours en Ligne",
        "texte": "Plus de 500 cours : développement, design, marketing, business. Certificats reconnus.",
        "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&h=400&fit=crop",
        "telephone": "+221770005555",
        "mail": "hello@kaayjang.sn",
        "url": "https://kaayjang.sn",
        "is_active": True
    },
    {
        "titre": "Agence Digital Marketing Boost",
        "texte": "Augmentez votre visibilité en ligne. SEO, Social Media, Publicité Facebook/Google.",
        "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop",
        "telephone": "+221770006666",
        "mail": "contact@digitalboost.sn",
        "url": "https://digitalboost.sn",
        "is_active": True
    },
    {
        "titre": "Restaurant Le Teranga - Cuisine Sénégalaise",
        "texte": "Découvrez les saveurs authentiques du Sénégal. Livraison & Traiteur disponibles.",
        "image": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=400&fit=crop",
        "telephone": "+221770007777",
        "mail": "info@leteranga.sn",
        "url": "https://leteranga.sn",
        "is_active": True
    },
    {
        "titre": "Auto-École Moderne Dakar",
        "texte": "Permis B en 30 jours. Formateurs expérimentés, véhicules neufs, taux de réussite 92%.",
        "image": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=800&h=400&fit=crop",
        "telephone": "+221770008888",
        "mail": "inscription@autoecolemoderne.sn",
        "url": "https://autoecolemoderne.sn",
        "is_active": True
    },
    {
        "titre": "Salle de Sport FitZone - Musculation & Fitness",
        "texte": "Équipements dernière génération, coach personnel, cours collectifs. Essai gratuit 7j.",
        "image": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800&h=400&fit=crop",
        "telephone": "+221770009999",
        "mail": "contact@fitzone.sn",
        "url": "https://fitzone.sn",
        "is_active": True
    },
    {
        "titre": "Agence Immobilière DakarHomes",
        "texte": "Vente, location, gestion immobilière. Plus de 1000 biens disponibles à Dakar.",
        "image": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800&h=400&fit=crop",
        "telephone": "+221770010000",
        "mail": "info@dakarhomes.sn",
        "url": "https://dakarhomes.sn",
        "is_active": True
    }
]

print("📋 Liste de 10 bannières publicitaires de test créée")
print("")
for i, banner in enumerate(TEST_BANNERS, 1):
    print(f"{i}. {banner['titre']}")
    print(f"   Tel: {banner['telephone']} | Email: {banner['mail']}")
    print(f"   Active: {banner['is_active']}")
    print("")
