import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Label } from '../components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { toast } from 'sonner';
import { MessageSquare, Plus, User, Calendar } from 'lucide-react';
import api from '../lib/api';

const ForumPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [categories, setCategories] = useState([]);
  const [topics, setTopics] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState({
    category_id: '',
    title: '',
    content: '',
  });

  useEffect(() => {
    loadCategories();
    loadTopics();
  }, [selectedCategory]);

  const loadCategories = async () => {
    try {
      const response = await api.get('/forum/categories');
      setCategories(response.data);
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const loadTopics = async () => {
    try {
      const params = selectedCategory ? { category_id: selectedCategory } : {};
      const response = await api.get('/forum/topics', { params });
      setTopics(response.data);
    } catch (error) {
      console.error('Failed to load topics:', error);
    }
  };

  const handleCreateTopic = async (e) => {
    e.preventDefault();
    if (!user) {
      toast.error('Vous devez être connecté pour créer un sujet');
      navigate('/login');
      return;
    }

    try {
      await api.post('/forum/topics', formData);
      toast.success('Sujet créé avec succès !');
      setIsOpen(false);
      setFormData({ category_id: '', title: '', content: '' });
      loadTopics();
    } catch (error) {
      toast.error('Erreur lors de la création du sujet');
    }
  };

  return (
    <div className="min-h-screen bg-black py-12 px-4">
      <div className="container mx-auto max-w-6xl">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-violet-600 bg-clip-text text-transparent">
            Forum
          </h1>
          {user && (
            <Dialog open={isOpen} onOpenChange={setIsOpen}>
              <DialogTrigger asChild>
                <Button className="bg-gradient-to-r from-cyan-500 to-violet-600">
                  <Plus className="h-4 w-4 mr-2" />
                  Nouveau sujet
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-gray-900 border-cyan-500/20">
                <DialogHeader>
                  <DialogTitle className="text-white">Créer un nouveau sujet</DialogTitle>
                </DialogHeader>
                <form onSubmit={handleCreateTopic} className="space-y-4">
                  <div>
                    <Label className="text-gray-300">Catégorie</Label>
                    <Select
                      value={formData.category_id}
                      onValueChange={(value) => setFormData({ ...formData, category_id: value })}
                    >
                      <SelectTrigger className="bg-black/50 border-cyan-500/30 text-white">
                        <SelectValue placeholder="Choisir une catégorie" />
                      </SelectTrigger>
                      <SelectContent className="bg-gray-900 border-cyan-500/30">
                        {categories.map((cat) => (
                          <SelectItem key={cat.id} value={cat.id}>
                            {cat.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label className="text-gray-300">Titre</Label>
                    <Input
                      value={formData.title}
                      onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                      className="bg-black/50 border-cyan-500/30 text-white"
                      required
                    />
                  </div>
                  <div>
                    <Label className="text-gray-300">Contenu</Label>
                    <Textarea
                      value={formData.content}
                      onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                      className="bg-black/50 border-cyan-500/30 text-white"
                      rows={6}
                      required
                    />
                  </div>
                  <Button type="submit" className="w-full bg-gradient-to-r from-cyan-500 to-violet-600">
                    Créer le sujet
                  </Button>
                </form>
              </DialogContent>
            </Dialog>
          )}
        </div>

        <div className="grid md:grid-cols-4 gap-6 mb-8">
          {categories.map((cat) => (
            <div
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id === selectedCategory ? '' : cat.id)}
              className={`p-4 rounded-xl cursor-pointer transition-all ${
                selectedCategory === cat.id
                  ? 'bg-cyan-900/30 border-cyan-500/50'
                  : 'bg-gray-900 border-gray-800 hover:bg-gray-800'
              } border`}
            >
              <h3 className="font-semibold text-white mb-1">{cat.name}</h3>
              <p className="text-sm text-gray-400">{cat.description}</p>
            </div>
          ))}
        </div>

        <div className="space-y-4">
          {topics.map((topic) => (
            <Link
              key={topic.id}
              to={`/forum/${topic.id}`}
              className="block p-6 bg-gradient-to-br from-gray-900 to-gray-950 border border-cyan-500/20 rounded-xl hover:border-cyan-500/40 transition-colors"
            >
              <h3 className="text-xl font-bold text-white mb-2">{topic.title}</h3>
              <div className="flex items-center gap-4 text-sm text-gray-400">
                <span className="flex items-center gap-1">
                  <MessageSquare className="h-4 w-4" />
                  {topic.posts_count} réponses
                </span>
                <span className="flex items-center gap-1">
                  <Calendar className="h-4 w-4" />
                  {new Date(topic.created_at).toLocaleDateString()}
                </span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ForumPage;
