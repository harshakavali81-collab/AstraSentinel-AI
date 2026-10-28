import test from 'node:test'
import assert from 'node:assert/strict'
import {makeComparisonRows} from '../src/scenarioCurves.js'

test('interpolates two independently sampled series on shared axis', () => {
  const rows = makeComparisonRows([
    {id: 'a', curve: [{time_s: 0, altitude_km: 0}, {time_s: 10, altitude_km: 100}]},
    {id: 'b', curve: [{time_s: 0, altitude_km: 0}, {time_s: 4, altitude_km: 12},
                      {time_s: 8, altitude_km: 20}, {time_s: 10, altitude_km: 30}]},
  ], 10)
  assert.equal(rows.length, 11)
  assert.deepEqual(rows[0], {time_s: 0, a: 0, b: 0})
  assert.equal(rows[2].a, 20)
  assert.equal(rows[2].b, 6)
  assert.equal(rows[6].b, 16)
  assert.equal(rows.at(-1).a, 100)
  assert.equal(rows.at(-1).b, 30)
})

test('does not extend a simulation past its actual final sample', () => {
  const rows = makeComparisonRows([
    {id: 'landed_early', curve: [{time_s: 0, altitude_km: 0}, {time_s: 5, altitude_km: 3}]},
    {id: 'later', curve: [{time_s: 0, altitude_km: 0}, {time_s: 10, altitude_km: 9}]},
  ], 10)
  assert.equal(rows[5].landed_early, 3)
  assert.equal(rows[6].landed_early, null)
  assert.equal(rows[8].later, 7.2)
})

test('empty scenario set is safe and requests are bounded', () => {
  assert.deepEqual(makeComparisonRows([]), [])
  assert.throws(() => makeComparisonRows([{id: 'a',curve: []}]), /at least two/)
  assert.throws(() => makeComparisonRows([{id: 'a',curve: [
    {time_s: 0, altitude_km: 0}, {time_s: 0, altitude_km: 1}]}]), /increasing/)
  assert.throws(() => makeComparisonRows([{id: 'a',curve: [
    {time_s: 0, altitude_km: 0}, {time_s: 2, altitude_km: Infinity}]}]), /finite/)
  assert.throws(() => makeComparisonRows([{
    id: 'a', curve: [{time_s: 0, altitude_km: 0}, {time_s: 1, altitude_km: 2}],
  }], 9999), /intervals/)
})
