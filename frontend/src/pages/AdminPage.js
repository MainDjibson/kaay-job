import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { toast } from 'sonner';
import { Users, Briefcase, MessageSquare, Plus, Trash2 } from 'lucide-react';
import api from '../lib/api';

const AdminPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [banners, setBanners] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState({
    titre: '',
    texte: '',
    image: '',
    telephone: '',
    mail: '',
    url: '',
  });

  useEffect(() => {
    if (user?.role !== 'admin') {
      navigate('/');
      return;
    }
    loadStats();
    loadBanners();
  }, [user]);

  const loadStats = async () => {
    try {
      const response = await api.get('/admin/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  const loadBanners = async () => {
    try {
      const response = await api.get('/banners');
      setBanners(response.data);
    } catch (error) {
      console.error('Failed to load banners:', error);
    }
  };

  const handleCreateBanner = async (e) => {
    e.preventDefault();
    try {
      await api.post('/banners', formData);
      toast.success('Bannière créée avec succès !');
      setIsOpen(false);
      setFormData({ titre: '', texte: '', image: '', telephone: '', mail: '', url: '' });
      loadBanners();
    } catch (error) {
      toast.error('Erreur lors de la création');
    }
  };

  const handleDeleteBanner = async (id) => {
    if (!window.confirm('Supprimer cette bannière ?')) return;
    try {
      await api.delete(`/banners/${id}`);
      toast.success('Bannière supprimée');
      loadBanners();
    } catch (error) {
      toast.error('Erreur lors de la suppression');
    }
  };

  return (
    <div className="min-h-screen bg-black py-12 px-4">
      <div className="container mx-auto max-w-6xl">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-violet-600 bg-clip-text text-transparent mb-8">
          Administration
        </h1>

        {stats && (
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="bg-gradient-to-br from-cyan-900/20 to-blue-900/20 border border-cyan-500/20 rounded-2xl p-6">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center">
                  <Users className="h-7 w-7 text-white" />
                </div>
                <div>
                  <div className="text-3xl font-bold text-white">{stats.total_users}</div>
                  <div className="text-gray-400">Utilisateurs</div>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-violet-900/20 to-purple-900/20 border border-violet-500/20 rounded-2xl p-6">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-violet-400 to-purple-600 flex items-center justify-center">
                  <Briefcase className="h-7 w-7 text-white" />
                </div>
                <div>
                  <div className="text-3xl font-bold text-white">{stats.total_jobs}</div>
                  <div className="text-gray-400">Offres d'emploi</div>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-blue-900/20 to-cyan-900/20 border border-blue-500/20 rounded-2xl p-6">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-400 to-cyan-600 flex items-center justify-center">
                  <MessageSquare className="h-7 w-7 text-white" />
                </div>
                <div>
                  <div className="text-3xl font-bold text-white">{stats.total_applications}</div>
                  <div className="text-gray-400">Candidatures</div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="bg-gradient-to-br from-gray-900 to-gray-950 border border-cyan-500/20 rounded-2xl p-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-white">Bannières publicitaires</h2>
            <Dialog open={isOpen} onOpenChange={setIsOpen}>
              <DialogTrigger asChild>
                <Button className="bg-gradient-to-r from-cyan-500 to-violet-600">
                  <Plus className="h-4 w-4 mr-2" />
                  Nouvelle bannière
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-gray-900 border-cyan-500/20 max-w-2xl">
                <DialogHeader>
                  <DialogTitle className="text-white">Créer une bannière publicitaire</DialogTitle>
                </DialogHeader>
                <form onSubmit={handleCreateBanner} className="space-y-4">
                  <div>
                    <Label className="text-gray-300">Titre</Label>
                    <Input
                      value={formData.titre}
                      onChange={(e) => setFormData({ ...formData, titre: e.target.value })}
                      className="bg-black/50 border-cyan-500/30 text-white"
                      required
                    />
                  </div>
                  <div>
                    <Label className="text-gray-300">Texte</Label>
                    <Textarea
                      value={formData.texte}
                      onChange={(e) => setFormData({ ...formData, texte: e.target.value })}
                      className="bg-black/50 border-cyan-500/30 text-white"
                      required
                    />
                  </div>
                  <div>
                    <Label className="text-gray-300">URL de l'image</Label>
                    <Input
                      value={formData.image}
                      onChange={(e) => setFormData({ ...formData, image: e.target.value })}
                      className="bg-black/50 border-cyan-500/30 text-white"
                      required
                    />
                  </div>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <Label className="text-gray-300">Téléphone</Label>
                      <Input
                        value={formData.telephone}
                        onChange={(e) => setFormData({ ...formData, telephone: e.target.value })}
                        className="bg-black/50 border-cyan-500/30 text-white"
                        required
                      />
                    </div>
                    <div>
                      <Label className="text-gray-300">Email</Label>
                      <Input
                        value={formData.mail}
                        onChange={(e) => setFormData({ ...formData, mail: e.target.value })}
                        className="bg-black/50 border-cyan-500/30 text-white"
                        type="email"
                        required
                      />
                    </div>
                  </div>
                  <div>
                    <Label className="text-gray-300">URL du site</Label>
                    <Input
                      value={formData.url}
                      onChange={(e) => setFormData({ ...formData, url: e.target.value })}
                      className="bg-black/50 border-cyan-500/30 text-white"
                      required
                    />
                  </div>
                  <Button type="submit" className="w-full bg-gradient-to-r from-cyan-500 to-violet-600">
                    Créer la bannière
                  </Button>
                </form>
              </DialogContent>
            </Dialog>
          </div>

          <div className="space-y-4">
            {banners.map((banner) => (
              <div key={banner.id} className="p-4 bg-black/30 border border-cyan-500/20 rounded-lg flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-white mb-1">{banner.titre}</h3>
                  <p className="text-sm text-gray-400">{banner.texte}</p>
                </div>
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={() => handleDeleteBanner(banner.id)}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminPage;
