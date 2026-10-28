import React, {useEffect, useMemo, useState} from 'react'
import {ChartNoAxesCombined, Download, FlaskConical, Rocket, SlidersHorizontal, TrendingUp} from 'lucide-react'
import {CartesianGrid, Line, LineChart, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis} from 'recharts'
import {api} from './api.js'
import {makeComparisonRows} from './scenarioCurves.js'

const PRESETS = {
  thrust_n: [25000, 30000, 35000, 40000],
  density_multiplier: [0.5, 1, 1.5, 2],
  propellant_kg: [600, 750, 900, 1050],
  drag_coefficient: [0.2, 0.42, 0.65, 1],
  area_m2: [0.5, 1, 1.5, 2],
}
const PARAMS = {
  thrust_n: 'Engine thrust (N)',
  density_multiplier: 'Air-density multiplier',
  propellant_kg: 'Propellant mass (kg)',
  drag_coefficient: 'Drag coefficient',
  area_m2: 'Frontal area (m²)',
}
const COLORS = ['#69eed0', '#84b0ff', '#ffbf89', '#b4a5ff', '#f4a1b8', '#c8e59c', '#72d2e9']

function saveFile(name, content, type) {
  const blob = new Blob([content], {type})
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = name
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}


export default function ScenarioLab() {
  const [parameter, setParameter] = useState('thrust_n')
  const [valueText, setValueText] = useState(PRESETS.thrust_n.join(', '))
  const [baseline, setBaseline] = useState({thrust_n: 30000, propellant_kg: 900, dry_mass_kg: 480,
    density_multiplier: 1, drag_coefficient: 0.42, area_m2: 1})
  const [data, setData] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const chartData = useMemo(() => data ? makeComparisonRows(data.scenarios) : [], [data])

  async function run(values, kind, base) {
    setBusy(true)
    setError('')
    try {
      if (values.length < 2 || values.length > 7 || values.some(x => !Number.isFinite(x))
          || new Set(values).size !== values.length) {
        throw new Error('Enter 2 to 7 unique numeric scenario values separated by commas.')
      }
      const result = await api('/rocket/compare', {method: 'POST',
        body: JSON.stringify({parameter: kind, values, baseline: base})})
      setData(result)
    } catch (err) { setError(err.message) } finally { setBusy(false) }
  }

  useEffect(() => {
    run(PRESETS.thrust_n, 'thrust_n',
      {thrust_n: 30000, propellant_kg: 900, dry_mass_kg: 480,
        density_multiplier: 1, drag_coefficient: 0.42, area_m2: 1})
  }, [])

  function switchParameter(value) {
    setParameter(value)
    setValueText(PRESETS[value].join(', '))
    setData(null)
    setError('')
  }
  function submit(e) {
    e.preventDefault()
    run(valueText.split(',').map(x => x.trim()).map(x => x ? Number(x) : NaN),
      parameter, baseline)
  }
  function downloadCSV() {
    if (!data) return
    const key = data.parameter
    const headings = [key, 'apogee_km', 'peak_velocity_m_s',
      'max_dynamic_pressure_pa', 'apogee_delta_vs_baseline_pct']
    const csv = [headings.join(',')].concat(data.scenarios.map(x => [
      x.value, x.metrics.apogee_km, x.metrics.peak_velocity_m_s,
      x.metrics.max_dynamic_pressure_pa, x.apogee_delta_vs_baseline_pct ?? ''
    ].join(','))).join('\n') + '\n'
    saveFile('astrasentinel-rocket-comparison-demo.csv', csv, 'text/csv;charset=utf-8')
  }

  return <div>
    <div className="section-heading">
      <div><p className="eyebrow">MODULE 06 / REPRODUCIBLE MISSION EXPERIMENTS</p>
        <h2>Scenario Comparison Lab</h2>
        <p className="muted">Compare bounded changes to one physics parameter, visualize multiple rocket trajectories, and download experimental results.</p></div>
      <span className="pill demo"><i/> EDUCATIONAL SIMULATION</span>
    </div>
    <div className="scenario-layout">
      <section className="panel">
        <h3><SlidersHorizontal size={17}/> Experiment design</h3>
        <form className="form" onSubmit={submit}>
          <label className="scenario-wide">Vary one parameter
            <select value={parameter} onChange={e => switchParameter(e.target.value)}>
              {Object.entries(PARAMS).map(([key, name]) => <option key={key} value={key}>{name}</option>)}
            </select>
          </label>
          <label className="scenario-wide">Values to compare (comma-separated)
            <input value={valueText} onChange={e => setValueText(e.target.value)}
              aria-label="Comma-separated scenario values" required/>
          </label>
          <p className="details scenario-wide">Use 2–7 unique values. The other input parameters stay fixed, allowing a controlled comparison.</p>
          {Object.entries(baseline).map(([key, value]) => <label key={key}>{PARAMS[key] || key.replaceAll('_', ' ')}
            <input type="number" step="any" required value={value}
              onChange={e => setBaseline(old => ({...old, [key]: Number(e.target.value)}))}/>
          </label>)}
          <button type="submit" className="primary" disabled={busy}>
            <Rocket size={16}/>{busy ? 'Running experiment…' : 'Compare simulated trajectories'}
          </button>
        </form>
        {error && <p className="error" role="alert">{error}</p>}
        {data && <div className="scenario-export">
          <button className="secondary" onClick={downloadCSV}><Download size={16}/> Export table CSV</button>
          <button className="secondary" onClick={() => saveFile(
            'astrasentinel-rocket-comparison-demo.json', JSON.stringify(data, null, 2) + '\n',
            'application/json')}><Download size={16}/> Export full JSON</button>
        </div>}
      </section>
      <div>
        <section className="panel">
          <h3><ChartNoAxesCombined size={17}/> Apogee comparison by scenario</h3>
          {data ? <><div className="scenario-results">
            {data.scenarios.map((s, i) => <div className="scenario-stat" key={s.id}
              style={{borderTopColor: COLORS[i]}}>
              <small>{data.parameter} · {s.value} {data.parameter_unit}</small>
              <strong>{s.metrics.apogee_km} km</strong>
              <span>Relative to baseline: {s.apogee_delta_vs_baseline_pct ?? 'N/A'}%</span>
            </div>)}
          </div>
          <div className="scenario-plot" role="img" aria-label="Simulated rocket altitude trajectories by parameter value">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{top:10,right:20,bottom:10,left:0}}>
                <CartesianGrid stroke="#29445b" strokeDasharray="4 7" vertical={false}/>
                <XAxis dataKey="time_s" type="number" domain={['dataMin','dataMax']}
                  tick={{fontSize:10, fill:'#88a9bf'}} tickLine={false}/>
                <YAxis tick={{fontSize:10, fill:'#88a9bf'}} tickLine={false}
                  label={{value:'Altitude (km)',angle:-90,position:'insideLeft',fill:'#91b5c8',fontSize:11}}/>
                <Tooltip contentStyle={{background:'#0c2032', border:'1px solid #38596d',
                  borderRadius:10, color:'#e0f6fd'}}/>
                <Legend wrapperStyle={{fontSize:11}}/>
                {data.scenarios.map((s, i) => <Line key={s.id} dataKey={s.id}
                  name={String(s.value) + ' ' + data.parameter_unit} type="linear"
                  stroke={COLORS[i]} strokeWidth={2.5} dot={false} connectNulls={false}
                  isAnimationActive={false}/>)}
              </LineChart>
            </ResponsiveContainer>
          </div><p className="details">Horizontal axis: simulated seconds. Each curve is downsampled for a responsive comparison; full model output remains available from the single-scenario rocket lab.</p></> :
          <p className="empty">{busy ? 'Computing scenarios…' : 'Run the experiment to see the simulation comparison.'}</p>}
        </section>
        {data && <section className="panel">
          <h3><TrendingUp size={17}/> Numerical scenario results</h3>
          <div className="table-scroll"><table><thead><tr><th>Parameter value</th><th>Apogee (km)</th><th>Max speed (m/s)</th><th>Max Q (Pa)</th></tr></thead>
          <tbody>{data.scenarios.map(s => <tr key={s.id}><td>{s.value} {data.parameter_unit}</td>
            <td>{s.metrics.apogee_km}</td><td>{s.metrics.peak_velocity_m_s}</td>
            <td>{s.metrics.max_dynamic_pressure_pa}</td></tr>)}</tbody></table></div>
          <p className="disclaimer">{data.disclaimer}</p>
        </section>}
        <section className="panel">
          <h3><FlaskConical size={17}/> Research method and scientific limits</h3>
          <p className="details">Change exactly one input while holding the others constant. Every scenario runs the same deterministic one-dimensional, variable-mass, semi-implicit Euler solver. These are sensitivity demonstrations, not uncertainty intervals or validated mission planning.</p>
        </section>
      </div>
    </div>
  </div>
}
