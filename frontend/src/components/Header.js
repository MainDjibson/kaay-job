import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from './ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from './ui/dropdown-menu';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Badge } from './ui/badge';
import { Bell, Briefcase, MessageSquare, Users, User, LogOut, Settings, Info } from 'lucide-react';
import api from '../lib/api';

const Header = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    if (user) {
      loadUnreadCount();
    }
  }, [user]);

  const loadUnreadCount = async () => {
    try {
      const response = await api.get('/messages/unread/count');
      setUnreadCount(response.data.count);
    } catch (error) {
      console.error('Failed to load unread count:', error);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-cyan-500/20 bg-black/90 backdrop-blur-xl">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link to="/" className="flex items-center space-x-2 group" data-testid="logo-link">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-400 via-blue-500 to-violet-600 flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300">
            <Briefcase className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-600 bg-clip-text text-transparent">
            kaay-job
          </span>
        </Link>

        <nav className="hidden md:flex items-center space-x-1">
          <Link to="/jobs" data-testid="jobs-nav-link">
            <Button variant="ghost" className="text-gray-300 hover:text-white hover:bg-cyan-500/10" size="sm">
              <Briefcase className="h-4 w-4 mr-2" />
              Offres d'emploi
            </Button>
          </Link>
          <Link to="/forum" data-testid="forum-nav-link">
            <Button variant="ghost" className="text-gray-300 hover:text-white hover:bg-cyan-500/10" size="sm">
              <Users className="h-4 w-4 mr-2" />
              Forum
            </Button>
          </Link>
          {user && (
            <>
              <Link to="/profile" data-testid="profile-nav-link">
                <Button variant="ghost" className="text-gray-300 hover:text-white hover:bg-cyan-500/10" size="sm">
                  <User className="h-4 w-4 mr-2" />
                  Profil
                </Button>
              </Link>
              <Link to="/messages" data-testid="messages-nav-link">
                <Button
                  variant="ghost"
                  className="text-gray-300 hover:text-white hover:bg-cyan-500/10 relative"
                  size="sm"
                >
                  <MessageSquare className="h-4 w-4 mr-2" />
                  Messages
                  {unreadCount > 0 && (
                    <Badge
                      variant="destructive"
                      className="absolute -top-1 -right-1 h-5 w-5 flex items-center justify-center p-0 text-xs"
                    >
                      {unreadCount}
                    </Badge>
                  )}
                </Button>
              </Link>
            </>
          )}
          <Link to="/about" data-testid="about-nav-link">
            <Button variant="ghost" className="text-gray-300 hover:text-white hover:bg-cyan-500/10" size="sm">
              <Info className="h-4 w-4 mr-2" />
              À propos
            </Button>
          </Link>
        </nav>

        <div className="flex items-center space-x-3">
          {user ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button
                  className="flex items-center space-x-2 hover:opacity-80 transition-opacity"
                  data-testid="user-menu-trigger"
                >
                  <Avatar className="h-9 w-9 ring-2 ring-cyan-500/50">
                    <AvatarImage src="" alt={user.email} />
                    <AvatarFallback className="bg-gradient-to-br from-cyan-400 to-violet-600 text-white">
                      {user.email[0].toUpperCase()}
                    </AvatarFallback>
                  </Avatar>
                  <span className="hidden md:block text-sm font-medium text-gray-300">{user.email}</span>
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56 bg-gray-900 border-cyan-500/20">
                <DropdownMenuItem
                  onClick={() => navigate('/profile')}
                  className="cursor-pointer text-gray-300 focus:bg-cyan-500/10 focus:text-white"
                  data-testid="profile-menu-item"
                >
                  <User className="mr-2 h-4 w-4" />
                  Mon Profil
                </DropdownMenuItem>
                {user.role === 'admin' && (
                  <DropdownMenuItem
                    onClick={() => navigate('/admin')}
                    className="cursor-pointer text-gray-300 focus:bg-cyan-500/10 focus:text-white"
                    data-testid="admin-menu-item"
                  >
                    <Settings className="mr-2 h-4 w-4" />
                    Administration
                  </DropdownMenuItem>
                )}
                <DropdownMenuItem
                  onClick={handleLogout}
                  className="cursor-pointer text-red-400 focus:bg-red-500/10 focus:text-red-400"
                  data-testid="logout-menu-item"
                >
                  <LogOut className="mr-2 h-4 w-4" />
                  Déconnexion
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <div className="flex items-center space-x-2">
              <Link to="/login" data-testid="login-button">
                <Button
                  variant="ghost"
                  size="sm"
                  className="text-gray-300 hover:text-white hover:bg-cyan-500/10"
                >
                  Connexion
                </Button>
              </Link>
              <Link to="/register" data-testid="register-button">
                <Button
                  size="sm"
                  className="bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-600 hover:to-violet-700 text-white font-medium shadow-lg shadow-cyan-500/20"
                >
                  Inscription
                </Button>
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
