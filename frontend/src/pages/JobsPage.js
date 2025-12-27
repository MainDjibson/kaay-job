import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import LocationAutocomplete from '../components/LocationAutocomplete';
import { Briefcase, MapPin, Clock, Search } from 'lucide-react';
import api from '../lib/api';
import { TYPES_CONTRAT } from '../lib/constants';

const JobsPage = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [location, setLocation] = useState('');
  const [contractType, setContractType] = useState('');

  useEffect(() => {
    loadJobs();
  }, [search, location, contractType]);

  const loadJobs = async () => {
    try {
      const params = {};
      if (search) params.search = search;
      if (location) params.location = location;
      if (contractType) params.contract_type = contractType;
      
      const response = await api.get('/jobs', { params });
      setJobs(response.data);
    } catch (error) {
      console.error('Failed to load jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black">
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-violet-600 bg-clip-text text-transparent mb-8" data-testid="jobs-page-title">
          Offres d'emploi
        </h1>

        <div className="grid md:grid-cols-3 gap-4 mb-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500" />
            <Input
              placeholder="Rechercher un poste..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-11 bg-gray-900 border-cyan-500/30 text-white placeholder:text-gray-500"
              data-testid="search-input"
            />
          </div>
          
          <LocationAutocomplete
            value={location}
            onChange={setLocation}
            className="bg-gray-900 border-cyan-500/30 text-white placeholder:text-gray-500"
          />

          <div className="flex gap-2 flex-wrap">
            <button
              onClick={() => setContractType('')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                contractType === ''
                  ? 'bg-white text-black'
                  : 'bg-gray-900 text-white border border-cyan-500/30 hover:bg-white hover:text-black'
              }`}
            >
              Tous
            </button>
            {TYPES_CONTRAT.map((type) => (
              <button
                key={type.value}
                onClick={() => setContractType(type.value)}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  contractType === type.value
                    ? 'bg-white text-black'
                    : 'bg-gray-900 text-white border border-cyan-500/30 hover:bg-white hover:text-black'
                }`}
                data-testid={`contract-type-${type.value}`}
              >
                {type.label}
              </button>
            ))}
          </div>
        </div>

        <div className="grid gap-6">
          {loading ? (
            <div className="text-white text-center">Chargement...</div>
          ) : jobs.length === 0 ? (
            <div className="text-gray-400 text-center">Aucune offre trouvée</div>
          ) : (
            jobs.map((job) => (
              <Link
                key={job.id}
                to={`/jobs/${job.id}`}
                className="block p-6 bg-gradient-to-br from-gray-900 to-gray-950 border border-cyan-500/20 rounded-xl hover:border-cyan-500/40 transition-colors"
                data-testid={`job-card-${job.id}`}
              >
                <h3 className="text-xl font-bold text-white mb-2">{job.title}</h3>
                <div className="flex flex-wrap gap-4 text-sm text-gray-400 mb-3">
                  <span className="flex items-center gap-1">
                    <MapPin className="h-4 w-4" />
                    {job.location}
                  </span>
                  <span className="flex items-center gap-1">
                    <Briefcase className="h-4 w-4" />
                    {job.contract_type}
                  </span>
                  {job.salary && <span>{job.salary}</span>}
                </div>
                <p className="text-gray-300 line-clamp-2">{job.description}</p>
              </Link>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default JobsPage;
