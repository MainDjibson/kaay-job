import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/button';
import { Textarea } from '../components/ui/textarea';
import { Label } from '../components/ui/label';
import { toast } from 'sonner';
import { Briefcase, MapPin, Calendar, DollarSign, GraduationCap } from 'lucide-react';
import api from '../lib/api';

const JobDetailPage = () => {
  const { jobId } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadJob();
  }, [jobId]);

  const loadJob = async () => {
    try {
      const response = await api.get(`/jobs/${jobId}`);
      setJob(response.data);
    } catch (error) {
      console.error('Failed to load job:', error);
      toast.error('Offre non trouvée');
      navigate('/jobs');
    } finally {
      setLoading(false);
    }
  };

  const handleApply = async (e) => {
    e.preventDefault();
    if (!user) {
      toast.error('Vous devez être connecté pour postuler');
      navigate('/login');
      return;
    }
    if (user.role !== 'job_seeker') {
      toast.error('Seuls les chercheurs d'emploi peuvent postuler');
      return;
    }

    setApplying(true);
    try {
      await api.post('/applications', {
        job_offer_id: jobId,
        message,
      });
      toast.success('Candidature envoyée avec succès !');
      setMessage('');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erreur lors de la candidature');
    } finally {
      setApplying(false);
    }
  };

  if (loading) return <div className="min-h-screen bg-black flex items-center justify-center"><div className="text-white">Chargement...</div></div>;
  if (!job) return null;

  return (
    <div className="min-h-screen bg-black py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <div className="bg-gradient-to-br from-gray-900 to-gray-950 border border-cyan-500/20 rounded-2xl p-8 mb-8">
          <h1 className="text-4xl font-bold text-white mb-4" data-testid="job-title">{job.title}</h1>
          
          <div className="grid md:grid-cols-2 gap-4 mb-6">
            <div className="flex items-center gap-2 text-gray-300">
              <MapPin className="h-5 w-5 text-cyan-400" />
              <span>{job.location}</span>
            </div>
            <div className="flex items-center gap-2 text-gray-300">
              <Briefcase className="h-5 w-5 text-cyan-400" />
              <span>{job.contract_type}</span>
            </div>
            {job.salary && (
              <div className="flex items-center gap-2 text-gray-300">
                <DollarSign className="h-5 w-5 text-cyan-400" />
                <span>{job.salary}</span>
              </div>
            )}
            {job.education_required && (
              <div className="flex items-center gap-2 text-gray-300">
                <GraduationCap className="h-5 w-5 text-cyan-400" />
                <span>{job.education_required}</span>
              </div>
            )}
          </div>

          <div className="border-t border-cyan-500/20 pt-6 mb-6">
            <h2 className="text-2xl font-bold text-white mb-3">Description</h2>
            <p className="text-gray-300 leading-relaxed whitespace-pre-line">{job.description}</p>
          </div>

          {job.skills && (
            <div className="border-t border-cyan-500/20 pt-6">
              <h2 className="text-2xl font-bold text-white mb-3">Compétences requises</h2>
              <p className="text-gray-300">{job.skills}</p>
            </div>
          )}
        </div>

        {user && user.role === 'job_seeker' && (
          <div className="bg-gradient-to-br from-gray-900 to-gray-950 border border-cyan-500/20 rounded-2xl p-8">
            <h2 className="text-2xl font-bold text-white mb-6">Postuler à cette offre</h2>
            <form onSubmit={handleApply} className="space-y-6" data-testid="application-form">
              <div>
                <Label className="text-gray-300 mb-2 block">Message de motivation (optionnel)</Label>
                <Textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Expliquez pourquoi vous êtes le candidat idéal..."
                  className="bg-black/50 border-cyan-500/30 text-white"
                  rows={6}
                  data-testid="motivation-textarea"
                />
              </div>
              <Button
                type="submit"
                disabled={applying}
                className="w-full bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-600 hover:to-violet-700 text-white font-medium py-6"
                data-testid="apply-button"
              >
                {applying ? 'Envoi en cours...' : 'Postuler maintenant'}
              </Button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default JobDetailPage;
