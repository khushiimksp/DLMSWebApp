import { meterService } from '../services/meterService';
import { Download, Landmark } from 'lucide-react';

export default function BillingSection() {
  const billing = meterService.getBillingHistory();

  return (
    <div className="space-y-6">
      <div className="glass p-8 rounded-[2rem]">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-6 mb-10">
          <div className="flex items-center gap-4">
            <div className="p-4 rounded-2xl bg-cyan-500/10 text-cyan-400">
              <Landmark size={32} />
            </div>
            <div>
              <h3 className="text-2xl font-bold">Billing Records</h3>
              <p className="text-sm text-slate-400">Historical consumption and demand logs per billing cycle</p>
            </div>
          </div>
          <button className="flex items-center gap-2 px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-sm font-medium transition-colors">
            <Download size={18} />
            Export Settlement (CSV)
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-900/50 text-[10px] text-slate-500 uppercase tracking-[0.2em] font-mono">
                <th className="px-6 py-4 border-b border-slate-800/50 font-medium">Billing Date</th>
                <th className="px-6 py-4 border-b border-slate-800/50 font-medium">Total Energy (kWh)</th>
                <th className="px-6 py-4 border-b border-slate-800/50 font-medium">Max Demand (kW)</th>
                <th className="px-6 py-4 border-b border-slate-800/50 font-medium">Tariff 1 (Units)</th>
                <th className="px-6 py-4 border-b border-slate-800/50 font-medium">Tariff 2 (Units)</th>
              </tr>
            </thead>
            <tbody className="text-sm">
              {billing.map((b) => (
                <tr key={b.date} className="hover:bg-slate-800/30 transition-colors">
                  <td className="px-6 py-4 border-b border-slate-800/50 font-mono text-slate-200">
                    {b.date}
                  </td>
                  <td className="px-6 py-4 border-b border-slate-800/50 font-semibold text-white">
                    {b.active_energy.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 border-b border-slate-800/50 text-amber-400">
                    {b.max_demand}
                  </td>
                  <td className="px-6 py-4 border-b border-slate-800/50 text-slate-400">
                    {b.tariff_1.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 border-b border-slate-800/50 text-slate-400">
                    {b.tariff_2.toLocaleString()}
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
