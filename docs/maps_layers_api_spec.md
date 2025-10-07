# Maps Layers API Spec (Frontend Contract)

Endpoint
- GET /api/maps/layers?analysis_id={id}[&layer={name}]

Query Parameters
- analysis_id (required): integer ID returned by /api/analysis/start
- layer (optional): string for layer selection (values suggested):
  - risk, biodiversity, soil, wildlife (align with frontend’s layer dropdown)

Response Formats
The frontend accepts the following JSON structures. You may return one or combine them as needed. The frontend will render in this order of preference based on the user’s View selection (Auto/Heatmap/Markers).

A. GeoJSON FeatureCollection (preferred for polygons/lines)
- Rendered as vector overlays; the map auto-fits to feature bounds
- Optional bbox: [west, south, east, north]

Example:
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": { "type": "Polygon", "coordinates": [[[lng,lat], ...]] },
      "properties": { "risk": "high" }
    }
  ],
  "bbox": [73.5, 18.4, 75.1, 19.2]
}

B. Weighted Heatmap Points (for density/intensity visualization)
- The frontend builds a heatmap when weighted points are provided
- weights are in [0,1], defaults to 0.5 if omitted
- Optional params: heat_radius (25), heat_blur (15), heat_maxZoom (17), heat_max (1.0), heat_gradient (Leaflet.heat gradient object)
- Optional bbox to assist fitting

Accepted keys for weighted points (any one):
- heat, heatmap, heat_points, or points (when each point has weight or intensity)

Example:
{
  "heat": [
    { "lat": 18.527, "lng": 73.856, "weight": 0.9 },
    { "lat": 18.520, "lng": 73.870, "weight": 0.6 }
  ],
  "bbox": [73.84, 18.50, 73.88, 18.54],
  "heat_radius": 30,
  "heat_blur": 18,
  "heat_max": 1.0
}

C. Marker/Circle Points (categorical risk or simple markers)
- Rendered as colored circles when heatmap points are not present or “Markers” view is selected
- Optional radius per point (meters); default 800
- Optional bbox to assist fitting

Example:
{
  "points": [
    { "lat": 18.527, "lng": 73.856, "risk": "high", "radius": 1200 },
    { "lat": 18.520, "lng": 73.870, "risk": "low" }
  ],
  "bbox": [73.84, 18.50, 73.88, 18.54]
}

Rendering Behavior
- Auto (default):
  - If weighted points are present, render heatmap;
  - else if points exist, render markers;
  - else if GeoJSON exists, render as vector layers.
- Heatmap: force heatmap if weighted points are present; otherwise falls back to markers/GeoJSON.
- Markers: force markers even if weighted points exist.
- Previous layers are cleared before rendering; the map fits to computed bounds from the returned data or provided bbox.

Recommendations
- Always include a bbox for faster, accurate fit, especially when data is sparse.
- For performance, keep weighted points to a few thousand max; aggregate server-side if needed.
- Use risk categories: high | medium | low (for consistent marker coloring on the frontend).

Error Responses
- 404 { "error": "Analysis not found" }
- 400 { "error": "Invalid parameters" }
- 500 { "error": "Internal server error" }
