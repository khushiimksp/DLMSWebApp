import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  Activity, 
  AlertTriangle, 
  FileText, 
  History, 
  Zap, 
  Menu, 
  X,
  Cpu
} from 'lucide-react';
import { meterService } from './services/meterService';
import { InstantaneousReading, MeterEvent } from './types';
import KPISection from './components/KPISection';
import ChartsSection from './components/ChartsSection';
import EventsSection from './components/EventsSection';
import BillingSection from './components/BillingSection';
import { cn } from './lib/utils';

export default function App() {
  const [activeTab, setActiveTab] = useState<'live' | 'events' | 'history' | 'billing'>('live');
  const [latestReading, setLatestReading] = useState<InstantaneousReading>(meterService.getLatestReading());
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setLatestReading(meterService.getLatestReading());
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const navItems = [
    { id: 'live', label: 'Live Monitoring', icon: Activity },
    { id: 'events', label: 'Tamper Alerts', icon: AlertTriangle },
    { id: 'history', label: 'Load Survey', icon: History },
    { id: 'billing', label: 'Billing Data', icon: FileText },
  ] as const;

  return (
    <div className="flex h-screen bg-slate-950 font-sans selection:bg-cyan-500/30">
      {/* Mobile Overlay */}
      <AnimatePresence>
        {isSidebarOpen && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsSidebarOpen(false)}
            className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <aside className={cn(
        "fixed inset-y-0 left-0 z-50 w-72 transform bg-slate-900 border-r border-slate-800 transition-transform duration-300 ease-in-out lg:relative lg:translate-x-0",
        !isSidebarOpen && "-translate-x-full"
      )}>
        <div className="flex flex-col h-full p-6">
          <div className="flex items-center gap-3 mb-10">
            <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-cyan-500 text-white shadow-lg shadow-cyan-500/20">
              <Zap size={24} />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-white">DLMS Monitor</h1>
              <p className="text-xs text-slate-400 font-mono">v1.2.0-stable</p>
            </div>
          </div>

          <nav className="space-y-2 flex-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveTab(item.id);
                    setIsSidebarOpen(false);
                  }}
                  className={cn(
                    "flex items-center w-full gap-3 px-4 py-3 rounded-xl transition-all duration-200 group",
                    isActive 
                      ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 shadow-lg shadow-cyan-500/5" 
                      : "text-slate-400 hover:bg-slate-800/50 hover:text-slate-200"
                  )}
                >
                  <Icon size={20} className={cn(isActive ? "text-cyan-400" : "text-slate-500 group-hover:text-slate-300")} />
                  <span className="font-medium">{item.label}</span>
                  {isActive && (
                    <motion.div 
                      layoutId="nav-active" 
                      className="ml-auto w-1.5 h-1.5 rounded-full bg-cyan-400"
                    />
                  )}
                </button>
              );
            })}
          </nav>

          <div className="mt-auto pt-6 border-t border-slate-800">
            <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-800/50">
              <div className="w-8 h-8 rounded-lg bg-green-500/20 border border-green-500/30 flex items-center justify-center">
                <Cpu size={16} className="text-green-400" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-slate-200 truncate">Meter SIM-001</p>
                <div className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                  <span className="text-[10px] text-green-400 font-mono uppercase tracking-widest">Simulation Mode</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Header */}
        <header className="h-16 flex items-center justify-between px-6 bg-slate-900/50 border-b border-slate-800/50 backdrop-blur-md sticky top-0 z-30">
          <button 
            onClick={() => setIsSidebarOpen(true)}
            className="p-2 -ml-2 text-slate-400 hover:text-white lg:hidden"
          >
            <Menu size={24} />
          </button>
          
          <div className="flex items-center gap-4 ml-auto">
            <div className="hidden sm:flex flex-col items-end">
              <span className="text-xs text-slate-500 uppercase tracking-widest font-mono">Server Time</span>
              <span className="text-sm text-slate-300 font-mono">{new Date().toLocaleTimeString()}</span>
            </div>
          </div>
        </header>

        {/* Scrollable Content Area */}
        <div className="flex-1 overflow-y-auto p-6 scrollbar-thin scrollbar-track-transparent scrollbar-thumb-slate-800">
          <div className="max-w-7xl mx-auto space-y-8 pb-10">
            <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
              <div>
                <h2 className="text-3xl font-bold tracking-tight text-white">
                  {navItems.find(i => i.id === activeTab)?.label}
                </h2>
                <p className="text-slate-400 mt-1">
                  Monitoring smart meter node: <span className="text-cyan-400 font-mono">192.168.1.100:4059</span>
                </p>
              </div>
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-[10px] text-slate-400 font-mono tracking-tighter">
                LAST REFRESH: {new Date(latestReading.timestamp).toLocaleTimeString()}
              </div>
            </div>

            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.2 }}
              >
                {activeTab === 'live' && (
                  <div className="space-y-8">
                    <KPISection latest={latestReading} />
                    <ChartsSection />
                  </div>
                )}
                {activeTab === 'events' && <EventsSection />}
                {activeTab === 'history' && <div className="glass p-12 rounded-3xl text-center text-slate-500 border-dashed">Historical load survey charts coming in next update.</div>}
                {activeTab === 'billing' && <BillingSection />}
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </main>
    </div>
  );
}
