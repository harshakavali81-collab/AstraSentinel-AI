import React, {useState} from 'react'
import {Download,FileJson,FileSpreadsheet,ShieldCheck} from 'lucide-react'
import {api} from './api.js'

function downloadBlob(name,content,mime){
  const blob=new Blob([content],{type:mime})
  const url=URL.createObjectURL(blob)
  const anchor=document.createElement('a')
  anchor.href=url;anchor.download=name;document.body.appendChild(anchor)
  anchor.click();anchor.remove()
  // Defer revocation slightly to allow the download to start.
  setTimeout(()=>URL.revokeObjectURL(url),1000)
}
function csvEscape(value) {
  const text=String(value??'')
  return '"' + text.replaceAll('"','""') + '"'
}
function toCsv(rows){
  if(!rows?.length)throw Error('No data available for this export')
  const keys=Object.keys(rows[0])
  return [keys.join(','),...rows.map(row=>keys.map(k=>csvEscape(row[k])).join(','))].join('\r\n')+'\r\n'
}
export default function MissionExportPanel({orbit,telemetry,rocket}){
  const [busy,setBusy]=useState(false),[error,setError]=useState('')
  async function missionJson(){
    setBusy(true);setError('')
    try{
      const snapshot=await api('/mission/report')
      downloadBlob('astrasentinel_mission_report.json',
        JSON.stringify(snapshot,null,2)+'\n','application/json;charset=utf-8')
    }catch(err){setError(err.message)}finally{setBusy(false)}
  }
  function exportOrbit(){
    try{
      setError('')
      const rows=orbit.points.map(p=>({
        time_utc:p.time,altitude_km:p.altitude_km,
        latitude_deg:p.latitude_deg,longitude_deg:p.longitude_deg,
        ecef_x_km:p.ecef_km[0],ecef_y_km:p.ecef_km[1],ecef_z_km:p.ecef_km[2]}))
      downloadBlob('astrasentinel_orbit_approximate.csv',
        '# '+orbit.source+'; coordinate frame: '+orbit.frame+'\r\n'+toCsv(rows),'text/csv;charset=utf-8')
    }catch(err){setError(err.message)}
  }
  function exportTelemetry(){
    try{
      setError('')
      const rows=telemetry.records.map(p=>({
        time_utc:p.time,...p.measurements,anomaly:p.anomaly,
        anomaly_score:p.anomaly_score,leading_deviation:p.leading_deviation,
        synthetic_injected:p.synthetic_injected}))
      downloadBlob('astrasentinel_synthetic_telemetry.csv',toCsv(rows),'text/csv;charset=utf-8')
    }catch(err){setError(err.message)}
  }
  function exportRocket(){
    try{
      setError('')
      downloadBlob('astrasentinel_simulated_rocket.csv',toCsv(rocket.points),'text/csv;charset=utf-8')
    }catch(err){setError(err.message)}
  }
  return <section className="panel">
    <h3><Download size={18}/> Mission Reports & Data Exports</h3>
    <p className="details">Export a provenance-aware JSON research snapshot or individual chart datasets for GitHub portfolios, reports and reproducible analysis. Exports preserve simulation and demo labels.</p>
    <div className="export-buttons">
      <button disabled={busy} className="primary" onClick={missionJson}><FileJson size={16}/>{busy?'Preparing…':'Mission JSON Report'}</button>
      <button className="secondary" disabled={!orbit} onClick={exportOrbit}><FileSpreadsheet size={16}/> Orbit CSV</button>
      <button className="secondary" disabled={!telemetry} onClick={exportTelemetry}><FileSpreadsheet size={16}/> Telemetry CSV</button>
      <button className="secondary" disabled={!rocket} onClick={exportRocket}><FileSpreadsheet size={16}/> Rocket CSV</button>
    </div>
    <div className="export-disclaimer"><ShieldCheck size={16}/> Synthetic telemetry and rocket data are not real-world observations. Orbit data may be historical or stale.</div>
    {error&&<p className="error">{error}</p>}
  </section>
}
