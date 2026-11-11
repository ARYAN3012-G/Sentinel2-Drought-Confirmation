// =============================================================================
// SCRIPT A — Find farmland automatically and split it into field segments
// Drought project, satellite module (weather -> SATELLITE -> UAV)
// Paste into https://code.earthengine.google.com and press Run.
// =============================================================================
// Steps
//  1. 3 km circle around each study area. Where circles overlap, each pixel
//     goes to the nearest area centre (nothing is counted twice).
//  2. Keep cropland in ESA WorldCover (2020 or 2021).
//  3. Remove pixels Dynamic World calls "built" in any year 2019-2023, mostly
//     "trees", or "water" in more than one year (houses, roads, orchards, tank beds).
//  4. Keep pixels whose Sentinel-2 NDVI shows a crop cycle (green-up and
//     dry-down) in at least 2 of 5 years (removes scrub and wasteland, but keeps
//     fields that failed in drought years).
//  5. Remove edge pixels (touching non-farmland).
//  6. Mark likely irrigated pixels (green in summer Mar-May, no rain then).
//  7. Split farmland into field-sized segments (SNIC), keep 0.3-10 ha.
//  8. Random sample per site: up to 20 rainfed + 10 irrigated segments.
// Outputs (Tasks tab -> RUN each):
//  A_site_cropland_stats   CSV      hectares left after each step, per site
//  A_field_segments_drive     GeoJSON  field_segments_v2.geojson: all segments (sampled = 1)
//                                      -> python tools/make_sampled_upload.py -> upload as
//                                         asset sampled_fields_v2 (used by script B)
//  A_cropland_mask_v2_asset   Asset    farmland mask (site id, irrigated), used by script B
// =============================================================================

// ---- 0. SETTINGS -------------------------------------------------------------
// Change ASSET_ROOT to your own: open the "Assets" tab (top left); the path shown
// above your assets looks like  projects/<your-project>/assets
var ASSET_ROOT = 'projects/serverchat-489517/assets';

var RADIUS_M        = 3000;
// v2: TRAINING years only (2019-2023), so the farmland mask, field boundaries and irrigation
// flag never use validation/test imagery (2024-2026).
var YEARS           = [2019, 2020, 2021, 2022, 2023];
// Dynamic World is used only to REMOVE non-farm land. Requiring "crops" in most
// years dropped dry rainfed fields (Dynamic World often calls them bare/scrub).
var MAX_TREE_YEARS  = 2;     // remove pixels whose top class is trees in > 2 of 5 years
var MAX_WATER_YEARS = 1;     // remove pixels whose top class is water in > 1 year
// Crop cycle needed in only 2 of 5 years: requiring most years removed fields
// that failed in drought years, i.e. exactly the fields this study needs.
var MIN_CYCLE_YEARS = 2;
var CYCLE_PEAK      = 0.35;  // yearly NDVI 90th percentile above this ...
var CYCLE_AMPLITUDE = 0.15;  // ... and 90th minus 10th percentile above this
var IRRIG_NDVI      = 0.40;  // summer (Mar-May) NDVI 75th percentile above this ...
var IRRIG_YEARS     = 2;     // ... in >= 2 of 5 years -> likely irrigated
var CLOUD_CS        = 0.60;  // Cloud Score+ clear-sky threshold (higher = stricter)
var SNIC_SIZE       = 8;     // segment seed spacing in pixels (8 x 10 m = 80 m)
var MIN_PIX = 30, MAX_PIX = 1000;   // segment size 0.3-10 ha (1 pixel = 0.01 ha)
var N_RAINFED = 20, N_IRRIG = 10, SEED = 42;
var CRS = 'EPSG:32643', SCALE = 10;

// Area centres (from study_sites_google_earth.kml). weather = site name in the
// weather module; Lepakshi shares Cholasamudram's ERA5-Land cell.
var SITES = [
  // centres = where the field data were collected (UAV survey); Somandepalle = drone photo
  // centre in Tungodu village (the dataset table's 13.799997 N is a copy of the Lepakshi point)
  {code: 'Som',  name: 'Somandepalle',            lat: 13.9988, lon: 77.6247, weather: 'Somandepalle'},
  {code: 'Lep',  name: 'Lepakshi',                lat: 13.7998, lon: 77.6194, weather: 'cholasamudram'},
  {code: 'Cho',  name: 'Cholasamudram',           lat: 13.8118, lon: 77.5687, weather: 'cholasamudram'},
  {code: 'Sira', name: 'Sira',                    lat: 13.7975, lon: 76.9750, weather: 'sira'},
  {code: 'Ped',  name: 'Peddakadubur',            lat: 15.7826, lon: 77.2528, weather: 'Peddakadubur'},
  {code: 'Din',  name: 'Kurnool_Dinnedevarapadu', lat: 15.7715, lon: 78.0471, weather: 'kurnool_dinedevarapadu'},
  {code: 'Bal',  name: 'Kurnool_Balaji_Villas',   lat: 15.7834, lon: 78.0561, weather: 'kurnool_balaji_villas'},
  {code: 'Pul',  name: 'Kurnool_Pullaiah',        lat: 15.7982, lon: 78.0806, weather: 'kurnool_balaji_villas'}
];

// ---- 1. Site circles and nearest-centre split ---------------------------------
var circles = SITES.map(function (s) {
  return ee.Feature(ee.Geometry.Point([s.lon, s.lat]).buffer(RADIUS_M), {site: s.name, site_code: s.code});
});
var circlesFC = ee.FeatureCollection(circles);
var AOI = circlesFC.geometry();

var siteIdx = ee.ImageCollection(SITES.map(function (s, i) {
  var d = ee.FeatureCollection([ee.Feature(ee.Geometry.Point([s.lon, s.lat]))])
            .distance(RADIUS_M + 500);
  return d.multiply(-1).rename('negd')
          .addBands(ee.Image.constant(i).toByte().rename('site'))
          .updateMask(d.lte(RADIUS_M));
})).qualityMosaic('negd').select('site');           // masked outside all circles
var inAOI = siteIdx.mask().gt(0);

// ---- 2. ESA WorldCover cropland (class 40) --------------------------------------
var wc20 = ee.ImageCollection('ESA/WorldCover/v100').first().select('Map');
var wc21 = ee.ImageCollection('ESA/WorldCover/v200').first().select('Map');
var wcCrop = wc20.eq(40).or(wc21.eq(40)).unmask(0);

// ---- 3. Dynamic World: crops in most years, never built ---------------------------
var DW_BANDS = ['water', 'trees', 'grass', 'flooded_vegetation', 'crops',
                'shrub_and_scrub', 'built', 'bare', 'snow_and_ice'];
var dwTop = ee.ImageCollection(YEARS.map(function (y) {
  return ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')
    .filterBounds(AOI).filterDate(y + '-01-01', (y + 1) + '-01-01')
    .select(DW_BANDS).mean()
    .toArray().arrayArgmax().arrayGet([0]).rename('top');
}));
function dwYears(cls) { return dwTop.map(function (im) { return im.eq(cls); }).sum(); }
var dwOK = dwYears(6).eq(0)                       // never built
  .and(dwYears(1).lte(MAX_TREE_YEARS))             // not mostly trees
  .and(dwYears(0).lte(MAX_WATER_YEARS))            // not tank bed / water
  .unmask(0);

// ---- 4. Sentinel-2 crop-cycle check ---------------------------------------------------
var CSP = ee.ImageCollection('GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED');
function s2(start, end) {
  return ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(AOI).filterDate(start, end)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 80))
    .linkCollection(CSP, ['cs_cdf'])
    .map(function (img) {
      var ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI');
      return img.addBands(ndvi).updateMask(img.select('cs_cdf').gte(CLOUD_CS));
    });
}
var cycleYears = ee.ImageCollection(YEARS.map(function (y) {
  var p = s2(y + '-01-01', (y + 1) + '-01-01').select('NDVI')
            .reduce(ee.Reducer.percentile([10, 90]));
  var peak = p.select('NDVI_p90'), amp = peak.subtract(p.select('NDVI_p10'));
  return peak.gt(CYCLE_PEAK).and(amp.gt(CYCLE_AMPLITUDE)).unmask(0);
})).sum();
var cycleOK = cycleYears.gte(MIN_CYCLE_YEARS).unmask(0);

// ---- 5. Combine and remove edge pixels ------------------------------------------------
var beforeEdges = wcCrop.and(dwOK).and(cycleOK).and(inAOI);
var farmland = beforeEdges.unmask(0)
  .reproject({crs: CRS, scale: SCALE})
  .focalMin({radius: 1, kernelType: 'square', units: 'pixels'})
  .and(inAOI);

// ---- 6. Likely irrigated: green in summer (Mar-May) ---------------------------------
var irrigYears = ee.ImageCollection(YEARS.map(function (y) {
  return s2(y + '-03-01', y + '-06-01').select('NDVI')
           .reduce(ee.Reducer.percentile([75])).gt(IRRIG_NDVI).unmask(0);
})).sum();
var irrigated = irrigYears.gte(IRRIG_YEARS).unmask(0);

// ---- 7. Field-sized segments (SNIC) on farmland -------------------------------------
var WINDOWS = [['2021-09-01', '2021-12-01'], ['2022-09-01', '2022-12-01'],
               ['2022-12-01', '2023-03-01'], ['2023-03-01', '2023-06-01'],
               ['2023-09-01', '2023-12-01']];                 // training years only
var feat = ee.Image.cat(WINDOWS.map(function (w, k) {
  return s2(w[0], w[1]).select('NDVI').median().unmask(0).rename('f' + k);
})).updateMask(farmland);
var snic = ee.Algorithms.Image.Segmentation.SNIC({
  image: feat, size: SNIC_SIZE, compactness: 1, connectivity: 8,
  neighborhoodSize: 4 * SNIC_SIZE,
  seeds: ee.Algorithms.Image.Segmentation.seedGrid(SNIC_SIZE)
}).select('clusters').reproject({crs: CRS, scale: SCALE});

function siteSegments(s, i) {
  var m = farmland.and(siteIdx.eq(i).unmask(0));
  var img = snic.addBands(irrigated.toFloat().rename('irrig')).updateMask(m);
  var vec = img.reduceToVectors({
    geometry: circles[i].geometry(), crs: CRS, scale: SCALE,
    geometryType: 'polygon', eightConnected: true, labelProperty: 'label',
    reducer: ee.Reducer.mean().combine({reducer2: ee.Reducer.count(), sharedInputs: true}),
    maxPixels: 1e10
  }).filter(ee.Filter.rangeContains('count', MIN_PIX, MAX_PIX));
  vec = vec.map(function (f) {
    var n = ee.Number(f.get('count')), fr = ee.Number(f.get('mean'));
    var id = ee.String(s.code + '_').cat(ee.Number(f.get('label')).format('%d'))
               .cat('_').cat(n.format('%d'));
    return f.set({field_id: id, site: s.name, site_code: s.code, weather_site: s.weather,
                  pixels: n, area_ha: n.divide(100), irrig_frac: fr, irrigated: fr.gte(0.5)});
  });
  // ---- 8. random sample (fixed seed) ----
  var rain = vec.filter(ee.Filter.eq('irrigated', 0)).randomColumn('r', SEED).sort('r').limit(N_RAINFED);
  var irr  = vec.filter(ee.Filter.eq('irrigated', 1)).randomColumn('r', SEED).sort('r').limit(N_IRRIG);
  var ids = rain.merge(irr).aggregate_array('field_id');
  return vec.map(function (f) {
    return f.set('sampled', ee.Algorithms.If(ids.contains(f.get('field_id')), 1, 0));
  }).select(['field_id', 'site', 'site_code', 'weather_site', 'pixels', 'area_ha',
             'irrig_frac', 'irrigated', 'sampled']);
}
var segments = ee.FeatureCollection(SITES.map(siteSegments)).flatten();

// ---- Per-site statistics ---------------------------------------------------------------
var stats = ee.FeatureCollection(SITES.map(function (s, i) {
  var inSite = siteIdx.eq(i).unmask(0);
  var img = ee.Image.cat([
    inSite,
    inSite.and(wcCrop),
    inSite.and(wcCrop).and(dwOK),
    inSite.and(beforeEdges.unmask(0)),
    inSite.and(farmland),
    inSite.and(farmland).and(irrigated),
    inSite.and(farmland).and(irrigated.not())
  ]).rename(['circle_ha', 'worldcover_ha', 'dynamicworld_ha', 'cropcycle_ha',
             'final_farmland_ha', 'irrigated_ha', 'rainfed_ha'])
    .multiply(ee.Image.pixelArea().divide(1e4));
  // tileScale splits the work into smaller pieces (avoids memory/time-out errors).
  // Segment counts are computed later in Python from field_segments.geojson.
  var sums = img.reduceRegion({reducer: ee.Reducer.sum(), geometry: circles[i].geometry(),
                               crs: CRS, scale: SCALE, maxPixels: 1e10, tileScale: 16});
  return ee.Feature(null, sums).set({
    site: s.name, site_code: s.code, weather_site: s.weather, lat: s.lat, lon: s.lon
  });
}));

// ---- Exports -----------------------------------------------------------------------------
Export.table.toDrive({collection: stats, description: 'A_site_cropland_stats',
  folder: 'drought_satellite', fileNamePrefix: 'site_cropland_stats_v2', fileFormat: 'CSV'});
Export.table.toDrive({collection: segments, description: 'A_field_segments_drive',
  folder: 'drought_satellite', fileNamePrefix: 'field_segments_v2', fileFormat: 'GeoJSON'});
var maskImg = siteIdx.updateMask(farmland).rename('site')
  .addBands(irrigated.toByte().updateMask(farmland).rename('irrigated')).toByte();
Export.image.toAsset({image: maskImg, description: 'A_cropland_mask_v2_asset',
  assetId: ASSET_ROOT + '/cropland_mask_v2', region: AOI.bounds(), crs: CRS, scale: SCALE,
  maxPixels: 1e10});

// ---- Map for visual checking ---------------------------------------------------------
var rgb = s2('2023-10-01', '2023-12-01').median().clip(AOI);
var edges = snic.neq(snic.focalMax(1)).or(snic.neq(snic.focalMin(1))).and(farmland);
// Only the farmland, irrigated and circle layers are on at start (faster loading).
Map.addLayer(rgb, {bands: ['B4', 'B3', 'B2'], min: 0, max: 3000}, 'Sentinel-2 Oct-Nov 2023', false);
Map.addLayer(wcCrop.and(inAOI).selfMask(), {palette: ['orange']}, 'Step 2: WorldCover cropland', false);
Map.addLayer(beforeEdges.selfMask(), {palette: ['ff8800']}, 'Steps 2-4: before edge removal', false);
Map.addLayer(wcCrop.and(inAOI).and(dwOK.not()).selfMask(), {palette: ['ff0000']}, 'Check: removed by Dynamic World', false);
Map.addLayer(wcCrop.and(inAOI).and(dwOK).and(cycleOK.not()).selfMask(), {palette: ['aa00ff']}, 'Check: removed by crop-cycle test', false);
Map.addLayer(farmland.selfMask(), {palette: ['ffff00'], opacity: 0.6}, 'Farmland kept (final)');
Map.addLayer(farmland.and(irrigated).selfMask(), {palette: ['00bfff'], opacity: 0.7}, 'Likely irrigated');
Map.addLayer(edges.selfMask(), {palette: ['ffffff']}, 'Field segment outlines', false);
Map.addLayer(segments.filter(ee.Filter.eq('sampled', 1)), {color: 'ff0000'}, 'Sampled fields (slow)', false);
Map.addLayer(ee.Image().byte().paint(circlesFC, 0, 2), {palette: ['ff0000']}, '3 km circles');

var picker = ui.Select({
  items: SITES.map(function (s) { return s.name; }),
  placeholder: 'Go to site',
  onChange: function (name) {
    var s = SITES.filter(function (x) { return x.name === name; })[0];
    Map.setCenter(s.lon, s.lat, 15);
  }
});
Map.add(ui.Panel([
  ui.Label('Script A: farmland check', {fontWeight: 'bold'}),
  picker,
  ui.Label('Yellow = farmland kept'),
  ui.Label('Blue = likely irrigated'),
  ui.Label('White lines = field segments (turn on in Layers)'),
  ui.Label('Layers load slowly (5 years of data); zoom in on one site.')
], null, {position: 'top-left', width: '230px'}));
Map.setOptions('SATELLITE');
Map.setCenter(SITES[0].lon, SITES[0].lat, 15);
print('Sites:', SITES.length, ' Years:', YEARS);
print('Next: Tasks tab -> RUN all 4 exports.');
