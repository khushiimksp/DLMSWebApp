import { InstantaneousReading } from '../types';
import { motion } from 'motion/react';
import { formatValue } from '../lib/utils';
import { 
  Zap, 
  Activity, 
  Gauge, 
  Battery, 
  Wind, 
  TrendingUp 
} from 'lucide-react';

interface Props {
  latest: InstantaneousReading;
}

export default function KPISection({ latest }: Props) {
  const metrics = [
    { label: 'Voltage R', value: latest.voltage_r, unit: 'V', icon: Battery, color: 'text-blue-400', bg: 'bg-blue-500/10' },
    { label: 'Current R', value: latest.current_r, unit: 'A', icon: Activity, color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
    { label: 'Frequency', value: latest.frequency, unit: 'Hz', icon: Wind, color: 'text-amber-400', bg: 'bg-amber-500/10' },
    { label: 'Active Power', value: latest.active_power, unit: 'kW', icon: Zap, color: 'text-cyan-400', bg: 'bg-cyan-500/10' },
    { label: 'Power Factor', value: latest.power_factor, unit: '', icon: Gauge, color: 'text-purple-400', bg: 'bg-purple-500/10', decimals: 3 },
    { label: 'Total Energy', value: latest.active_energy, unit: 'kWh', icon: TrendingUp, color: 'text-rose-400', bg: 'bg-rose-500/10' },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {metrics.map((m, idx) => (
        <motion.div
          key={m.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: idx * 0.05 }}
          className="glass p-6 rounded-3xl group hover:border-slate-700 transition-colors"
        >
          <div className="flex items-center justify-between mb-4">
            <div className={`p-3 rounded-2xl ${m.bg}`}>
              <m.icon className={m.color} size={24} />
            </div>
            <div className="flex flex-col items-end">
               <span className="text-3xl font-bold tracking-tight">{formatValue(m.value, m.decimals ?? 2)}</span>
               <span className="text-xs text-slate-500 font-mono uppercase tracking-widest">{m.unit}</span>
            </div>
          </div>
          <p className="text-sm text-slate-400 group-hover:text-slate-200 transition-colors">{m.label}</p>
        </motion.div>
      ))}
    </div>
  );
}
