import React,{useMemo,useState} from 'react'
import {Canvas} from '@react-three/fiber'
import {OrbitControls,Line,Stars} from '@react-three/drei'
import * as THREE from 'three'

const R=3.35, SCALE=R/6378.137
function GlobeTexture(){
  return useMemo(()=>{
    const c=document.createElement('canvas');c.width=1024;c.height=512
    const x=c.getContext('2d')
    const g=x.createLinearGradient(0,0,1024,512)
    g.addColorStop(0,'#1b6487');g.addColorStop(.6,'#10416c');g.addColorStop(1,'#071c37')
    x.fillStyle=g;x.fillRect(0,0,1024,512)
    // Stylized geography is decorative, not a georeferenced Earth basemap.
    const land=[
      [[110,95],[190,71],[257,93],[289,132],[269,196],[230,237],[172,216],[133,173]],
      [[259,239],[306,246],[353,303],[325,392],[291,457],[271,365]],
      [[455,122],[512,87],[602,110],[626,150],[587,193],[532,183],[494,219]],
      [[508,207],[580,197],[619,263],[606,333],[574,382],[541,348]],
      [[630,120],[724,69],[861,103],[915,161],[862,237],[751,255],[681,211]],
      [[819,315],[885,306],[933,340],[911,388],[849,405]]]
    for(const p of land){x.beginPath();p.forEach(([a,b],i)=>i?x.lineTo(a,b):x.moveTo(a,b));x.closePath()
      x.fillStyle='#247560';x.fill();x.strokeStyle='#40a48d';x.lineWidth=2;x.stroke()}
    for(let i=0;i<100;i++){let xx=(i*173+47)%1024,yy=(i*89+27)%512
      x.fillStyle='rgba(220,250,255,0.09)';x.beginPath()
      x.ellipse(xx,yy,15+(i%8)*5,3+(i%4),-.17,0,6.283);x.fill()}
    const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t
  },[])
}
function Scene({orbit,index}){
  const texture=GlobeTexture()
  const points=useMemo(()=>(orbit?.points||[]).map(p=>p.ecef_km.map(v=>v*SCALE)),[orbit])
  const current=points[index]||[0,0,R+.25]
  return <>
    <color attach="background" args={['#030c1b']}/>
    <ambientLight intensity={.65}/>
    <directionalLight position={[8,5,7]} intensity={2.1} color="#d6edff"/>
    <Stars radius={100} depth={50} count={2400} factor={3} saturation={0} fade speed={0}/>
    <mesh rotation={[0,-Math.PI/2,0]}><sphereGeometry args={[R,96,64]}/>
      <meshPhongMaterial map={texture} emissive="#081d36" emissiveIntensity={.23}/></mesh>
    <mesh><sphereGeometry args={[R+.11,64,40]}/>
      <meshBasicMaterial color="#51b6ff" transparent opacity={.13} side={THREE.BackSide} depthWrite={false}/></mesh>
    <mesh><sphereGeometry args={[R+.24,64,40]}/>
      <meshBasicMaterial color="#2687ec" transparent opacity={.045} side={THREE.BackSide} depthWrite={false}/></mesh>
    {points.length>1&&<Line points={points} color="#76f9dd" lineWidth={2.2}/>}
    <mesh position={current}><sphereGeometry args={[.10,24,24]}/><meshBasicMaterial color="#b3fff2"/></mesh>
    <mesh position={current}><sphereGeometry args={[.22,24,24]}/><meshBasicMaterial color="#7eeae3" transparent opacity={.18}/></mesh>
    <OrbitControls enablePan={false} minDistance={5.5} maxDistance={17}/>
  </>
}
export default function OrbitGlobe({orbit}){
  const [index,setIndex]=useState(60)
  const point=orbit?.points?.[index]
  return <section className="globe">
    <header className="globe-head"><strong>◎ 3D EARTH / INTERACTIVE ORBIT</strong><span>DRAG TO ROTATE · SCROLL TO ZOOM</span></header>
    <div className="globe-stage"><Canvas dpr={[1,1.8]} camera={{position:[5.4,4.2,9],fov:44}}><Scene orbit={orbit} index={index}/></Canvas>
      <div className="globe-caption">SGP4 · TEME TO APPROX. ECEF · NOT A PRECISION BASEMAP</div></div>
    <div className="scrubber"><div className="scrub-head"><span>MISSION TIME SCRUBBER</span><strong>{point?new Date(point.time).toLocaleString():'—'}</strong></div>
      <input aria-label="Mission time scrubber" type="range" min="0" max={Math.max(0,(orbit?.points?.length||1)-1)} value={index} onChange={e=>setIndex(Number(e.target.value))}/>
      <div className="scrub-stats"><span>ALTITUDE <b>{point?.altitude_km??'—'} km</b></span><span>LATITUDE <b>{point?.latitude_deg??'—'}°</b></span><span>LONGITUDE <b>{point?.longitude_deg??'—'}°</b></span></div>
    </div>
  </section>
}
