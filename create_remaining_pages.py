#!/usr/bin/env python3
"""
Script pour créer toutes les pages React manquantes pour kaay-job
"""

import os

# Define base pages directory
PAGES_DIR = "/app/frontend/src/pages"

# ProfilePage.js
profile_page = '''import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar';
import { toast } from 'sonner';
import { User, Mail, MapPin, Briefcase, Upload, FileText, Building2, Globe } from 'lucide-react';
import api from '../lib/api';

const ProfilePage = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({});

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const response = await api.get('/profiles/me');
      setProfile(response.data);
      setFormData(response.data);
    } catch (error) {
      console.error('Failed to load profile:', error);
      toast.error('Erreur lors du chargement du profil');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const response = await api.put('/profiles/me', formData);
      setProfile(response.data);
      setEditing(false);
      toast.success('Profil mis à jour avec succès !');
    } catch (error) {
      toast.error('Erreur lors de la mise à jour');
    }
  };

  const handleCVUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/profiles/upload-cv', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      toast.success('CV uploadé avec succès !');
      loadProfile();
    } catch (error) {
      toast.error("Erreur lors de l'upload du CV");
    }
  };

  const handleAvatarUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      await api.post('/profiles/upload-avatar', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      toast.success('Avatar uploadé avec succès !');
      loadProfile();
    } catch (error) {
      toast.error("Erreur lors de l'upload de l'avatar");
    }
  };

  if (loading) {
    return <div className="min-h-screen bg-black flex items-center justify-center"><div className="text-white">Chargement...</div></div>;
  }

  return (
    <div className="min-h-screen bg-black py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <div className="bg-gradient-to-br from-gray-900 to-gray-950 border border-cyan-500/20 rounded-2xl p-8">
          <div className="flex items-start gap-6 mb-8">
            <div className="relative">
              <Avatar className="h-24 w-24 ring-4 ring-cyan-500/50">
                <AvatarImage src={profile?.avatar_url || ''} />
                <AvatarFallback className="bg-gradient-to-br from-cyan-400 to-violet-600 text-white text-2xl">
                  {(profile?.full_name || profile?.company_name || user?.email || '?')[0].toUpperCase()}
                </AvatarFallback>
              </Avatar>
              <label htmlFor="avatar-upload" className="absolute bottom-0 right-0 p-2 bg-cyan-500 rounded-full cursor-pointer hover:bg-cyan-600">
                <Upload className="h-4 w-4 text-white" />
              </label>
              <input
                id="avatar-upload"
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handleAvatarUpload}
              />
            </div>
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-white mb-2">
                {profile?.full_name || profile?.company_name || user?.email}
              </h1>
              <p className="text-gray-400">{user?.role === 'job_seeker' ? 'Chercheur d\'emploi' : 'Employeur'}</p>
            </div>
            <Button
              onClick={() => setEditing(!editing)}
              className="bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-600 hover:to-violet-700"
            >
              {editing ? 'Annuler' : 'Modifier'}
            </Button>
          </div>

          {editing ? (
            <form onSubmit={handleUpdate} className="space-y-6">
              {user?.role === 'job_seeker' ? (
                <>
                  <div className="space-y-2">
                    <Label className="text-gray-300">Nom complet</Label>
                    <Input
                      value={formData.full_name || ''}
                      onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                      className="bg-black/50 border-cyan-500/30 text-white"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-gray-300">Titre professionnel</Label>
                    <Input
                      value={formData.profile_title || ''}
                      onChange={(e) => setFormData({ ...formData, profile_title: e.target.value })}
                      className="bg-black/50 border-cyan-500/30 text-white"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-gray-300">Niveau d'études</Label>
                    <Input
                      value={formData.education_level || ''}
                      onChange={(e) => setFormData({ ...formData, education_level: e.target.value })}
                      className="bg-black/50 border-cyan-500/30 text-white"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-gray-300">Compétences</Label>
                    <Textarea
                      value={formData.skills || ''}
                      onChange={(e) => setFormData({ ...formData, skills: e.target.value })}
                      className="bg-black/50 border-cyan-500/30 text-white"
                      rows={3}
                    />
                  </div>
                </>
              ) : (
                <>
                  <div className="space-y-2">
                    <Label className="text-gray-300">Nom de l'entreprise</Label>
                    <Input
                      value={formData.company_name || ''}
                      onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
                      className="bg-black/50 border-cyan-500/30 text-white"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-gray-300">Secteur d'activité</Label>
                    <Input
                      value={formData.company_sector || ''}
                      onChange={(e) => setFormData({ ...formData, company_sector: e.target.value })}
                      className="bg-black/50 border-cyan-500/30 text-white"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-gray-300">Description</Label>
                    <Textarea
                      value={formData.company_description || ''}
                      onChange={(e) => setFormData({ ...formData, company_description: e.target.value })}
                      className="bg-black/50 border-cyan-500/30 text-white"
                      rows={3}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-gray-300">Site web</Label>
                    <Input
                      value={formData.company_website || ''}
                      onChange={(e) => setFormData({ ...formData, company_website: e.target.value })}
                      className="bg-black/50 border-cyan-500/30 text-white"
                    />
                  </div>
                </>
              )}
              <div className="space-y-2">
                <Label className="text-gray-300">Localisation</Label>
                <Input
                  value={formData.location || ''}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  className="bg-black/50 border-cyan-500/30 text-white"
                />
              </div>
              <div className="space-y-2">
                <Label className="text-gray-300">Téléphone</Label>
                <Input
                  value={formData.phone || ''}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="bg-black/50 border-cyan-500/30 text-white"
                />
              </div>
              <div className="space-y-2">
                <Label className="text-gray-300">Bio</Label>
                <Textarea
                  value={formData.bio || ''}
                  onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                  className="bg-black/50 border-cyan-500/30 text-white"
                  rows={4}
                />
              </div>
              <Button
                type="submit"
                className="w-full bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-600 hover:to-violet-700"
              >
                Enregistrer les modifications
              </Button>
            </form>
          ) : (
            <div className="space-y-6">
              {user?.role === 'job_seeker' && (
                <>
                  {profile?.profile_title && (
                    <div className="flex items-center gap-2 text-gray-300">
                      <Briefcase className="h-5 w-5 text-cyan-400" />
                      <span>{profile.profile_title}</span>
                    </div>
                  )}
                  {profile?.education_level && (
                    <div className="flex items-center gap-2 text-gray-300">
                      <User className="h-5 w-5 text-cyan-400" />
                      <span>{profile.education_level}</span>
                    </div>
                  )}
                  {profile?.skills && (
                    <div>
                      <h3 className="text-lg font-semibold text-white mb-2">Compétences</h3>
                      <p className="text-gray-300">{profile.skills}</p>
                    </div>
                  )}
                  <div className="border-t border-cyan-500/20 pt-6">
                    <h3 className="text-lg font-semibold text-white mb-4">CV</h3>
                    {profile?.cv_url ? (
                      <div className="flex items-center gap-4">
                        <a
                          href={profile.cv_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 text-cyan-400 hover:text-cyan-300"
                        >
                          <FileText className="h-5 w-5" />
                          Voir mon CV
                        </a>
                        <label className="cursor-pointer">
                          <Button variant="outline" className="border-cyan-500/50" asChild>
                            <span>
                              <Upload className="h-4 w-4 mr-2" />
                              Mettre à jour
                            </span>
                          </Button>
                          <input
                            type="file"
                            accept=".pdf,.doc,.docx"
                            className="hidden"
                            onChange={handleCVUpload}
                          />
                        </label>
                      </div>
                    ) : (
                      <label className="cursor-pointer">
                        <Button className="bg-gradient-to-r from-cyan-500 to-violet-600" asChild>
                          <span>
                            <Upload className="h-4 w-4 mr-2" />
                            Uploader mon CV
                          </span>
                        </Button>
                        <input
                          type="file"
                          accept=".pdf,.doc,.docx"
                          className="hidden"
                          onChange={handleCVUpload}
                        />
                      </label>
                    )}
                  </div>
                </>
              )}
              {user?.role === 'employer' && (
                <>
                  {profile?.company_sector && (
                    <div className="flex items-center gap-2 text-gray-300">
                      <Building2 className="h-5 w-5 text-cyan-400" />
                      <span>{profile.company_sector}</span>
                    </div>
                  )}
                  {profile?.company_website && (
                    <div className="flex items-center gap-2 text-gray-300">
                      <Globe className="h-5 w-5 text-cyan-400" />
                      <a href={profile.company_website} target="_blank" rel="noopener noreferrer" className="text-cyan-400 hover:text-cyan-300">
                        {profile.company_website}
                      </a>
                    </div>
                  )}
                  {profile?.company_description && (
                    <div>
                      <h3 className="text-lg font-semibold text-white mb-2">Description</h3>
                      <p className="text-gray-300">{profile.company_description}</p>
                    </div>
                  )}
                </>
              )}
              {profile?.location && (
                <div className="flex items-center gap-2 text-gray-300">
                  <MapPin className="h-5 w-5 text-cyan-400" />
                  <span>{profile.location}</span>
                </div>
              )}
              {profile?.phone && (
                <div className="flex items-center gap-2 text-gray-300">
                  <Mail className="h-5 w-5 text-cyan-400" />
                  <span>{profile.phone}</span>
                </div>
              )}
              {profile?.bio && (
                <div>
                  <h3 className="text-lg font-semibold text-white mb-2">Bio</h3>
                  <p className="text-gray-300 leading-relaxed">{profile.bio}</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
'''

# Write ProfilePage
with open(os.path.join(PAGES_DIR, "ProfilePage.js"), "w") as f:
    f.write(profile_page)

print("✅ ProfilePage.js créé")
