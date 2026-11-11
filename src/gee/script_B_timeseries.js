// =============================================================================
// SCRIPT B — Download real Sentinel-2 time series (2019 - Oct 2026)
// Drought project, satellite module. Needs two assets:
//   sampled_fields_v2  the 240 sampled fields (upload src/gee/upload/sampled_fields_v2.zip)
//   cropland_mask_v2   made by script A (bands: site 0-7, irrigated 0/1)
// Paste into https://code.earthengine.google.com, press Run, then
// Tasks tab -> RUN all 4 exports.
// =============================================================================
// Outputs (Google Drive folder drought_satellite):
//  B_field_timeseries.csv  one row per sampled field per clear Sentinel-2 image:
//                          mean reflectance (B2-B12), NDVI, NDMI, EVI, clear pixel count
//  B_zone_timeseries.csv   whole-area farmland per site, rainfed and irrigated
//                          separately (zone = site*2 + irrigated): NDVI, NDMI, clear pixels
//  B_zone_pixels.csv       total farmland pixels per zone (to compute clear fraction)
//  B_uav_points_timeseries.csv  25 m circles at the 10 UAV survey points (same columns + lat, lon)
// Same-day duplicates (one field on two overlapping image tiles) are merged in Python.
// =============================================================================

var ASSET_ROOT = 'projects/serverchat-489517/assets';
var START = '2019-01-01', END = '2026-11-01';
var CLOUD_CS = 0.60;
var CRS = 'EPSG:32643', SCALE = 10;

// Same order as in script A (site index 0-7 in cropland_mask)
var SITE_CODES = ['Som', 'Lep', 'Cho', 'Sira', 'Ped', 'Din', 'Bal', 'Pul'];
var SITE_LONLAT = [[77.6247, 13.9988], [77.6194, 13.7998], [77.5687, 13.8118], [76.9750, 13.7975],
                   [77.2528, 15.7826], [78.0471, 15.7715], [78.0561, 15.7834], [78.0806, 15.7982]];
var AOI = ee.FeatureCollection(SITE_LONLAT.map(function (c) {
  return ee.Feature(ee.Geometry.Point(c).buffer(3000));
})).geometry();

// The 240 sampled fields, uploaded as a shapefile (src/gee/upload/sampled_fields.zip)
var FIELDS = ee.FeatureCollection(ASSET_ROOT + '/sampled_fields_v2');
var MASK = ee.Image(ASSET_ROOT + '/cropland_mask_v2');
var ZONE = MASK.select('site').multiply(2).add(MASK.select('irrigated')).rename('zone');

// ---- Sentinel-2 with Cloud Score+ and SCL cloud/shadow masking ----------------
var CSP = ee.ImageCollection('GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED');
var REFL = ['B2', 'B3', 'B4', 'B5', 'B8', 'B11', 'B12'];
var S2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(AOI).filterDate(START, END)
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 90))
  .linkCollection(CSP, ['cs_cdf'])
  .map(function (img) {
    var scl = img.select('SCL');
    var clear = img.select('cs_cdf').gte(CLOUD_CS)
      .and(scl.neq(1)).and(scl.neq(3)).and(scl.neq(8)).and(scl.neq(9))
      .and(scl.neq(10)).and(scl.neq(11));
    var r = img.select(REFL).divide(10000);
    var ndvi = r.normalizedDifference(['B8', 'B4']).rename('NDVI');
    var ndmi = r.normalizedDifference(['B8', 'B11']).rename('NDMI');
    var evi = r.expression('2.5 * (N - R) / (N + 6 * R - 7.5 * B + 1)',
      {N: r.select('B8'), R: r.select('B4'), B: r.select('B2')}).rename('EVI');
    return r.addBands([ndvi, ndmi, evi]).updateMask(clear)
      .copyProperties(img, ['system:time_start', 'MGRS_TILE', 'CLOUDY_PIXEL_PERCENTAGE']);
  });

// ---- 1. Sampled fields ------------------------------------------------------------
var BANDS = REFL.concat(['NDVI', 'NDMI', 'EVI']);
var fieldRed = ee.Reducer.mean().combine({reducer2: ee.Reducer.count(), sharedInputs: true});
function fieldSeries(fields) {
  return S2.filterBounds(fields.geometry()).map(function (img) {
    var date = img.date().format('YYYY-MM-dd');
    return img.select(BANDS).reduceRegions({
      collection: fields.filterBounds(img.geometry()),
      reducer: fieldRed, crs: CRS, scale: SCALE, tileScale: 2
    }).map(function (f) {
      return f.set({date: date, tile: img.get('MGRS_TILE'),
                    scene_cloud_pct: img.get('CLOUDY_PIXEL_PERCENTAGE')});
    });
  }).flatten().filter(ee.Filter.gt('NDVI_count', 0));
}
var fieldTS = fieldSeries(FIELDS);

var FIELD_COLS = ['date', 'tile', 'scene_cloud_pct', 'field_id', 'site', 'site_code',
                  'weather', 'irrigated', 'area_ha', 'pixels', 'NDVI_count'];
BANDS.forEach(function (b) { FIELD_COLS.push(b + '_mean'); });
Export.table.toDrive({collection: fieldTS, description: 'B_field_timeseries',
  folder: 'drought_satellite', fileNamePrefix: 'B_field_timeseries', fileFormat: 'CSV',
  selectors: FIELD_COLS});

// ---- 2. Whole-area farmland per site (rainfed / irrigated) ---------------------------
function grouped(img, band, withCount) {
  var red = withCount
    ? ee.Reducer.mean().combine({reducer2: ee.Reducer.count(), sharedInputs: true})
    : ee.Reducer.mean();
  var out = img.select(band).addBands(ZONE).reduceRegion({
    reducer: red.group({groupField: 1, groupName: 'zone'}),
    geometry: AOI, crs: CRS, scale: SCALE, maxPixels: 1e10, tileScale: 4
  });
  return ee.List(out.get('groups'));
}
var zoneTS = S2.map(function (img) {
  var date = img.date().format('YYYY-MM-dd');
  var g1 = grouped(img, 'NDVI', true);
  var g2 = grouped(img, 'NDMI', false);
  var key = function (d) { return ee.Number(ee.Dictionary(d).get('zone')).format('%d'); };
  // A zone with no clear pixels in this image has no 'mean' -> use defaults, drop later.
  var ndmi = ee.Dictionary.fromLists(g2.map(key),
                                     g2.map(function (d) { return ee.Dictionary(d).get('mean', -9999); }));
  return ee.FeatureCollection(g1.map(function (d) {
    d = ee.Dictionary(d);
    var z = ee.Number(d.get('zone'));
    return ee.Feature(null, {
      date: date, tile: img.get('MGRS_TILE'), zone: z,
      site_idx: z.divide(2).floor(), irrigated: z.mod(2),
      NDVI: d.get('mean', -9999), NDMI: ndmi.get(z.format('%d'), -9999),
      clear_pixels: d.get('count', 0)
    });
  }));
}).flatten().filter(ee.Filter.gt('clear_pixels', 0)).filter(ee.Filter.gt('NDVI', -9000));
Export.table.toDrive({collection: zoneTS, description: 'B_zone_timeseries',
  folder: 'drought_satellite', fileNamePrefix: 'B_zone_timeseries', fileFormat: 'CSV',
  selectors: ['date', 'tile', 'zone', 'site_idx', 'irrigated', 'NDVI', 'NDMI', 'clear_pixels']});

// ---- 3. Total farmland pixels per zone (static) ------------------------------------
var totals = ee.Image.constant(1).rename('one').addBands(ZONE).reduceRegion({
  reducer: ee.Reducer.count().group({groupField: 1, groupName: 'zone'}),
  geometry: AOI, crs: CRS, scale: SCALE, maxPixels: 1e10, tileScale: 4
});
var zonePixels = ee.FeatureCollection(ee.List(totals.get('groups')).map(function (d) {
  d = ee.Dictionary(d);
  var z = ee.Number(d.get('zone'));
  return ee.Feature(null, {zone: z, site_idx: z.divide(2).floor(), irrigated: z.mod(2),
                           site_code: ee.List(SITE_CODES).get(z.divide(2).floor()),
                           total_pixels: d.get('count')});
}));
Export.table.toDrive({collection: zonePixels, description: 'B_zone_pixels',
  folder: 'drought_satellite', fileNamePrefix: 'B_zone_pixels', fileFormat: 'CSV',
  selectors: ['zone', 'site_idx', 'site_code', 'irrigated', 'total_pixels']});

// ---- Quick checks in the Console ----------------------------------------------------
print('Sampled fields (should be 240):', FIELDS.size());
print('Sentinel-2 images found:', S2.size());
var oneField = fieldSeries(FIELDS.limit(1)).map(function (f) {
  return f.set('t', ee.Date(f.get('date')).millis());
});
print('Example: NDVI / NDMI of one field, 2019-2026 (should rise and fall with seasons)',
      ui.Chart.feature.byFeature(oneField, 't', ['NDVI_mean', 'NDMI_mean'])
        .setOptions({hAxis: {format: 'yyyy'}, pointSize: 2, lineWidth: 0}));
Map.addLayer(MASK.select('site').randomVisualizer(), {}, 'Farmland by site (from script A)');
Map.addLayer(FIELDS, {color: 'ff0000'}, 'Sampled fields');
Map.centerObject(FIELDS, 9);
print('Next: Tasks tab -> RUN all 3 exports.');

// ---- 4. UAV survey points (dataset table, Nov 2025 - Jan 2026) ----------------------
// A 25 m circle around each surveyed field centre, so the satellite series can be compared
// with the drone verdicts at the same place. Somandepalli = drone photo centre (see script A).
var UAV = [
  ['UAV_Peddakadubur',        15.782581, 77.252819, 'Ped'],
  ['UAV_Dinnedevarapadu',     15.771507, 78.047100, 'Din'],
  ['UAV_Balaji_villas',       15.783407, 78.056083, 'Bal'],
  ['UAV_Shilpa_township',     15.777797, 78.051204, 'Bal'],
  ['UAV_Puddur',              15.794037, 78.085369, 'Pul'],
  ['UAV_Pullaiah_college',    15.798243, 78.080614, 'Pul'],
  ['UAV_Cholasamudram',       13.811762, 77.568719, 'Cho'],
  ['UAV_Lepakshi',            13.799838, 77.619387, 'Lep'],
  ['UAV_Somandepalli',        13.998767, 77.624733, 'Som'],
  ['UAV_Sira',                13.797532, 76.975030, 'Sira']
];
var UAV_FC = ee.FeatureCollection(UAV.map(function (u) {
  return ee.Feature(ee.Geometry.Point([u[2], u[1]]).buffer(25), {
    field_id: u[0], site: u[0], site_code: u[3], weather: '', irrigated: -1,
    area_ha: 0.196, pixels: 20, lat: u[1], lon: u[2]});
}));
Export.table.toDrive({collection: fieldSeries(UAV_FC), description: 'B_uav_points_timeseries',
  folder: 'drought_satellite', fileNamePrefix: 'B_uav_points_timeseries', fileFormat: 'CSV',
  selectors: FIELD_COLS.concat(['lat', 'lon'])});
