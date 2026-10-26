import React, {useState} from 'react'
import {CloudSun, Wind, Gauge, Info, ArrowDownToLine} from 'lucide-react'
import {CartesianGrid,Legend,Line,LineChart,ResponsiveContainer,Tooltip,XAxis,YAxis} from 'recharts'

export default function AtmospherePage({state}) {
  const [multiplier,setMultiplier]=useState(1)
  const data=state.data
  const points=(data?.points||[]).map(p=>({
    altitude_km:p.altitude_km,
    baseline:p.density_kg_m3,
    adjusted:p.density_kg_m3*multiplier,
  }))
  const at10=points.find(p=>p.altitude_km===10)
  const at50=points.find(p=>p.altitude_km===50)
  return <div>
    <div className="section-heading">
      <div><p className="eyebrow">MODULE 05 / ATMOSPHERIC SCIENCE</p>
        <h2>Atmospheric Density Laboratory</h2>
        <p className="muted">Explore how a simplified exponential atmosphere responds to changes in sea-level density.</p>
      </div><span className="pill demo"><i/>EDUCATIONAL APPROXIMATION</span>
    </div>
    <div className="atmosphere-hero">
      <div className="atmosphere-scene">
        <div className="atmo-sky"><div className="atmo-glow"/><div className="atmo-earth"/>
          <span className="atmo-star">✦</span><span className="atmo-alt top">100 KM · UPPER LAYER</span>
          <span className="atmo-alt mid">50 KM · UPPER STRATOSPHERE</span>
          <span className="atmo-alt low">10 KM · TROPOSPHERE</span>
        </div>
      </div>
      <div className="atmosphere-details">
        <div className="panel-icon"><CloudSun size={25}/></div>
        <p className="eyebrow">DENSITY ASSUMPTION</p>
        <h3>Pressure fades exponentially with altitude.</h3>
        <p>Use the multiplier to compare hypothetical density scenarios. This model does not include real weather, thermospheric composition, solar forcing, or winds.</p>
        <label htmlFor="atmo-multiplier">Density multiplier <strong>{multiplier.toFixed(1)}×</strong></label>
        <input id="atmo-multiplier" type="range" min="0.2" max="3" step="0.1"
          value={multiplier} onChange={event=>setMultiplier(Number(event.target.value))}/>
        <div className="atmo-chips"><span>SEA LEVEL 1.225 kg/m³</span><span>SCALE HEIGHT 8,500 m</span></div>
      </div>
    </div>
    {state.error&&<div className="error">{state.error}</div>}
    {state.loading&&!data&&<div className="empty">Loading atmospheric model…</div>}
    {data&&<>
      <div className="triple">
        <div className="metric"><span className="metric-title"><Gauge size={17}/>0 km · sea level</span>
          <strong>{(1.225*multiplier).toFixed(4)}</strong><small>kg/m³ · scaled density</small></div>
        <div className="metric"><span className="metric-title"><Wind size={17}/>10 km · lower atmosphere</span>
          <strong>{at10?.adjusted.toFixed(4)}</strong><small>kg/m³ · scaled density</small></div>
        <div className="metric"><span className="metric-title"><ArrowDownToLine size={17}/>50 km · higher altitude</span>
          <strong>{at50?.adjusted.toExponential(3)}</strong><small>kg/m³ · scaled density</small></div>
      </div>
      <section className="panel"><h3><CloudSun size={17}/> Air density vs altitude (logarithmic scale)</h3>
        <div style={{width:'100%',height:350}}><ResponsiveContainer>
          <LineChart data={points} margin={{top:12,right:18,bottom:10,left:6}}>
            <CartesianGrid stroke="#284057" strokeDasharray="3 7"/>
            <XAxis dataKey="altitude_km" tick={{fill:'#92afbf',fontSize:11}}
              label={{value:'Altitude (km)',position:'insideBottom',offset:-5,fill:'#a1bbcf'}}/>
            <YAxis domain={[0.000001,4]} scale="log" tick={{fill:'#92afbf',fontSize:11}}
              width={68} tickFormatter={v=>Number(v).toExponential(0)}/>
            <Tooltip contentStyle={{background:'#0d2237',border:'1px solid #346277',borderRadius:12}}
              formatter={v=>[Number(v).toExponential(4)+' kg/m³']}/>
            <Legend verticalAlign="top" height={35}/>
            <Line name="Baseline density" dataKey="baseline" stroke="#7dabff" dot={false} strokeWidth={2.5}/>
            <Line name="Scenario density" dataKey="adjusted" stroke="#70efd4" dot={false} strokeWidth={2.5}/>
          </LineChart>
        </ResponsiveContainer></div>
      </section>
      <div className="panel"><h3><Info size={17}/> Why these curves matter</h3>
        <p className="details">Aerodynamic drag scales linearly with air density at fixed area, drag coefficient and speed. In the Rocket Lab, changing the same density multiplier changes modeled aerodynamic loading and resulting trajectory. The one-scale-height profile is not a physically validated representation of Earth's whole atmosphere.</p>
        <p className="details">The model deliberately extends to 100 km to visualize exponential decline. At high altitude its accuracy is especially limited. Use it only for educational comparisons, not thermal, flight or orbital decay predictions.</p>
      </div>
    </>}
  </div>
}
