export async function api(path,init) {
  const response=await fetch('/api'+path,{...init,headers:{'Content-Type':'application/json',...(init?.headers||{})}})
  if(!response.ok){const detail=await response.text();throw Error('API '+response.status+': '+detail.slice(0,240))}
  return response.json()
}
