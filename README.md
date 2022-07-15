# Do wealthy neighborhoods have greener and cooler environment?

## Datasets
+ Global 10-daily Leaf Area Index 333m
```json
{
  "datasetId": "EO:CLMS:DAT:CGLS_GLOBAL_LAI300_V1_333M",
  "dateRangeSelectValues": [
    {
      "name": "dtrange",
      "start": "2022-06-01T00:00:00.000Z",
      "end": "2022-06-30T23:59:59.999Z"
    }
  ]
}
```
+ Level 2 Land - Sea and Land Surface 
Temperature Radiometer (SLSTR) - Sentinel-3
```json
{
  "datasetId": "EO:ESA:DAT:SENTINEL-3:SL_2_LST___",
  "boundingBoxValues": [
    {
      "name": "bbox",
      "bbox": [
        18.99804053609134,
        47.42120186691113,
        19.190237776905892,
        47.58048586099437
      ]
    }
  ],
  "dateRangeSelectValues": [
    {
      "name": "position",
      "start": "2022-06-01T00:00:00.000Z",
      "end": "2022-06-30T00:00:00.000Z"
    }
  ],
  "stringChoiceValues": [
    {
      "name": "productType",
      "value": "LST"
    },
    {
      "name": "timeliness",
      "value": "Near+Real+Time"
    },
    {
      "name": "orbitDirection",
      "value": "ascending"
    },
    {
      "name": "processingLevel",
      "value": "LEVEL2"
    }
  ]
}
```
+ Global 10-daily Fraction of Vegetation Cover 333m
```json
{
  "datasetId": "EO:CLMS:DAT:CGLS_GLOBAL_FCOVER300_V1_333M",
  "dateRangeSelectValues": [
    {
      "name": "dtrange",
      "start": "2022-06-01T00:00:00.000Z",
      "end": "2022-06-30T23:59:59.999Z"
    }
  ]
}
```
+ [Budapest administrative boundaries shapefile](https://data2.openstreetmap.hu/hatarok/index.php?admin=8)
+ Budapest property square meter prices
  ([collected by our own scraper](https://github.com/Urbanum-Lab/budapest_property_price_scraper))

## TODOs
+ Refactor code, put reusable functions into a utils module
+ clean up data folder