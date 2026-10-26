import React, {useEffect,useState} from 'react'
import {Activity,Atom,ChartNoAxesCombined,CloudSun,Cpu,Database,Earth,Gauge,GitBranch,
  Orbit,Radio,RefreshCw,Rocket,Satellite,ShieldAlert,SlidersHorizontal,Sparkles,TrendingUp,
  Waves,Zap} from 'lucide-react'
import {CartesianGrid,Line,LineChart,ResponsiveContainer,Tooltip,XAxis,YAxis,Legend,ReferenceLine} from 'recharts'
import OrbitGlobe from './OrbitGlobe.jsx'
import AtmospherePage from './AtmospherePage.jsx'
import MissionExportPanel from './MissionExportPanel.jsx'
import {api} from './api.js'

const nav=[
  ['overview','Mission Overview',Gauge],['orbit','Orbital Explorer',Orbit],
  ['telemetry','Satellite Health AI',Activity],['weather','Space Weather',CloudSun],
  ['rocket','Rocket Lab',Rocket],['atmosphere','Atmosphere Model',CloudSun],['architecture','System Architecture',GitBranch]]
const colors=['#70efd4','#80adff','#f3ba7c','#b8a9ff']
function useEndpoint(path,version){
  const [state,set]=useState({data:null,loading:true,error:null})
  useEffect(()=>{let active=true;set(s=>({...s,loading:true,error:null}))
    api(path).then(data=>active&&set({data,loading:false,error:null}))
      .catch(err=>active&&set({data:null,loading:false,error:err.message}))
    return()=>{active=false}
  },[path,version])
  return state
}
function Pill({children,demo=false}){return <span className={'pill '+(demo?'demo':'')}><i/>{children}</span>}
function Panel({title,icon:Icon,children,className=''}){return <section className={'panel '+className}><h3>{Icon&&<Icon size={17}/>} {title}</h3>{children}</section>}
function Metric({icon:Icon,label,value,sub,color=0}){return <div className="metric">
  <span className="metric-title"><Icon size={17} color={colors[color]}/>{label}</span>
  <strong>{value??'—'}</strong><small>{sub}</small></div>}
function Header({eyebrow,title,desc,badge}){return <div className="section-heading">
  <div><p className="eyebrow">{eyebrow}</p><h2>{title}</h2><p className="muted">{desc}</p></div>{badge&&<Pill>{badge}</Pill>}</div>}
function Source({source,age,status}){const demo=source&&source!=='CelesTrak'&&source!=='NOAA SWPC'
  return <div className="source"><Pill demo={demo||status==='stale'}>{demo?'DEMO / HISTORICAL':status==='stale'?'STALE DATA':'PUBLIC DATA'}</Pill>
    <span>Source: {source||'—'}</span>{age!==null&&age!==undefined&&<span>Age: {age}h</span>}</div>}
function Plot({data,series,x='time',reference,height=270}){
  if(!data?.length)return <div className="empty">Waiting for chart data...</div>
  return <div style={{height,width:'100%'}}><ResponsiveContainer width="100%" height="100%">
    <LineChart data={data.filter((_,i)=>data.length<220||i%3===0)} margin={{top:15,left:-10,right:8,bottom:6}}>
      <CartesianGrid stroke="#284057" strokeDasharray="3 7" vertical={false}/>
      <XAxis dataKey={x} axisLine={false} tickLine={false} minTickGap={24} tick={{fontSize:10,fill:'#83a1b9'}}
        tickFormatter={x==='time'?(t)=>t?new Date(t).toLocaleDateString('en-GB',{day:'2-digit',month:'short'}):'':undefined}/>
      <YAxis yAxisId="left" axisLine={false} tickLine={false} tick={{fontSize:10,fill:'#83a1b9'}} width={46}/>
      {series.some(s=>s.right)&&<YAxis yAxisId="right" orientation="right" axisLine={false} tickLine={false} tick={{fontSize:10,fill:'#83a1b9'}} width={46}/>}
      <Tooltip contentStyle={{background:'#0c2032',border:'1px solid #2e5470',borderRadius:10,color:'#deeff9'}}/>
      <Legend wrapperStyle={{fontSize:11}}/>
      {reference!==undefined&&<ReferenceLine yAxisId="left" y={reference} stroke="#e9b67a" strokeDasharray="4 4"/>}
      {series.map((s,i)=><Line key={s.key} dataKey={s.key} name={s.title} yAxisId={s.right?'right':'left'}
        stroke={colors[i%colors.length]} strokeWidth={2.2} dot={false} type="monotone" isAnimationActive={false}/>)}
    </LineChart>
  </ResponsiveContainer></div>
}
function Loading({state}){return <div className="empty">{state.loading?'Fetching mission data…':state.error||'No records'}</div>}
function Overview({orbit,weather,tele,rocket,navigate}){
  return <><div className="hero"><div className="hero-copy"><div className="hero-label">● SYSTEMS INITIALIZED <span>EDUCATIONAL DIGITAL TWIN / V1.0</span></div>
    <p className="eyebrow">ASTRASENTINEL / MISSION INTELLIGENCE</p>
    <h1>See the mission.<br/><em>Understand the signal.</em></h1>
    <p>Explore public orbital measurements, synthetic telemetry intelligence and launch physics in one connected aerospace research workspace.</p>
    <div className="actions"><button className="primary" onClick={()=>navigate('orbit')}>Explore 3D Orbit <Orbit size={17}/></button>
      <button className="secondary" onClick={()=>navigate('telemetry')}>Inspect AI Model <Activity size={16}/></button></div></div>
    <div className="planet-art"><div className="orbital-ring a"/><div className="orbital-ring b"/><div className="planet"/><span>✦</span></div></div>
    <div className="metrics">
      <Metric icon={Satellite} label="Tracked Satellite" value="ISS / 25544" sub={orbit?.source||'Awaiting data'}/>
      <Metric icon={Orbit} label="Est. Orbital Altitude" value={orbit?.points?orbit.points[60].altitude_km+' km':'—'} sub="SGP4 estimated position" color={1}/>
      <Metric icon={Waves} label="Planetary Kp Index" value={weather?.latest_kp} sub={weather?.status==='demo'?'Synthetic demo':'NOAA observation'} color={3}/>
      <Metric icon={ShieldAlert} label="AI Anomaly Flags" value={tele?.records.filter(p=>p.anomaly).length} sub="Synthetic telemetry detections" color={2}/>
    </div>
    <div className="two-col"><Panel title="Orbital mechanics" icon={Orbit}><div className="kv">
      <p>Propagation algorithm <strong>SGP4</strong></p><p>Orbital period <strong>{orbit?.period_minutes??'—'} minutes</strong></p>
      <p>Inclination <strong>{orbit?.inclination_deg??'—'}°</strong></p><p>Source state <strong>{orbit?.status??'—'}</strong></p></div>
      <button className="link-button" onClick={()=>navigate('orbit')}>Open 3D Earth viewer →</button></Panel>
      <Panel title="Machine learning evaluation" icon={Cpu}><div className="kv">
      <p>Detector <strong>Isolation Forest</strong></p><p>Training samples <strong>{tele?.model_metrics.training_samples??'—'}</strong></p>
      <p>Synthetic precision <strong>{tele?.model_metrics?Math.round(tele.model_metrics.precision*100)+'%':'—'}</strong></p>
      <p>Synthetic recall <strong>{tele?.model_metrics?Math.round(tele.model_metrics.recall*100)+'%':'—'}</strong></p></div>
      <button className="link-button" onClick={()=>navigate('telemetry')}>Investigate telemetry events →</button></Panel></div>
    <div className="two-col"><Panel title="Space weather observations" icon={CloudSun}>
      <div className="big-stat">{weather?.latest_kp??'—'} <div><strong>Latest Kp index</strong><span>{weather?.level||'Awaiting NOAA source'}</span></div></div>
      {weather&&<Source source={weather.source} age={weather.age_hours} status={weather.status}/>}
      <button className="link-button" onClick={()=>navigate('weather')}>Inspect geomagnetic timeline →</button></Panel>
    <Panel title="Rocket trajectory preview" icon={Rocket}><div className="kv">
      <p>Simulated apogee <strong>{rocket?.metrics.apogee_km??'—'} km</strong></p>
      <p>Maximum ascent velocity <strong>{rocket?.metrics.peak_velocity_m_s??'—'} m/s</strong></p>
      <p>Maximum dynamic pressure <strong>{rocket?.metrics.max_dynamic_pressure_pa??'—'} Pa</strong></p>
      <p>Trajectory model <strong>1D / variable mass</strong></p></div>
      <button className="link-button" onClick={()=>navigate('rocket')}>Launch simulation laboratory →</button></Panel></div>
    <MissionExportPanel orbit={orbit} telemetry={tele} rocket={rocket}/>
  </>
}
function OrbitPage({state}){
  const d=state.data;return <><Header eyebrow="MODULE 01 / ASTRODYNAMICS" title="Orbital Explorer"
    desc="CelesTrak orbital elements · SGP4 propagation · interactive 3D Earth" badge="3D ORBIT VIEWER"/>
    {d?<><Source source={d.source} age={d.elements_age_hours} status={d.status}/>
      <div className="orbit-grid"><OrbitGlobe orbit={d}/><div className="rightpanels">
        <Panel title="Orbital elements" icon={Satellite}><div className="kv">
          <p>NORAD ID <strong>{d.catalog_id}</strong></p><p>Object <strong>{d.name}</strong></p>
          <p>Inclination <strong>{d.inclination_deg}°</strong></p><p>Period <strong>{d.period_minutes} min</strong></p>
          <p>Element epoch <strong>{new Date(d.epoch).toLocaleDateString()}</strong></p>
          <p>Samples <strong>{d.points.length}</strong></p></div></Panel>
        <Panel title="Coordinate reference" icon={Earth}><p className="details">{d.frame}. Geographical boundaries on the globe are stylized. No precision geodesy, prediction of collisions or maneuver guidance is implied.</p>
          <a className="external" href={d.source_url} target="_blank" rel="noreferrer">CelesTrak GP data ↗</a></Panel>
      </div></div>
      <Panel title="Estimated altitude trajectory" icon={ChartNoAxesCombined}><Plot data={d.points.map((p,i)=>({...p,sample:i}))} x="sample"
        series={[{key:'altitude_km',title:'Altitude (km)'}]}/></Panel></>:<Loading state={state}/>}
    </>
}
function TelemetryPage({state}){
  const d=state.data
  const [values,setValues]=useState({battery_voltage_v:28,temperature_c:22,bus_current_a:2.8,attitude_error_deg:.5})
  const [result,setResult]=useState(null),[error,setError]=useState(''),[busy,setBusy]=useState(false)
  async function submit(e){e.preventDefault();setBusy(true);setError('')
    try{setResult(await api('/telemetry/score',{method:'POST',body:JSON.stringify(values)}))}
    catch(err){setError(err.message)}finally{setBusy(false)}}
  return <><Header eyebrow="MODULE 02 / ANOMALY AI" title="Satellite Health Intelligence"
    desc="Seeded synthetic telemetry · Isolation Forest · interpretable feature deviations" badge="SYNTHETIC DATA"/>
    {d?<><div className="metrics">
      <Metric icon={Cpu} label="Anomaly Model" value="IsolationForest" sub="120 trees · random seed 42" color={3}/>
      <Metric icon={Database} label="Training Samples" value={d.model_metrics.training_samples} sub="Simulated normal conditions"/>
      <Metric icon={TrendingUp} label="Synthetic Precision" value={Math.round(d.model_metrics.precision*100)+'%'} sub="Controlled synthetic injections" color={1}/>
      <Metric icon={ShieldAlert} label="False Alarm Rate" value={(d.model_metrics.false_alarm_rate*100).toFixed(1)+'%'} sub="Held-out synthetic cases" color={2}/>
    </div>
    <Panel title="Battery voltage and temperature" icon={Activity}><Plot data={d.records.map(r=>({time:r.time,...r.measurements}))}
      series={[{key:'battery_voltage_v',title:'Battery voltage (V)'},{key:'temperature_c',title:'Temperature (°C)',right:true}]}/></Panel>
    <div className="two-col"><Panel title="Detected anomaly events" icon={ShieldAlert}>
      <div className="table-scroll"><table><thead><tr><th>UTC Time</th><th>Score</th><th>Lead deviation</th></tr></thead><tbody>
      {d.records.filter(r=>r.anomaly).slice(0,12).map((r,i)=><tr key={i}><td>{new Date(r.time).toLocaleTimeString()}</td><td className="warning-text">{r.anomaly_score}</td><td>{r.leading_deviation} · {r.deviation_z}σ</td></tr>)}
      </tbody></table></div><p className="details">Scores are negative decision functions, not calibrated probabilities. Leading z-score is a diagnostic rather than a causal explanation.</p>
    </Panel><Panel title="Score a hypothetical telemetry sample" icon={SlidersHorizontal}>
      <form className="form" onSubmit={submit}>{Object.entries(values).map(([key,val])=><label key={key}>{key.replaceAll('_',' ')}
        <input required type="number" step="any" value={val} onChange={e=>setValues({...values,[key]:Number(e.target.value)})}/></label>)}
        <button type="submit" className="primary" disabled={busy}>{busy?'Evaluating…':'Run anomaly detector'} <Zap size={15}/></button></form>
      {result&&<div className="result"><Pill demo={result.anomaly}>{result.anomaly?'ANOMALOUS':'BASELINE-LIKE'}</Pill>
        <p>Score: <b>{result.anomaly_score}</b></p><p>Leading deviation: <b>{result.leading_deviation} ({result.deviation_z}σ)</b></p></div>}
      {error&&<div className="error">{error}</div>}</Panel></div>
    <Panel title="Evaluation transparency" icon={Sparkles}><p className="details">All training and evaluation records are synthetically generated with fixed random seeds. Precision, recall and false-alarm rates measure performance ONLY on synthetic injected anomalies. The model is not calibrated for real spacecraft fault detection.</p>
      <span className="evaluation">TP {d.model_metrics.confusion_matrix.tp} · FP {d.model_metrics.confusion_matrix.fp} · FN {d.model_metrics.confusion_matrix.fn} · TN {d.model_metrics.confusion_matrix.tn}</span></Panel>
    </>:<Loading state={state}/>}</>
}
function WeatherPage({state}){
  const d=state.data
  return <><Header eyebrow="MODULE 03 / HELIOPHYSICS" title="Space Weather Observatory"
    desc="NOAA SWPC planetary K-index time series · explicit data freshness" badge="GEOMAGNETIC READINGS"/>
    {d?<><Source source={d.source} age={d.age_hours} status={d.status}/>
      <div className="two-col"><Panel title="Current observation" icon={Waves}>
        <div className="weather-stat">{d.latest_kp}<div><strong>Planetary Kp</strong><span>{d.level}</span></div></div>
        <p className="details">{d.status==='demo'?'Synthetic historical example (NOT a current NOAA observation)':'Most recent NOAA reading, subject to reporting delay.'}</p>
      </Panel><Panel title="Interpretation" icon={CloudSun}><p className="details">Kp is a global geomagnetic activity index on a scale of 0–9. Geomagnetic storm conditions begin at Kp 5. These observations are not a spacecraft-specific radiation measurement or a failure prediction.</p>
        <div className="scale">{Array.from({length:10},(_,i)=><span key={i} style={{background:i>=7?'#b96f86':i>=5?'#d5a36a':i>=4?'#779f9b':'#347c8d'}}>{i}</span>)}</div>
        <a className="external" href={d.source_url} target="_blank" rel="noreferrer">NOAA SWPC source ↗</a></Panel></div>
      <Panel title="Planetary Kp observation timeline" icon={ChartNoAxesCombined}><Plot data={d.points}
        series={[{key:'kp',title:'Kp index'}]} reference={5} height={330}/></Panel>
      <p className="disclaimer">NOAA data may be provisional or delayed. No satellite-specific risk probability is inferred.</p>
    </>:<Loading state={state}/>}</>
}
function RocketPage({state}){
  const defaults={dry_mass_kg:480,propellant_kg:900,thrust_n:30000,burn_time_s:60,
    drag_coefficient:.42,area_m2:1,density_multiplier:1,duration_s:420,dt_s:.2}
  const [values,setValues]=useState(defaults)
  const [result,setResult]=useState(null),[error,setError]=useState(''),[busy,setBusy]=useState(false)
  const d=result||state.data
  async function submit(e){e.preventDefault();setBusy(true);setError('')
    try{setResult(await api('/rocket',{method:'POST',body:JSON.stringify(values)}))}
    catch(err){setError(err.message)}finally{setBusy(false)}}
  return <><Header eyebrow="MODULE 04 / FLIGHT PHYSICS" title="Rocket Trajectory Laboratory"
    desc="Educational vertical ascent model · variable mass · gravity · atmospheric drag" badge="NOT FLIGHT CERTIFIED"/>
    <div className="rocket-grid"><Panel title="Launch scenario" icon={SlidersHorizontal}>
      <form className="form" onSubmit={submit}>{Object.entries(values).map(([key,val])=><label key={key}>{key.replaceAll('_',' ')}
        <input type="number" min="0" step="any" required value={val} onChange={e=>setValues({...values,[key]:Number(e.target.value)})}/></label>)}
        <button type="submit" className="primary" disabled={busy}>{busy?'Calculating…':'Run trajectory simulation'} <Rocket size={16}/></button></form>
      {error&&<div className="error">{error}</div>}</Panel>
    <div><div className="triple">
      <Metric icon={TrendingUp} label="Simulated Apogee" value={d?d.metrics.apogee_km+' km':null} sub="Maximum altitude"/>
      <Metric icon={Zap} label="Peak Speed" value={d?d.metrics.peak_velocity_m_s+' m/s':null} sub="Vertical velocity" color={1}/>
      <Metric icon={Waves} label="Max Dynamic Pressure" value={d?Math.round(d.metrics.max_dynamic_pressure_pa)+' Pa':null} sub="Estimated maximum Q" color={2}/>
    </div><Panel title="Altitude vs mission time" icon={ChartNoAxesCombined}>
      {d?<Plot data={d.points} x="time_s" series={[{key:'altitude_km',title:'Altitude (km)'}]}/>:<Loading state={state}/>}</Panel>
    <Panel title="Velocity and aerodynamic loading" icon={Activity}>
      {d?<Plot data={d.points} x="time_s" series={[{key:'velocity_m_s',title:'Velocity (m/s)'},{key:'dynamic_pressure_pa',title:'Dynamic pressure (Pa)',right:true}]}/>:<Loading state={state}/>}</Panel>
    </div></div><p className="disclaimer">1D point-mass ascent with a fixed exponential atmosphere and semi-implicit Euler solver. It excludes winds, launch guidance, steering losses, staging and high-fidelity atmosphere models. This is NOT a design or certification tool.</p>
  </>
}
function ArchitecturePage(){
  const layers=[['SOURCE LAYER','CelesTrak GP / NOAA SWPC / synthetic telemetry',Radio],
    ['PHYSICS LAYER','SGP4 / approximate ECEF / exponential atmosphere / ascent integrator',Atom],
    ['AI INTELLIGENCE','IsolationForest / z-score diagnostics / synthetic evaluation',Cpu],
    ['SERVICE INTERFACE','FastAPI HTTP JSON / bounded input validation / data-source flags',Database],
    ['MISSION DASHBOARD','React / Three.js WebGL globe / chart visualizations',Earth],
    ['QUALITY GATES','pytest / offline fixtures / GitHub Actions / Docker',ShieldAlert]]
  return <><Header eyebrow="MODULE 05 / ENGINEERING" title="System Architecture"
    desc="Modular service boundaries, explainable models, source provenance and reproducible tests" badge="ENGINEERING WORKFLOW"/>
    <div className="architecture">{layers.map(([title,desc,Icon],i)=><React.Fragment key={title}>
      <div className="architecture-row"><div><Icon size={21}/><b>{title}</b></div><span>{desc}</span></div>
      {i<layers.length-1&&<div className="architecture-arrow">↓ VALIDATED SCIENCE DATA ↓</div>}
    </React.Fragment>)}</div>
    <div className="two-col"><Panel title="Deep-dive documentation" icon={GitBranch}>
      <div className="doc-links">{['ARCHITECTURE','DATA_SOURCES','PHYSICS','MODEL_CARD','DEMO_GUIDE','TEST_PLAN','LIMITATIONS'].map(name=>
        <a key={name} target="_blank" rel="noreferrer" href={'https://github.com/harshakavali81-collab/AstraSentinel-AI/blob/main/docs/'+name+'.md'}>{name.replaceAll('_',' ')} ↗</a>)}</div>
      </Panel><Panel title="Scientific integrity" icon={Sparkles}><p className="details">Public orbital elements are estimates, not telemetry. Satellite health data is synthetic. Visualized coordinates are approximate. Physics simulations are educational, and AstraSentinel AI is not an official space-agency service.</p></Panel></div>
  </>
}
export default function App(){
  const [page,setPage]=useState('overview'),[refresh,setRefresh]=useState(0)
  const orbit=useEndpoint('/orbit',refresh),weather=useEndpoint('/weather',refresh)
  const tele=useEndpoint('/telemetry',refresh),rocket=useEndpoint('/rocket/demo',refresh)
  const atmosphere=useEndpoint('/atmosphere',refresh)
  const hasError=[orbit,weather,tele,rocket].some(s=>s.error)
  return <div className="shell"><aside className="sidebar"><div className="brand"><div className="brand-icon"><Orbit size={25}/></div>
    <div><b>ASTRA<span>SENTINEL</span></b><small>MISSION INTELLIGENCE</small></div></div>
    <p className="nav-caption">CONTROL CENTER</p><nav>{nav.map(([id,label,Icon])=><button key={id}
      onClick={()=>setPage(id)} className={'nav-item '+(page===id?'active':'')}><Icon size={19}/><span>{label}</span></button>)}</nav>
    <div className="sidebar-footer"><p><i className="live-dot"/> SIMULATION ENVIRONMENT</p><span>Educational science only.<br/>No operational spacecraft access.</span>
      <a target="_blank" rel="noreferrer" href="https://github.com/harshakavali81-collab/AstraSentinel-AI">VIEW GITHUB REPOSITORY ↗</a></div>
    </aside><main className="main"><header className="topbar"><div><span>ASTRASENTINEL</span><em>/</em><strong>{nav.find(n=>n[0]===page)?.[1]}</strong></div>
      <div><Pill demo={hasError}>{hasError?'SOME SOURCES UNAVAILABLE':'MISSION CONSOLE'}</Pill>
        <button title="Refresh data" className="refresh" onClick={()=>setRefresh(v=>v+1)}><RefreshCw size={17}/></button></div></header>
    <div className="content">
      {page==='overview'&&<Overview orbit={orbit.data} weather={weather.data} tele={tele.data} rocket={rocket.data} navigate={setPage}/>}
      {page==='orbit'&&<OrbitPage state={orbit}/>}
      {page==='telemetry'&&<TelemetryPage state={tele}/>}
      {page==='weather'&&<WeatherPage state={weather}/>}
      {page==='rocket'&&<RocketPage state={rocket}/>} 
      {page==='atmosphere'&&<AtmospherePage state={atmosphere}/>}
      {page==='architecture'&&<ArchitecturePage/>}
    </div><footer>ASTRASENTINEL AI © 2026 · EDUCATIONAL DIGITAL TWIN <span>ORBIT ≠ GROUND TRUTH · MODEL SCORE ≠ RISK PROBABILITY</span></footer>
    </main></div>
}
