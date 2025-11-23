import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/button';
import { Textarea } from '../components/ui/textarea';
import { Avatar, AvatarFallback } from '../components/ui/avatar';
import { toast } from 'sonner';
import { User, Calendar } from 'lucide-react';
import api from '../lib/api';

const ForumTopicPage = () => {
  const { topicId } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [topic, setTopic] = useState(null);
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState('');

  useEffect(() => {
    loadTopic();
    loadPosts();
  }, [topicId]);

  const loadTopic = async () => {
    try {
      const response = await api.get(`/forum/topics/${topicId}`);
      setTopic(response.data);
    } catch (error) {
      console.error('Failed to load topic:', error);
    }
  };

  const loadPosts = async () => {
    try {
      const response = await api.get(`/forum/posts/${topicId}`);
      setPosts(response.data);
    } catch (error) {
      console.error('Failed to load posts:', error);
    }
  };

  const handleCreatePost = async (e) => {
    e.preventDefault();
    if (!user) {
      toast.error('Vous devez être connecté pour répondre');
      navigate('/login');
      return;
    }

    try {
      await api.post('/forum/posts', {
        topic_id: topicId,
        content: newPost,
      });
      toast.success('Réponse publiée !');
      setNewPost('');
      loadPosts();
      loadTopic();
    } catch (error) {
      toast.error('Erreur lors de la publication');
    }
  };

  if (!topic) return <div className="min-h-screen bg-black flex items-center justify-center"><div className="text-white">Chargement...</div></div>;

  return (
    <div className="min-h-screen bg-black py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <div className="bg-gradient-to-br from-gray-900 to-gray-950 border border-cyan-500/20 rounded-2xl p-8 mb-8">
          <h1 className="text-3xl font-bold text-white mb-4">{topic.title}</h1>
          <p className="text-gray-300 leading-relaxed whitespace-pre-line">{topic.content}</p>
          <div className="mt-4 flex items-center gap-2 text-sm text-gray-400">
            <Calendar className="h-4 w-4" />
            {new Date(topic.created_at).toLocaleDateString()}
          </div>
        </div>

        <div className="space-y-6 mb-8">
          <h2 className="text-2xl font-bold text-white">Réponses ({posts.length})</h2>
          {posts.map((post) => (
            <div key={post.id} className="bg-gradient-to-br from-gray-900 to-gray-950 border border-cyan-500/20 rounded-xl p-6">
              <div className="flex items-start gap-4">
                <Avatar>
                  <AvatarFallback className="bg-gradient-to-br from-cyan-400 to-violet-600">?</AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <p className="text-gray-300 whitespace-pre-line mb-2">{post.content}</p>
                  <div className="text-sm text-gray-500">
                    {new Date(post.created_at).toLocaleDateString()}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {user && (
          <div className="bg-gradient-to-br from-gray-900 to-gray-950 border border-cyan-500/20 rounded-2xl p-8">
            <h3 className="text-xl font-bold text-white mb-4">Répondre</h3>
            <form onSubmit={handleCreatePost} className="space-y-4">
              <Textarea
                value={newPost}
                onChange={(e) => setNewPost(e.target.value)}
                placeholder="Votre réponse..."
                className="bg-black/50 border-cyan-500/30 text-white"
                rows={4}
                required
              />
              <Button
                type="submit"
                className="bg-gradient-to-r from-cyan-500 to-violet-600"
              >
                Publier
              </Button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default ForumTopicPage;
