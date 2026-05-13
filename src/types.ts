export interface InstantaneousReading {
  timestamp: string;
  voltage_r: number;
  voltage_y: number;
  voltage_b: number;
  current_r: number;
  current_y: number;
  current_b: number;
  frequency: number;
  power_factor: number;
  active_power: number;
  reactive_power: number;
  apparent_power: number;
  active_energy: number;
}

export interface MeterEvent {
  id: string;
  timestamp: string;
  type: 'MAGNETIC_TAMPER' | 'COVER_OPEN' | 'POWER_FAILURE' | 'REVERSE_CURRENT' | 'NEUTRAL_DISTURBANCE';
  status: 'ACTIVE' | 'RESTORED';
  description: string;
}

export interface BillingRecord {
  date: string;
  active_energy: number;
  max_demand: number;
  tariff_1: number;
  tariff_2: number;
}
