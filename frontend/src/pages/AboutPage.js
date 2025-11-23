import React from 'react';
import { Mail, Phone, ExternalLink } from 'lucide-react';

const AboutPage = () => {
  return (
    <div className="min-h-screen bg-black py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        {/* À propos de kaay-job */}
        <section className="mb-12 bg-gradient-to-br from-gray-900 to-gray-950 border border-cyan-500/20 rounded-2xl p-8" data-testid="about-platform-section">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-violet-600 bg-clip-text text-transparent mb-6">
            À propos de kaay-job
          </h1>
          <p className="text-gray-300 text-lg leading-relaxed mb-4">
            <strong className="text-white">kaay-job</strong> est la plateforme de référence qui met en relation les chercheurs d'emploi et les employeurs en Afrique. Notre mission est de faciliter la rencontre entre les talents et les opportunités professionnelles.
          </p>
          <p className="text-gray-300 text-lg leading-relaxed mb-4">
            Nous croyons que chaque personne mérite d'avoir accès aux meilleures opportunités de carrière, et que chaque entreprise devrait pouvoir trouver les talents dont elle a besoin pour se développer.
          </p>
          <h3 className="text-2xl font-bold text-white mt-8 mb-4">Notre Vision</h3>
          <p className="text-gray-300 text-lg leading-relaxed">
            Devenir la plateforme numéro un pour l'emploi en Afrique, en connectant des millions de professionnels avec des opportunités qui transforment leur vie et contribuent au développement économique du continent.
          </p>
        </section>

        {/* À propos du développeur */}
        <section className="mb-12 bg-gradient-to-br from-gray-900 to-gray-950 border border-cyan-500/20 rounded-2xl p-8" data-testid="about-developer-section">
          <h2 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-violet-600 bg-clip-text text-transparent mb-6">
            À propos du développeur
          </h2>
          <div className="space-y-4">
            <p className="text-gray-300 text-lg leading-relaxed">
              <strong className="text-white">Nom :</strong> Équipe de développement kaay-job
            </p>
            <p className="text-gray-300 text-lg leading-relaxed">
              Cette plateforme a été conçue et développée avec passion pour répondre aux besoins du marché de l'emploi africain. Notre équipe travaille continuellement pour améliorer l'expérience utilisateur et ajouter de nouvelles fonctionnalités.
            </p>
            <div className="mt-6 p-4 bg-cyan-900/20 border border-cyan-500/30 rounded-lg">
              <p className="text-gray-300 flex items-center gap-2">
                <Mail className="h-5 w-5 text-cyan-400" />
                <span className="font-medium">Email de contact :</span>
                <a href="mailto:contact@kaay-job.sn" className="text-cyan-400 hover:text-cyan-300">
                  contact@kaay-job.sn
                </a>
              </p>
            </div>
          </div>
        </section>

        {/* Publicité / Annonces */}
        <section className="bg-gradient-to-br from-violet-900/20 to-purple-900/20 border border-violet-500/20 rounded-2xl p-8" data-testid="advertising-section">
          <h2 className="text-3xl font-bold bg-gradient-to-r from-violet-400 to-purple-600 bg-clip-text text-transparent mb-6">
            Publicité sur kaay-job
          </h2>
          <p className="text-gray-300 text-lg leading-relaxed mb-6">
            Vous souhaitez promouvoir votre entreprise, vos produits ou services sur kaay-job ? Nous proposons des espaces publicitaires visibles par des milliers de visiteurs chaque jour.
          </p>
          
          <div className="bg-black/30 border border-violet-500/30 rounded-lg p-6 mb-6">
            <h3 className="text-xl font-bold text-white mb-4">Informations requises pour votre publicité :</h3>
            <ul className="space-y-2 text-gray-300">
              <li className="flex items-start gap-2">
                <span className="text-violet-400">•</span>
                <span><strong>Titre :</strong> Le titre de votre annonce</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-violet-400">•</span>
                <span><strong>Texte :</strong> Description courte de votre offre</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-violet-400">•</span>
                <span><strong>Image :</strong> Une image attractive (format recommandé : 800x400px)</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-violet-400">•</span>
                <span><strong>Téléphone :</strong> Votre numéro de contact</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-violet-400">•</span>
                <span><strong>Email :</strong> Votre adresse email</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-violet-400">•</span>
                <span><strong>URL :</strong> Le lien vers votre site web ou boutique</span>
              </li>
            </ul>
          </div>

          <div className="bg-violet-900/20 border border-violet-500/30 rounded-lg p-6">
            <h3 className="text-xl font-bold text-white mb-4">Contactez-nous :</h3>
            <div className="space-y-3">
              <p className="text-gray-300 flex items-center gap-2">
                <Mail className="h-5 w-5 text-violet-400" />
                <span className="font-medium">Email :</span>
                <a href="mailto:pub@kaay-job.sn" className="text-violet-400 hover:text-violet-300">
                  pub@kaay-job.sn
                </a>
              </p>
              <p className="text-gray-300 flex items-center gap-2">
                <Phone className="h-5 w-5 text-violet-400" />
                <span className="font-medium">Téléphone :</span>
                <a href="tel:+221770000000" className="text-violet-400 hover:text-violet-300">
                  +221 77 000 00 00
                </a>
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default AboutPage;
