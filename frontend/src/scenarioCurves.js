/**
 * Resample independent simulation trajectories on a shared *time* axis.
 *
 * Multiple downsampled rocket runs may stop at different timestamps, so simply
 * joining by exact timestamps creates fragmented Recharts lines. Linear
 * interpolation only connects measured samples *inside* each scenario's range.
 * Curves never extrapolate after an early ground impact or other run endpoint.
 */
export function makeComparisonRows(scenarios, intervals = 180) {
  if (!Array.isArray(scenarios) || scenarios.length === 0) return []
  if (!Number.isInteger(intervals) || intervals < 2 || intervals > 500) {
    throw new RangeError('Comparison sampling intervals must be 2..500')
  }
  for (const scenario of scenarios) {
    if (!scenario?.id || !Array.isArray(scenario.curve) || scenario.curve.length < 2) {
      throw new TypeError('Every scenario requires an id and at least two points')
    }
    if (scenario.curve.some((p, i) =>
      !Number.isFinite(p?.time_s) || !Number.isFinite(p?.altitude_km) ||
      (i > 0 && p.time_s <= scenario.curve[i - 1].time_s))) {
      throw new TypeError('Scenario curves require finite, strictly increasing time samples')
    }
  }
  const maxTime = Math.max(...scenarios.map(s => s.curve[s.curve.length - 1].time_s))
  if (maxTime <= 0) throw new RangeError('Maximum simulated time must be positive')
  const cursors = scenarios.map(() => 0)
  return Array.from({length: intervals + 1}, (_, step) => {
    const t = maxTime * step / intervals
    const row = {time_s: Number(t.toFixed(3))}
    scenarios.forEach(({id, curve}, index) => {
      if (t < curve[0].time_s || t > curve[curve.length - 1].time_s) {
        row[id] = null
        return
      }
      let cursor = cursors[index]
      while (cursor + 1 < curve.length - 1 && curve[cursor + 1].time_s < t) {
        cursor++
      }
      cursors[index] = cursor
      const a = curve[cursor]
      const b = curve[cursor + 1]
      const ratio = Math.max(0, Math.min(1, (t - a.time_s) / (b.time_s - a.time_s)))
      row[id] = a.altitude_km + ratio * (b.altitude_km - a.altitude_km)
    })
    return row
  })
}
