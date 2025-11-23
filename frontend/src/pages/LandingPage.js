import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Briefcase, Users, MessageSquare, TrendingUp, Search, Building2 } from 'lucide-react';
import AdBanner from '../components/AdBanner';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-black">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 via-blue-900/5 to-violet-500/10"></div>
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiMwNjBhMGYiIGZpbGwtb3BhY2l0eT0iMC40Ij48cGF0aCBkPSJNMzYgMzRjMC0yLjIxIDEuNzktNCA0LTRzNCAxLjc5IDQgNC0xLjc5IDQtNCA0LTQtMS43OS00LTR6bTAgMTBjMC0yLjIxIDEuNzktNCA0LTRzNCAxLjc5IDQgNC0xLjc5IDQtNCA0LTQtMS43OS00LTR6Ii8+PC9nPjwvZz48L3N2Zz4=')] opacity-30"></div>
        
        <div className="container relative mx-auto px-4 pt-20 pb-32">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-600 bg-clip-text text-transparent leading-tight" data-testid="landing-hero-title">
              Trouvez votre prochain défi professionnel
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-12 leading-relaxed" data-testid="landing-hero-subtitle">
              La plateforme qui connecte les talents avec les opportunités en Afrique
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/jobs" data-testid="landing-browse-jobs-button">
                <Button size="lg" className="bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-600 hover:to-violet-700 text-white font-medium px-8 py-6 text-lg shadow-xl shadow-cyan-500/20">
                  <Search className="mr-2 h-5 w-5" />
                  Explorer les offres
                </Button>
              </Link>
              <Link to="/register" data-testid="landing-register-button">
                <Button size="lg" variant="outline" className="border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10 font-medium px-8 py-6 text-lg">
                  Créer un compte
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Ad Banner */}
      <AdBanner />

      {/* Features Section */}
      <section className="py-24 bg-gradient-to-b from-black via-gray-950 to-black">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16 bg-gradient-to-r from-cyan-400 to-violet-600 bg-clip-text text-transparent">
            Pourquoi choisir kaay-job ?
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <div className="group p-8 rounded-2xl bg-gradient-to-br from-cyan-900/20 to-blue-900/20 border border-cyan-500/20 hover:border-cyan-500/40 transition-all duration-300 hover:transform hover:scale-105" data-testid="feature-card-jobs">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center mb-6 group-hover:shadow-lg group-hover:shadow-cyan-500/50 transition-shadow">
                <Briefcase className="h-7 w-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">Offres variées</h3>
              <p className="text-gray-400 leading-relaxed">
                Accédez à des milliers d'offres d'emploi dans tous les secteurs et niveaux d'expérience
              </p>
            </div>

            <div className="group p-8 rounded-2xl bg-gradient-to-br from-violet-900/20 to-purple-900/20 border border-violet-500/20 hover:border-violet-500/40 transition-all duration-300 hover:transform hover:scale-105" data-testid="feature-card-network">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-violet-400 to-purple-600 flex items-center justify-center mb-6 group-hover:shadow-lg group-hover:shadow-violet-500/50 transition-shadow">
                <Users className="h-7 w-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">Réseau professionnel</h3>
              <p className="text-gray-400 leading-relaxed">
                Connectez-vous avec des professionnels et développez votre réseau
              </p>
            </div>

            <div className="group p-8 rounded-2xl bg-gradient-to-br from-blue-900/20 to-cyan-900/20 border border-blue-500/20 hover:border-blue-500/40 transition-all duration-300 hover:transform hover:scale-105" data-testid="feature-card-messaging">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-400 to-cyan-600 flex items-center justify-center mb-6 group-hover:shadow-lg group-hover:shadow-blue-500/50 transition-shadow">
                <MessageSquare className="h-7 w-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">Communication directe</h3>
              <p className="text-gray-400 leading-relaxed">
                Échangez directement avec les recruteurs et les candidats
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-gradient-to-r from-cyan-900/10 via-blue-900/10 to-violet-900/10 border-y border-cyan-500/20">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto text-center">
            <div>
              <div className="text-5xl font-bold bg-gradient-to-r from-cyan-400 to-blue-600 bg-clip-text text-transparent mb-2">
                500+
              </div>
              <div className="text-gray-400 font-medium">Offres d'emploi</div>
            </div>
            <div>
              <div className="text-5xl font-bold bg-gradient-to-r from-violet-400 to-purple-600 bg-clip-text text-transparent mb-2">
                1000+
              </div>
              <div className="text-gray-400 font-medium">Candidats</div>
            </div>
            <div>
              <div className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-cyan-600 bg-clip-text text-transparent mb-2">
                200+
              </div>
              <div className="text-gray-400 font-medium">Entreprises</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center bg-gradient-to-br from-cyan-900/20 via-blue-900/20 to-violet-900/20 border border-cyan-500/20 rounded-3xl p-12">
            <h2 className="text-4xl font-bold text-white mb-6">
              Prêt à commencer votre parcours ?
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Rejoignez des milliers de professionnels qui ont trouvé leur opportunité sur kaay-job
            </p>
            <Link to="/register">
              <Button size="lg" className="bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-600 hover:to-violet-700 text-white font-medium px-10 py-6 text-lg shadow-xl shadow-cyan-500/20">
                S'inscrire gratuitement
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
