'use client';

import React, { useState } from 'react';

export default function ChatInterface() {
    const [messages, setMessages] = useState([
        { id: 1, role: 'assistant', text: 'Hello PM. I am Athena. How can I assist you with Project Universe today?' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg = input;
        setMessages(prev => [...prev, { id: Date.now(), role: 'user', text: userMsg }]);
        setInput('');
        setLoading(true);

        // Simulate API call to Athena Core
        setTimeout(() => {
            setMessages(prev => [...prev, {
                id: Date.now() + 1,
                role: 'assistant',
                text: `Based on the latest graph query, there are 3 critical risks. I have drafted an escalation email for review. \n\nCitation: [Neo4j: Risk r-123 impacting Story-101]`
            }]);
            setLoading(false);
        }, 1500);
    };

    return (
        <div className="flex flex-col h-[80vh] bg-slate-800 rounded-xl border border-slate-700 shadow-2xl overflow-hidden">
            <div className="bg-slate-800 border-b border-slate-700 p-4">
                <h2 className="text-xl font-bold flex items-center gap-2">
                    <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
                    Athena Chat Console
                </h2>
                <p className="text-sm text-slate-400">Powered by LangGraph & GraphRAG</p>
            </div>

            <div className="flex-1 p-6 overflow-y-auto space-y-6">
                {messages.map((msg) => (
                    <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[75%] p-4 rounded-2xl ${msg.role === 'user'
                                ? 'bg-blue-600 text-white rounded-br-sm'
                                : 'bg-slate-700 text-slate-200 rounded-bl-sm border border-slate-600'
                            }`}>
                            <p className="whitespace-pre-wrap">{msg.text}</p>
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-slate-700 p-4 rounded-2xl rounded-bl-sm border border-slate-600 flex gap-2 items-center">
                            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" />
                            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
                        </div>
                    </div>
                )}
            </div>

            <div className="p-4 bg-slate-800 border-t border-slate-700">
                <form onSubmit={handleSend} className="flex gap-4">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask Athena about project risks or status..."
                        className="flex-1 bg-slate-900 border border-slate-600 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all placeholder:text-slate-500"
                    />
                    <button
                        type="submit"
                        disabled={loading || !input.trim()}
                        className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-500 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                    >
                        Send
                    </button>
                </form>
            </div>
        </div>
    );
}
