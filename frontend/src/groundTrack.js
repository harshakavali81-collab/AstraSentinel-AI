/**
 * Equirectangular latitude/longitude plot of SGP4-derived points.
 * An intentionally blank grid (no coastline) prevents confusing the plot
 * with a precision geodetic world map.
 */
export const TRACK_BOUNDS = Object.freeze({width: 960, height: 430, left: 61, right: 22,
  top: 32, bottom: 48})

export function groundProject(lon, lat, b = TRACK_BOUNDS) {
  if (!Number.isFinite(lon) || !Number.isFinite(lat) || lon < -180 || lon > 180 ||
      lat < -90 || lat > 90) throw new RangeError('Invalid longitude/latitude')
  const w = b.width - b.left - b.right
  const h = b.height - b.top - b.bottom
  return [b.left + (lon + 180) / 360 * w, b.top + (90 - lat) / 180 * h]
}

export function splitAtDateline(points) {
  if (!Array.isArray(points)) return []
  const segments = []
  let current = []
  let previous = null
  for (const p of points) {
    const lon = Number(p.longitude_deg)
    const lat = Number(p.latitude_deg)
    const xy = groundProject(lon, lat)
    // A ±180° wrap must not be drawn as a straight line across the full plot.
    if (previous !== null && Math.abs(lon - previous) > 180 && current.length) {
      segments.push(current)
      current = []
    }
    current.push({time:p.time, longitude_deg:lon, latitude_deg:lat, x:xy[0], y:xy[1]})
    previous = lon
  }
  if (current.length) segments.push(current)
  return segments
}
