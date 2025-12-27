import React, { useState, useRef, useEffect } from 'react';
import { Input } from './ui/input';
import { VILLES_AFRIQUE } from '../lib/constants';
import { MapPin, X } from 'lucide-react';

const LocationAutocomplete = ({ value, onChange, className = '' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [filteredCities, setFilteredCities] = useState([]);
  const wrapperRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleInputChange = (e) => {
    const inputValue = e.target.value;
    onChange(inputValue);

    if (inputValue.length > 0) {
      const filtered = VILLES_AFRIQUE.filter((city) =>
        city.toLowerCase().includes(inputValue.toLowerCase())
      );
      setFilteredCities(filtered.slice(0, 8)); // Limiter à 8 résultats
      setIsOpen(true);
    } else {
      setFilteredCities([]);
      setIsOpen(false);
    }
  };

  const handleSelectCity = (city) => {
    onChange(city);
    setIsOpen(false);
  };

  const handleClear = () => {
    onChange('');
    setFilteredCities([]);
    setIsOpen(false);
  };

  return (
    <div ref={wrapperRef} className="relative">
      <div className="relative">
        <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500" />
        <Input
          type="text"
          placeholder="Ville ou pays..."
          value={value}
          onChange={handleInputChange}
          onFocus={() => value && setIsOpen(true)}
          className={`pl-10 pr-10 ${className}`}
          data-testid="location-autocomplete"
        />
        {value && (
          <button
            onClick={handleClear}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white"
            data-testid="clear-location"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>

      {isOpen && filteredCities.length > 0 && (
        <div className="absolute z-50 w-full mt-1 bg-gray-900 border border-cyan-500/30 rounded-lg shadow-xl max-h-64 overflow-y-auto">
          {filteredCities.map((city, index) => (
            <button
              key={index}
              onClick={() => handleSelectCity(city)}
              className="w-full px-4 py-3 text-left text-gray-300 hover:bg-cyan-500/10 hover:text-white transition-colors flex items-center gap-2"
              data-testid={`city-option-${index}`}
            >
              <MapPin className="h-4 w-4 text-cyan-400" />
              {city}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default LocationAutocomplete;
