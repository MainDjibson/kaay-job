import React, { useState, useEffect } from 'react';
import { Phone, Mail, ExternalLink } from 'lucide-react';
import api from '../lib/api';

const AdBanner = () => {
  const [banners, setBanners] = useState([]);
  const [currentBanner, setCurrentBanner] = useState(null);
  const [previousIndex, setPreviousIndex] = useState(-1);

  useEffect(() => {
    loadBanners();
  }, []);

  useEffect(() => {
    if (banners.length > 0) {
      selectRandomBanner();
      const interval = setInterval(() => {
        selectRandomBanner();
      }, 15000); // Change every 15 seconds

      return () => clearInterval(interval);
    }
  }, [banners]);

  const loadBanners = async () => {
    try {
      const response = await api.get('/banners/active');
      setBanners(response.data);
    } catch (error) {
      console.error('Failed to load banners:', error);
    }
  };

  const selectRandomBanner = () => {
    if (banners.length === 0) return;

    let newIndex;
    if (banners.length === 1) {
      newIndex = 0;
    } else {
      // Avoid showing the same banner twice in a row
      do {
        newIndex = Math.floor(Math.random() * banners.length);
      } while (newIndex === previousIndex && banners.length > 1);
    }

    setPreviousIndex(newIndex);
    setCurrentBanner(banners[newIndex]);
  };

  if (!currentBanner) return null;

  return (
    <div className="w-full bg-gradient-to-r from-cyan-900/30 via-blue-900/30 to-violet-900/30 border-y border-cyan-500/20 overflow-hidden" data-testid="ad-banner">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          {/* Image */}
          <div className="flex-shrink-0">
            <img
              src={currentBanner.image}
              alt={currentBanner.titre}
              className="w-full md:w-48 h-32 object-cover rounded-xl border border-cyan-500/30 shadow-lg"
              data-testid="banner-image"
            />
          </div>

          {/* Content */}
          <div className="flex-1 text-center md:text-left">
            <h3 className="text-2xl font-bold text-white mb-2" data-testid="banner-title">
              {currentBanner.titre}
            </h3>
            <p className="text-gray-300 text-base leading-relaxed" data-testid="banner-text">
              {currentBanner.texte}
            </p>
          </div>

          {/* Contact Info */}
          <div className="flex flex-col gap-3 min-w-[250px]">
            <a
              href={`tel:${currentBanner.telephone}`}
              className="flex items-center gap-2 text-sm text-cyan-400 hover:text-cyan-300 transition-colors px-3 py-2 bg-cyan-900/20 rounded-lg border border-cyan-500/30"
              data-testid="banner-phone"
            >
              <Phone className="h-4 w-4" />
              {currentBanner.telephone}
            </a>
            <a
              href={`mailto:${currentBanner.mail}`}
              className="flex items-center gap-2 text-sm text-cyan-400 hover:text-cyan-300 transition-colors px-3 py-2 bg-cyan-900/20 rounded-lg border border-cyan-500/30"
              data-testid="banner-email"
            >
              <Mail className="h-4 w-4" />
              {currentBanner.mail}
            </a>
            <a
              href={currentBanner.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2 text-sm font-medium text-white bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-600 hover:to-violet-700 transition-colors px-4 py-2 rounded-lg shadow-lg"
              data-testid="banner-url"
            >
              <ExternalLink className="h-4 w-4" />
              Visiter le site
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdBanner;
