import React, {useMemo} from 'react'
import {TRACK_BOUNDS, groundProject, splitAtDateline} from './groundTrack.js'

const B = TRACK_BOUNDS
const w = B.width - B.left - B.right
const h = B.height - B.top - B.bottom

export default function GroundTrack({points=[],source='—',status='demo'}) {
  const segments = useMemo(() => splitAtDateline(points), [points])
  const valid = segments.reduce((sum,s) => sum + s.length, 0)
  const first = segments[0]?.[0]
  const last = segments[segments.length-1]?.at(-1)

  return <div className="ground-track">
    <p className="details">Equirectangular coordinate grid using calculated orbital samples.
      Each sample is projected from the approximate SGP4-derived Earth-fixed position;
      no geographical coastline or precision geodesy is implied. Antimeridian wraps are split.</p>
    <svg viewBox={'0 0 '+B.width+' '+B.height} role="img" aria-label="Actual modeled ISS ground track by estimated longitude and latitude; no coastline is depicted">
      <rect x={B.left} y={B.top} width={w} height={h} fill="#091b2d" stroke="#365671"/>
      {[-180,-120,-60,0,60,120,180].map(lon => {
        const [x] = groundProject(lon,0)
        return <g key={lon}>
          <line x1={x} y1={B.top} x2={x} y2={B.top+h}
            stroke={lon===0?'#50778e':'#27435c'} strokeDasharray={lon===0?'0':'5 8'}/>
          <text x={x} y={B.top+h+20} textAnchor="middle" fill="#9cb6c5" fontSize="12">{lon}°</text>
        </g>
      })}
      {[-90,-60,-30,0,30,60,90].map(lat => {
        const [,y] = groundProject(0,lat)
        return <g key={lat}>
          <line x1={B.left} y1={y} x2={B.left+w} y2={y}
            stroke={lat===0?'#50778e':'#27435c'} strokeDasharray={lat===0?'0':'5 8'}/>
          <text x={B.left-11} y={y+4} textAnchor="end" fill="#9cb6c5" fontSize="12">{lat}°</text>
        </g>
      })}
      {segments.map((s,i) => <polyline key={i} fill="none" stroke="#6ce9d2" strokeWidth="3"
        strokeLinecap="round" strokeLinejoin="round" points={s.map(p=>p.x+','+p.y).join(' ')}/>)}
      {first&&<g><circle cx={first.x} cy={first.y} r="7" fill="#75d7ff" stroke="#e0fcff" strokeWidth="2"/>
        <title>{'Start: '+first.time}</title></g>}
      {last&&<g><circle cx={last.x} cy={last.y} r="7" fill="#ffb36a" stroke="#fff2d1" strokeWidth="2"/>
        <title>{'End: '+last.time}</title></g>}
      <text x={B.left+w/2} y={B.height-8} textAnchor="middle" fill="#82a6bd" fontSize="12">Longitude (degrees)</text>
      <text transform={'translate(15 '+(B.top+h/2)+') rotate(-90)'} textAnchor="middle"
        fill="#82a6bd" fontSize="12">Latitude (degrees)</text>
    </svg>
    <div className="ground-legend">
      <span><i className="sampled"/> Computed orbital samples: {valid}</span>
      <span><i className="ground-start"/> Start</span>
      <span><i className="ground-end"/> End</span>
      <span>{source} · {status==='demo'?'Historical demo TLE':status==='stale'?'Stale public TLE':'Public orbital elements'}</span>
    </div>
  </div>
}
