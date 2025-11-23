import React from 'react';
import { Link } from 'react-router-dom';
import { Briefcase } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="border-t border-cyan-500/20 bg-black/80 backdrop-blur-sm mt-auto">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-400 via-blue-500 to-violet-600 flex items-center justify-center">
                <Briefcase className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-600 bg-clip-text text-transparent">
                kaay-job
              </span>
            </div>
            <p className="text-gray-400 text-sm">
              La plateforme qui connecte les talents avec les opportunités en Afrique.
            </p>
          </div>

          <div>
            <h4 className="text-white font-semibold mb-4">Navigation</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>
                <Link to="/jobs" className="hover:text-cyan-400 transition-colors">
                  Offres d'emploi
                </Link>
              </li>
              <li>
                <Link to="/forum" className="hover:text-cyan-400 transition-colors">
                  Forum
                </Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-cyan-400 transition-colors">
                  À propos
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-white font-semibold mb-4">Contact</h4>
            <p className="text-gray-400 text-sm">
              Pour toute question ou publicité, consultez notre page À propos.
            </p>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-cyan-500/20 text-center text-gray-500 text-sm">
          <p>© 2025 kaay-job. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
