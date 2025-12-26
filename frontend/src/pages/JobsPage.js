import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Briefcase, MapPin, Clock, Search } from 'lucide-react';
import api from '../lib/api';
import AdBanner from '../components/AdBanner';

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
      <AdBanner />
      
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-violet-600 bg-clip-text text-transparent mb-8" data-testid="jobs-page-title">
          Offres d'emploi
        </h1>

        <div className="grid md:grid-cols-3 gap-4 mb-8">
          <Input
            placeholder="Rechercher un poste..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="bg-gray-900 border-cyan-500/30 text-white"
            data-testid="search-input"
          />
          <Input
            placeholder="Localisation..."
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="bg-gray-900 border-cyan-500/30 text-white"
            data-testid="location-input"
          />
          <Select value={contractType} onValueChange={setContractType}>
            <SelectTrigger className="bg-gray-900 border-cyan-500/30 text-white">
              <SelectValue placeholder="Type de contrat" />
            </SelectTrigger>
            <SelectContent className="bg-gray-900 border-cyan-500/30">
              <SelectItem value=" ">Tous</SelectItem>
              <SelectItem value="CDI">CDI</SelectItem>
              <SelectItem value="CDD">CDD</SelectItem>
              <SelectItem value="Stage">Stage</SelectItem>
              <SelectItem value="Alternance">Alternance</SelectItem>
              <SelectItem value="Freelance">Freelance</SelectItem>
            </SelectContent>
          </Select>
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
