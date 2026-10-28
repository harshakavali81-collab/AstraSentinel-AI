import test from 'node:test'
import assert from 'node:assert/strict'
import {groundProject, splitAtDateline, TRACK_BOUNDS} from '../src/groundTrack.js'

test('projects validated geographic degrees onto a bounded equirectangular plot', () => {
  const a = groundProject(-180, 90), b = groundProject(180, -90)
  assert.deepEqual(a, [TRACK_BOUNDS.left, TRACK_BOUNDS.top])
  assert.deepEqual(b, [TRACK_BOUNDS.width - TRACK_BOUNDS.right,
                       TRACK_BOUNDS.height - TRACK_BOUNDS.bottom])
  const mid = groundProject(0,0)
  assert.equal(mid[0], (a[0]+b[0])/2)
  assert.equal(mid[1], (a[1]+b[1])/2)
  assert.throws(()=>groundProject(190,20),RangeError)
  assert.throws(()=>groundProject(-10,91),RangeError)
  assert.throws(()=>groundProject(NaN,30),RangeError)
})

test('splits dateline crossing instead of drawing across the entire map',()=>{
  const sample = [
    {time:'t1',longitude_deg:174, latitude_deg:2},
    {time:'t2',longitude_deg:179, latitude_deg:4},
    {time:'t3',longitude_deg:-178,latitude_deg:5},
    {time:'t4',longitude_deg:-175,latitude_deg:6},
  ]
  const segments=splitAtDateline(sample)
  assert.equal(segments.length,2)
  assert.deepEqual(segments.map(s=>s.length),[2,2])
  assert.equal(segments[0][0].longitude_deg,174)
  assert.equal(segments[1][0].longitude_deg,-178)
})

test('normal point sequences remain in one segment',()=>{
  const segments=splitAtDateline([
    {time:'t1',longitude_deg:10, latitude_deg:0},
    {time:'t2',longitude_deg:12, latitude_deg:3},
  ])
  assert.equal(segments.length,1)
  assert.deepEqual(splitAtDateline([]),[])
})
