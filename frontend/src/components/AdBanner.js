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
      const response = await api.get('/banners');
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
    <div className="w-full bg-gradient-to-r from-cyan-900/20 via-blue-900/20 to-violet-900/20 border-y border-cyan-500/20 overflow-hidden" data-testid="ad-banner">
      <div className="container mx-auto px-4 py-4">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          {/* Image */}
          <div className="flex-shrink-0">
            <img
              src={currentBanner.image}
              alt={currentBanner.titre}
              className="w-full md:w-40 h-24 object-cover rounded-lg border border-cyan-500/30 shadow-lg"
              data-testid="banner-image"
            />
          </div>

          {/* Content */}
          <div className="flex-1 text-center md:text-left">
            <h3 className="text-xl font-bold text-white mb-1" data-testid="banner-title">
              {currentBanner.titre}
            </h3>
            <p className="text-gray-300 text-sm" data-testid="banner-text">
              {currentBanner.texte}
            </p>
          </div>

          {/* Contact Info */}
          <div className="flex flex-col gap-2">
            <a
              href={`tel:${currentBanner.telephone}`}
              className="flex items-center gap-2 text-sm text-cyan-400 hover:text-cyan-300 transition-colors"
              data-testid="banner-phone"
            >
              <Phone className="h-4 w-4" />
              {currentBanner.telephone}
            </a>
            <a
              href={`mailto:${currentBanner.mail}`}
              className="flex items-center gap-2 text-sm text-cyan-400 hover:text-cyan-300 transition-colors"
              data-testid="banner-email"
            >
              <Mail className="h-4 w-4" />
              {currentBanner.mail}
            </a>
            <a
              href={currentBanner.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-sm font-medium text-violet-400 hover:text-violet-300 transition-colors"
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
