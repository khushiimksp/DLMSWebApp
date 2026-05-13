import { InstantaneousReading, MeterEvent, BillingRecord } from '../types';

class MeterService {
  private energyAccumulator: number = 10245.67;
  private readingsHistory: InstantaneousReading[] = [];

  constructor() {
    // Generate some initial history
    for (let i = 60; i >= 0; i--) {
      const time = new Date(Date.now() - i * 5000);
      this.readingsHistory.push(this.generateReading(time));
    }
  }

  private generateReading(timestamp: Date = new Date()): InstantaneousReading {
    const v_base = 230 + (Math.random() * 4 - 2);
    const i_base = 8 + (Math.random() * 4 - 2);
    const pf = 0.92 + (Math.random() * 0.05);
    
    this.energyAccumulator += (i_base * v_base * pf) / (3600 * 1000) * 5; // Simulating 5s increment

    return {
      timestamp: timestamp.toISOString(),
      voltage_r: v_base + (Math.random() * 0.5),
      voltage_y: v_base + (Math.random() * 0.5 - 0.2),
      voltage_b: v_base + (Math.random() * 0.5 + 0.3),
      current_r: i_base + (Math.random() * 0.2),
      current_y: i_base * 0.95 + (Math.random() * 0.2),
      current_b: i_base * 1.05 + (Math.random() * 0.2),
      frequency: 50 + (Math.random() * 0.1 - 0.05),
      power_factor: pf,
      active_power: (v_base * i_base * pf) / 1000,
      reactive_power: (v_base * i_base * Math.sin(Math.acos(pf))) / 1000,
      apparent_power: (v_base * i_base) / 1000,
      active_energy: this.energyAccumulator
    };
  }

  getLatestReading(): InstantaneousReading {
    const newReading = this.generateReading();
    this.readingsHistory.push(newReading);
    if (this.readingsHistory.length > 200) this.readingsHistory.shift();
    return newReading;
  }

  getHistory(): InstantaneousReading[] {
    return this.readingsHistory;
  }

  getEvents(): MeterEvent[] {
    return [
      {
        id: '1',
        timestamp: new Date(Date.now() - 3600000).toISOString(),
        type: 'POWER_FAILURE',
        status: 'RESTORED',
        description: 'Main grid supply interrupted and restored after 5 mins'
      },
      {
        id: '2',
        timestamp: new Date(Date.now() - 86400000).toISOString(),
        type: 'MAGNETIC_TAMPER',
        status: 'RESTORED',
        description: 'Strong magnetic field detected near meter'
      }
    ];
  }

  getBillingHistory(): BillingRecord[] {
    return [
      { date: '2024-04-01', active_energy: 10245.67, max_demand: 4.5, tariff_1: 6120.30, tariff_2: 4125.37 },
      { date: '2024-03-01', active_energy: 9850.42, max_demand: 4.2, tariff_1: 5890.12, tariff_2: 3960.30 },
      { date: '2024-02-01', active_energy: 9420.15, max_demand: 5.1, tariff_1: 5640.45, tariff_2: 3779.70 }
    ];
  }
}

export const meterService = new MeterService();
