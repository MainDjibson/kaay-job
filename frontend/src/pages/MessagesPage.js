import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Avatar, AvatarFallback } from '../components/ui/avatar';
import { Send } from 'lucide-react';
import api from '../lib/api';

const MessagesPage = () => {
  const { user } = useAuth();
  const [conversations, setConversations] = useState([]);
  const [selectedConv, setSelectedConv] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    loadConversations();
  }, []);

  useEffect(() => {
    if (selectedConv) {
      loadMessages(selectedConv.user_id);
    }
  }, [selectedConv]);

  const loadConversations = async () => {
    try {
      const response = await api.get('/messages/conversations');
      setConversations(response.data);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  };

  const loadMessages = async (userId) => {
    try {
      const response = await api.get(`/messages/${userId}`);
      setMessages(response.data);
    } catch (error) {
      console.error('Failed to load messages:', error);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !selectedConv) return;

    try {
      await api.post('/messages', {
        receiver_id: selectedConv.user_id,
        content: newMessage,
      });
      setNewMessage('');
      loadMessages(selectedConv.user_id);
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  return (
    <div className="min-h-screen bg-black">
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-violet-600 bg-clip-text text-transparent mb-8">
          Messages
        </h1>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="space-y-2">
            {conversations.map((conv) => (
              <div
                key={conv.user_id}
                onClick={() => setSelectedConv(conv)}
                className={`p-4 rounded-xl cursor-pointer transition-colors ${
                  selectedConv?.user_id === conv.user_id
                    ? 'bg-cyan-900/30 border-cyan-500/50'
                    : 'bg-gray-900 border-gray-800 hover:bg-gray-800'
                } border`}
              >
                <div className="flex items-center gap-3">
                  <Avatar>
                    <AvatarFallback className="bg-gradient-to-br from-cyan-400 to-violet-600">
                      {conv.profile.full_name?.[0] || conv.profile.company_name?.[0] || '?'}
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex-1">
                    <div className="font-medium text-white">
                      {conv.profile.full_name || conv.profile.company_name}
                    </div>
                    <div className="text-sm text-gray-400">{conv.email}</div>
                  </div>
                  {conv.unread_count > 0 && (
                    <div className="bg-cyan-500 text-white text-xs rounded-full w-6 h-6 flex items-center justify-center">
                      {conv.unread_count}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>

          <div className="md:col-span-2 bg-gradient-to-br from-gray-900 to-gray-950 border border-cyan-500/20 rounded-2xl p-6">
            {selectedConv ? (
              <>
                <div className="border-b border-cyan-500/20 pb-4 mb-4">
                  <h2 className="text-xl font-bold text-white">
                    {selectedConv.profile.full_name || selectedConv.profile.company_name}
                  </h2>
                </div>

                <div className="h-96 overflow-y-auto mb-4 space-y-4">
                  {messages.map((msg) => (
                    <div
                      key={msg.id}
                      className={`flex ${msg.sender_id === user.id ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-xs p-3 rounded-lg ${
                          msg.sender_id === user.id
                            ? 'bg-cyan-600 text-white'
                            : 'bg-gray-800 text-gray-300'
                        }`}
                      >
                        {msg.content}
                      </div>
                    </div>
                  ))}
                </div>

                <form onSubmit={handleSendMessage} className="flex gap-2">
                  <Input
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    placeholder="Votre message..."
                    className="bg-black/50 border-cyan-500/30 text-white flex-1"
                  />
                  <Button
                    type="submit"
                    className="bg-gradient-to-r from-cyan-500 to-violet-600"
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </form>
              </>
            ) : (
              <div className="h-96 flex items-center justify-center text-gray-400">
                Sélectionnez une conversation
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MessagesPage;
