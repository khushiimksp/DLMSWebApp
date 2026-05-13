import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';
import { meterService } from '../services/meterService';
import { useEffect, useState } from 'react';
import { InstantaneousReading } from '../types';

export default function ChartsSection() {
  const [data, setData] = useState<InstantaneousReading[]>(meterService.getHistory());

  useEffect(() => {
    const interval = setInterval(() => {
      setData([...meterService.getHistory()]);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const chartData = data.map(d => ({
    ...d,
    time: new Date(d.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  }));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* Voltage Chart */}
      <div className="glass p-8 rounded-[2rem]">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h3 className="text-lg font-semibold">Voltage Stability</h3>
            <p className="text-xs text-slate-500">Real-time Phase R/Y/B Monitoring (V)</p>
          </div>
        </div>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
              <XAxis dataKey="time" stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} />
              <YAxis domain={[220, 240]} stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px' }}
                itemStyle={{ fontSize: '12px' }}
              />
              <Line type="monotone" dataKey="voltage_r" stroke="#3b82f6" strokeWidth={2} dot={false} isAnimationActive={false} />
              <Line type="monotone" dataKey="voltage_y" stroke="#eab308" strokeWidth={2} dot={false} isAnimationActive={false} />
              <Line type="monotone" dataKey="voltage_b" stroke="#ef4444" strokeWidth={2} dot={false} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Power Chart */}
      <div className="glass p-8 rounded-[2rem]">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h3 className="text-lg font-semibold">Load Profile</h3>
            <p className="text-xs text-slate-500">Active Power Consumption Trend (kW)</p>
          </div>
        </div>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="colorPower" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
              <XAxis dataKey="time" stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} />
              <YAxis stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px' }}
                itemStyle={{ fontSize: '12px' }}
              />
              <Area type="monotone" dataKey="active_power" stroke="#06b6d4" fillOpacity={1} fill="url(#colorPower)" isAnimationActive={false} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
