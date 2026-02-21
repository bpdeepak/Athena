import React from 'react';

export default function HealthDashboard() {
  return (
    <div className="space-y-8 animate-in fade-in zoom-in duration-500">
      <header>
        <h2 className="text-3xl font-bold text-white mb-2">Program Health Overview</h2>
        <p className="text-slate-400">Real-time status synced from Project Universe.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-xl relative overflow-hidden group hover:border-blue-500 transition-all">
          <div className="absolute top-0 right-0 w-24 h-24 bg-blue-500/10 rounded-full blur-2xl -mt-8 -mr-8 group-hover:bg-blue-500/20 transition-all" />
          <h3 className="text-xl font-semibold mb-1">Active Epics</h3>
          <p className="text-4xl font-bold text-blue-400">12</p>
          <p className="text-sm text-slate-400 mt-2">4 on track, 8 at risk</p>
        </div>

        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-xl relative overflow-hidden group hover:border-red-500 transition-all">
          <div className="absolute top-0 right-0 w-24 h-24 bg-red-500/10 rounded-full blur-2xl -mt-8 -mr-8 group-hover:bg-red-500/20 transition-all" />
          <h3 className="text-xl font-semibold mb-1">Critical Risks</h3>
          <p className="text-4xl font-bold text-red-500">3</p>
          <p className="text-sm text-slate-400 mt-2">Require immediate attention</p>
        </div>

        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-xl relative overflow-hidden group hover:border-green-500 transition-all">
          <div className="absolute top-0 right-0 w-24 h-24 bg-green-500/10 rounded-full blur-2xl -mt-8 -mr-8 group-hover:bg-green-500/20 transition-all" />
          <h3 className="text-xl font-semibold mb-1">Athena Status</h3>
          <p className="text-4xl font-bold text-green-400">Operational</p>
          <p className="text-sm text-slate-400 mt-2">Listening for webhooks...</p>
        </div>
      </div>

      <div className="bg-slate-800 rounded-xl border border-slate-700 shadow-xl p-6">
        <h3 className="text-xl font-semibold mb-4 border-b border-slate-700 pb-2">Recent Changes (Action & Tracking Log)</h3>
        <ul className="space-y-4">
          {[
            { id: 1, action: "Entity Sync", details: "Synced STORY-101 to Neo4j and ChromaDB", time: "2 mins ago" },
            { id: 2, action: "Risk Escalation", details: "Elevated risk r-123 to CRITICAL status due to deadline slip.", time: "15 mins ago", alert: true },
            { id: 3, action: "Milestone Created", details: "Q3 Release milestone added by PM.", time: "1 hr ago" }
          ].map(log => (
            <li key={log.id} className="flex items-start gap-4 p-3 rounded-lg hover:bg-slate-700/50 transition-colors">
              <div className={`w-2 h-2 mt-2 rounded-full ${log.alert ? 'bg-red-500 animate-pulse' : 'bg-blue-500'}`} />
              <div>
                <p className="font-medium text-slate-200">{log.action}</p>
                <p className="text-slate-400 text-sm mt-1">{log.details}</p>
              </div>
              <span className="ml-auto text-xs text-slate-500">{log.time}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
