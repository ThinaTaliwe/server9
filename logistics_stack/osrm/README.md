### OSRM data directory

This directory should contain the preprocessed OSRM map files used by the `osrm`
service in the `docker-compose.yml`. The service expects a file named
`region.osrm` and its associated `.osrm*` support files to be available in
`./data`.

To generate these files:

1. Download a raw OSM PBF file for your region from a source such as
   [Geofabrik](https://download.geofabrik.de). For example, to download road
   data for South Africa you can run:

   ```sh
   wget https://download.geofabrik.de/africa/south-africa-latest.osm.pbf -O south-africa.osm.pbf
   ```

2. Use the OSRM tools (`osrm-extract` and `osrm-partition`) on your host to
   preprocess the PBF. The commands below prepare the data for the `mld`
   algorithm used in the `osrm` service. Substitute the filename with your
   downloaded PBF.

   ```sh
   docker run --rm -t -v $(pwd):/data osrm/osrm-backend osrm-extract -p /opt/valhalla/profiles/car.lua /data/south-africa.osm.pbf
   docker run --rm -t -v $(pwd):/data osrm/osrm-backend osrm-partition /data/south-africa.osrm
   docker run --rm -t -v $(pwd):/data osrm/osrm-backend osrm-customize /data/south-africa.osrm
   ```

3. After processing, copy the resulting `.osrm` files into `logistics_stack/osrm/data/` and rename the
   base file to `region.osrm` (for example `south-africa.osrm` → `region.osrm`). The `docker-compose.yml`
   file refers to this name.

4. When you start the stack with `docker compose up -d`, the OSRM routing
   service will be available on port 5000.