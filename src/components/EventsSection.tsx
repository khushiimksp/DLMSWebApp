import { meterService } from '../services/meterService';
import { AlertCircle, CheckCircle2, History } from 'lucide-react';
import { cn } from '../lib/utils';

export default function EventsSection() {
  const events = meterService.getEvents();

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass p-5 rounded-2xl">
          <p className="text-xs text-slate-500 uppercase tracking-widest font-mono mb-1">Total Tamper Events</p>
          <p className="text-2xl font-bold">12</p>
        </div>
        <div className="glass p-5 rounded-2xl">
          <p className="text-xs text-slate-500 uppercase tracking-widest font-mono mb-1">Active Alarms</p>
          <p className="text-2xl font-bold text-rose-500">0</p>
        </div>
      </div>

      <div className="glass rounded-[2rem] overflow-hidden">
        <div className="p-6 border-b border-slate-800/50 bg-slate-800/20">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <History size={20} className="text-cyan-400" />
            Audit Trail
          </h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-900/50 text-[10px] text-slate-500 uppercase tracking-[0.2em] font-mono">
                <th className="px-6 py-4 border-b border-slate-800/50 font-medium">Timestamp</th>
                <th className="px-6 py-4 border-b border-slate-800/50 font-medium">Event Type</th>
                <th className="px-6 py-4 border-b border-slate-800/50 font-medium">Status</th>
                <th className="px-6 py-4 border-b border-slate-800/50 font-medium">Description</th>
              </tr>
            </thead>
            <tbody className="text-sm">
              {events.map((e) => (
                <tr key={e.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="px-6 py-4 border-b border-slate-800/50 font-mono text-slate-400">
                    {new Date(e.timestamp).toLocaleString()}
                  </td>
                  <td className="px-6 py-4 border-b border-slate-800/50">
                    <span className="font-semibold text-slate-200">{e.type.replace('_', ' ')}</span>
                  </td>
                  <td className="px-6 py-4 border-b border-slate-800/50">
                    <div className={cn(
                      "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider",
                      e.status === 'ACTIVE' ? "bg-rose-500/10 text-rose-500" : "bg-emerald-500/10 text-emerald-500"
                    )}>
                      {e.status === 'ACTIVE' ? <AlertCircle size={12} /> : <CheckCircle2 size={12} />}
                      {e.status}
                    </div>
                  </td>
                  <td className="px-6 py-4 border-b border-slate-800/50 text-slate-400">
                    {e.description}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
