'use client';

import React, { useState } from 'react';

export default function GodMode() {
    const [logs, setLogs] = useState<string[]>([]);

    const triggerChaos = async (action: string) => {
        setLogs(prev => [`[${new Date().toLocaleTimeString()}] Triggered: ${action}`, ...prev]);

        // Simulate hitting the Simulator API
        setTimeout(() => {
            setLogs(prev => [`[${new Date().toLocaleTimeString()}] Success: ${action} injected. Webhook fired.`, ...prev]);
        }, 800);
    };

    const chaosOptions = [
        { id: 'blocker', name: 'Inject Blocker', desc: 'Sets a random story to BLOCKED status.', color: 'red' },
        { id: 'scope', name: 'Inject Scope Creep', desc: 'Adds 5 points to an in-progress story.', color: 'orange' },
        { id: 'risk', name: 'Escalate Risk', desc: 'Elevates a random active risk to CRITICAL.', color: 'rose' },
        { id: 'milestone', name: 'Delay Milestone', desc: 'Turns an Epic RAG status to AMBER/RED.', color: 'yellow' }
    ];

    return (
        <div className="space-y-8 animate-in slide-in-from-bottom-4 duration-500">
            <header>
                <h2 className="text-3xl font-bold text-red-500 mb-2 flex items-center gap-3">
                    <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    God Mode Console
                </h2>
                <p className="text-slate-400">Inject enterprise chaos into Project Universe to test Athena's proactive capabilities.</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                    <h3 className="text-xl font-semibold mb-4">Chaos Injectors</h3>
                    {chaosOptions.map(opt => (
                        <button
                            key={opt.id}
                            onClick={() => triggerChaos(opt.name)}
                            className="w-full text-left bg-slate-800 p-5 rounded-xl border border-slate-700 shadow-lg hover:border-red-500/50 hover:bg-slate-700/50 transition-all group flex items-start gap-4"
                        >
                            <div className={`p-3 rounded-lg bg-${opt.color}-500/10 text-${opt.color}-400 group-hover:bg-${opt.color}-500/20 transition-colors`}>
                                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                            </div>
                            <div>
                                <h4 className="font-semibold text-lg">{opt.name}</h4>
                                <p className="text-slate-400 text-sm mt-1">{opt.desc}</p>
                            </div>
                        </button>
                    ))}
                </div>

                <div className="bg-black/50 rounded-xl border border-slate-700 shadow-inner overflow-hidden flex flex-col h-[500px]">
                    <div className="bg-slate-800 border-b border-slate-700 p-3 flex justify-between items-center">
                        <h3 className="text-sm font-semibold font-mono text-slate-300">Terminal Output</h3>
                        <button onClick={() => setLogs([])} className="text-xs text-slate-500 hover:text-slate-300">Clear</button>
                    </div>
                    <div className="flex-1 p-4 font-mono text-sm overflow-y-auto space-y-2">
                        {logs.length === 0 ? (
                            <p className="text-slate-600 italic">No events generated yet. Waiting for chaos...</p>
                        ) : (
                            logs.map((log, i) => (
                                <div key={i} className={`${log.includes('Success') ? 'text-green-400' : 'text-blue-400'}`}>
                                    {log}
                                </div>
                            ))
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
