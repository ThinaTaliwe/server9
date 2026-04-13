<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>Available Routes</title>
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; }
        td { vertical-align: top; padding: 10px; }
        h2 { margin-top: 0; color: #333; }
        ul { padding-left: 20px; }
        li { margin: 5px 0; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .section-header { 
            background: #f5f5f5; 
            padding: 8px 12px; 
            margin: 15px 0 10px 0; 
            border-left: 4px solid #0066cc;
            font-weight: bold;
        }
        .param-note { 
            font-size: 0.85em; 
            color: #666; 
            font-style: italic; 
        }
        pre { 
            background: #f8f8f8; 
            padding: 10px; 
            border-radius: 4px; 
            overflow-x: auto; 
        }
        details { margin: 5px 0; }
        summary { cursor: pointer; }
    </style>
</head>
<body>
    <div id="app">
        <center>
            <h1>Available Routes</h1>
        </center>

        <table border="1" width="100%" cellpadding="10" cellspacing="0">
            <tr>
                <td width="33%" valign="top" style="max-height: 100vh; overflow-y: auto;">
                    <h2>GET Routes</h2>
                    
                    <!-- Original BFRN Routes -->
                    <div class="section-header">BFRN Core Routes</div>
                    <ul>
                        <li>
                            <a href="{{ url('/api/proxy/movement') }}"
                               @click.prevent="loadRoute('{{ url('/api/proxy/movement') }}', 'GET /api/proxy/movement')">
                                GET /api/proxy/movement
                            </a>
                        </li>
                        <li>
                            <a href="{{ url('/bfrn/api/freehub/ports') }}"
                               @click.prevent="loadRoute('{{ url('/bfrn/api/freehub/ports') }}', 'GET /bfrn/api/freehub/ports')">
                                GET /bfrn/api/freehub/ports
                            </a>
                        </li>
                        <li>
                            <a href="{{ url('/bfrn/api/freehub/lines') }}"
                               @click.prevent="loadRoute('{{ url('/bfrn/api/freehub/lines') }}', 'GET /bfrn/api/freehub/lines')">
                                GET /bfrn/api/freehub/lines
                            </a>
                        </li>
                        <li>
                            <a href="{{ url('/bfrn/api/freehub/agents') }}"
                               @click.prevent="loadRoute('{{ url('/bfrn/api/freehub/agents') }}', 'GET /bfrn/api/freehub/agents')">
                                GET /bfrn/api/freehub/agents
                            </a>
                        </li>
                        <li>
                            <a href="{{ url('/bfrn/api/freehub/cma/events') }}"
                               @click.prevent="loadRoute('{{ url('/bfrn/api/freehub/cma/events') }}', 'GET /bfrn/api/freehub/cma/events')">
                                GET /bfrn/api/freehub/cma/events
                                <span class="param-note">*(requires query params)</span>
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.index') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.index') }}', 'GET /bfrn')">
                                GET /bfrn
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.create') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.create') }}', 'GET /bfrn/create')">
                                GET /bfrn/create
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.shipments.create') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.shipments.create') }}', 'GET /bfrn/shipcreate')">
                                GET /bfrn/shipcreate
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.shipmentSA') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.shipmentSA') }}', 'GET /bfrn/APImap')">
                                GET /bfrn/APImap
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.diagram') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.diagram') }}', 'GET /bfrn/APIdata')">
                                GET /bfrn/APIdata
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.api') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.api') }}', 'GET /bfrn/api')">
                                GET /bfrn/api
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.api.shipments.index') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.api.shipments.index') }}', 'GET /bfrn/api/shipments')">
                                GET /bfrn/api/shipments
                            </a>
                        </li>
                        <li>
                            <a href="{{ url('/bfrn/api/shipments/1') }}"
                               @click.prevent="loadRoute('{{ url('/bfrn/api/shipments/1') }}', 'GET /bfrn/api/shipments/{id}')">
                                GET /bfrn/api/shipments/{id}
                                <span class="param-note">*(example: id=1)</span>
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.api.loading.loadings') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.api.loading.loadings') }}', 'GET /bfrn/api/loading/loadings')">
                                GET /bfrn/api/loading/loadings
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.api.loading.items') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.api.loading.items') }}', 'GET /bfrn/api/loading/loading-items')">
                                GET /bfrn/api/loading/loading-items
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.api.movement.movements') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.api.movement.movements') }}', 'GET /bfrn/api/movement/movements')">
                                GET /bfrn/api/movement/movements
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.api.movement.items') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.api.movement.items') }}', 'GET /bfrn/api/movement/movement-items')">
                                GET /bfrn/api/movement/movement-items
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.api.offloading.offloadings') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.api.offloading.offloadings') }}', 'GET /bfrn/api/offloading/offloadings')">
                                GET /bfrn/api/offloading/offloadings
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.api.offloading.items') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.api.offloading.items') }}', 'GET /bfrn/api/offloading/offloading-items')">
                                GET /bfrn/api/offloading/offloading-items
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.api.storage.storage') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.api.storage.storage') }}', 'GET /bfrn/api/storage/storage')">
                                GET /bfrn/api/storage/storage
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.api.storage.items') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.api.storage.items') }}', 'GET /bfrn/api/storage/storage-items')">
                                GET /bfrn/api/storage/storage-items
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.api.bu.index') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.api.bu.index') }}', 'GET /bfrn/api/bu')">
                                GET /bfrn/api/bu
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.api.shipment-types.index') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.api.shipment-types.index') }}', 'GET /bfrn/api/shipment-types')">
                                GET /bfrn/api/shipment-types
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.api.address-types.index') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.api.address-types.index') }}', 'GET /bfrn/api/address-types')">
                                GET /bfrn/api/address-types
                            </a>
                        </li>
                        <li>
                            <a href="{{ route('bfrn.api.addresses.index') }}"
                               @click.prevent="loadRoute('{{ route('bfrn.api.addresses.index') }}', 'GET /bfrn/api/addresses')">
                                GET /bfrn/api/addresses
                            </a>
                        </li>
                    </ul>

                    <!-- NEW: Container Tracking Endpoints -->
                    <div class="section-header">Container Tracking Endpoints</div>
                    <ul>
                        <li>
                            <a href="{{ url('/api/containers/MSKU1234567/tracking') }}"
                               @click.prevent="loadRoute('{{ url('/api/containers/MSKU1234567/tracking') }}', 'GET /api/containers/{container_number}/tracking')">
                                GET /api/containers/{container_number}/tracking
                                <span class="param-note">*(example: MSKU1234567)</span>
                            </a>
                        </li>
                        <li>
                            <a href="{{ url('/api/containers/MSKU1234567/route') }}"
                               @click.prevent="loadRoute('{{ url('/api/containers/MSKU1234567/route') }}', 'GET /api/containers/{container_number}/route')">
                                GET /api/containers/{container_number}/route
                                <span class="param-note">*(example: MSKU1234567)</span>
                            </a>
                        </li>
                        <li>
                            <a href="{{ url('/api/containers/MSKU1234567/history') }}"
                               @click.prevent="loadRoute('{{ url('/api/containers/MSKU1234567/history') }}', 'GET /api/containers/{container_number}/history')">
                                GET /api/containers/{container_number}/history
                                <span class="param-note">*(example: MSKU1234567)</span>
                            </a>
                        </li>
                        <li>
                            <a href="{{ url('/api/containers/MSKU1234567/vessel') }}"
                               @click.prevent="loadRoute('{{ url('/api/containers/MSKU1234567/vessel') }}', 'GET /api/containers/{container_number}/vessel')">
                                GET /api/containers/{container_number}/vessel
                                <span class="param-note">*(example: MSKU1234567)</span>
                            </a>
                        </li>
                    </ul>

                    <!-- NEW: Shipping Tracking Endpoints -->
                    <div class="section-header"> Shipping Tracking Endpoints</div>
                    <ul>
                        <li>
                            <a href="{{ url('/api/shipments/1001/tracking') }}"
                               @click.prevent="loadRoute('{{ url('/api/shipments/1001/tracking') }}', 'GET /api/shipments/{shipment_id}/tracking')">
                                GET /api/shipments/{shipment_id}/tracking
                                <span class="param-note">*(example: shipment_id=1001)</span>
                            </a>
                        </li>
                        <li>
                            <a href="{{ url('/api/shipments/1001/tracking/start') }}"
                               @click.prevent="loadRoute('{{ url('/api/shipments/1001/tracking/start') }}', 'GET /api/shipments/{shipment_id}/tracking/start')">
                                GET /api/shipments/{shipment_id}/tracking/start
                                <span class="param-note">*(example: shipment_id=1001)</span>
                            </a>
                        </li>
                    </ul>

                    <!-- NEW: Bill of Lading Tracking Endpoint -->
                    <div class="section-header"> Bill of Lading Tracking</div>
                    <ul>
                        <li>
                            <a href="{{ url('/api/bl/BL123456789/tracking') }}"
                               @click.prevent="loadRoute('{{ url('/api/bl/BL123456789/tracking') }}', 'GET /api/bl/{bl_number}/tracking')">
                                GET /api/bl/{bl_number}/tracking
                                <span class="param-note">*(example: BL123456789)</span>
                            </a>
                        </li>
                    </ul>

                    <!-- NEW: Shipping Lines Endpoints -->
                    <div class="section-header"> Shipping Lines Endpoints</div>
                    <ul>
                        <li>
                            <a href="{{ url('/api/shipping-lines') }}"
                               @click.prevent="loadRoute('{{ url('/api/shipping-lines') }}', 'GET /api/shipping-lines')">
                                GET /api/shipping-lines
                            </a>
                        </li>
                        <li>
                            <a href="{{ url('/api/shipping-lines/MSK') }}"
                               @click.prevent="loadRoute('{{ url('/api/shipping-lines/MSK') }}', 'GET /api/shipping-lines/{scac}')">
                                GET /api/shipping-lines/{scac}
                                <span class="param-note">*(example: SCAC code like MSK, CMA, COSCO)</span>
                            </a>
                        </li>
                    </ul>

                    <!-- NEW: Tracking History Endpoints -->
                    <div class="section-header"> Tracking History Endpoints</div>
                    <ul>
                        <li>
                            <a href="{{ url('/api/tracking/history') }}"
                               @click.prevent="loadRoute('{{ url('/api/tracking/history') }}', 'GET /api/tracking/history')">
                                GET /api/tracking/history
                            </a>
                        </li>
                        <li>
                            <a href="{{ url('/api/tracking/history/500') }}"
                               @click.prevent="loadRoute('{{ url('/api/tracking/history/500') }}', 'GET /api/tracking/history/{id}')">
                                GET /api/tracking/history/{id}
                                <span class="param-note">*(example: id=500)</span>
                            </a>
                        </li>
                    </ul>

                    <!-- NEW: Provider-specific Endpoints -->
                    <div class="section-header"> Provider-specific Endpoints</div>
                    <ul>
                        <li>
                            <a href="{{ url('/api/providers/shipsgo/container/MSKU1234567') }}"
                               @click.prevent="loadRoute('{{ url('/api/providers/shipsgo/container/MSKU1234567') }}', 'GET /api/providers/shipsgo/container/{container}')">
                                GET /api/providers/shipsgo/container/{container}
                                <span class="param-note">*(ShipsGo provider)</span>
                            </a>
                        </li>
                        <li>
                            <a href="{{ url('/api/providers/searates/container/MSKU1234567') }}"
                               @click.prevent="loadRoute('{{ url('/api/providers/searates/container/MSKU1234567') }}', 'GET /api/providers/searates/container/{container}')">
                                GET /api/providers/searates/container/{container}
                                <span class="param-note">*(SeaRates provider)</span>
                            </a>
                        </li>
                        <li>
                            <a href="{{ url('/api/providers/searates/route/MSKU1234567') }}"
                               @click.prevent="loadRoute('{{ url('/api/providers/searates/route/MSKU1234567') }}', 'GET /api/providers/searates/route/{container}')">
                                GET /api/providers/searates/route/{container}
                                <span class="param-note">*(SeaRates provider)</span>
                            </a>
                        </li>
                    </ul>

                    <h2>Non-GET Routes</h2>
                    <ul>
                        <li><a href="#" @click.prevent="showMessage('POST /bfrn/shipments')">POST /bfrn/shipments</a></li>
                        <li><a href="#" @click.prevent="showMessage('POST /bfrn/api/shipments')">POST /bfrn/api/shipments</a></li>
                        <li><a href="#" @click.prevent="showMessage('PUT /bfrn/api/shipments/{id}')">PUT /bfrn/api/shipments/{id}</a></li>
                        <li><a href="#" @click.prevent="showMessage('DELETE /bfrn/api/shipments/{id}')">DELETE /bfrn/api/shipments/{id}</a></li>
                        <li><a href="#" @click.prevent="showMessage('POST /bfrn/api/addresses')">POST /bfrn/api/addresses</a></li>
                        <li><a href="#" @click.prevent="showMessage('POST /bfrn/api/shipment-instructions')">POST /bfrn/api/shipment-instructions</a></li>
                        <!-- NEW: Non-GET tracking endpoints (if applicable) -->
                        <li><a href="#" @click.prevent="showMessage('POST /api/shipments/{id}/tracking/start')">POST /api/shipments/{id}/tracking/start</a></li>
                    </ul>

                    <h2>Notes</h2>
                    <ul>
                        <li>The CMA events route needs query parameters.</li>
                        <li>The shipment show, update, and delete routes need an actual ID.</li>
                        <li>POST, PUT, and DELETE routes cannot be opened directly like normal links.</li>
                        <li><strong>Container/BL tracking endpoints:</strong> Replace placeholder values (e.g., <code>MSKU1234567</code>, <code>BL123456789</code>) with real identifiers.</li>
                        <li><strong>SCAC codes:</strong> Use valid Standard Carrier Alpha Codes like <code>MSK</code> (Maersk), <code>CMA</code> (CMA CGM), <code>COSCO</code>, etc.</li>
                        <li>Provider endpoints may require additional authentication headers.</li>
                    </ul>
                </td>

                <td width="67%" valign="top">
                    <h2>Smart JSON Data Viewer</h2>

                    <p><strong>Selected Route:</strong> @{{ selectedRoute }}</p>
                    <p><strong>Status:</strong> @{{ status }}</p>

                    <div v-if="loading">
                        <p>⏳ Loading data...</p>
                    </div>

                    <div v-else-if="error">
                        <p style="color: #c00;"><strong>Error:</strong> @{{ error }}</p>
                    </div>

                    <div v-else-if="jsonData !== null">
                        <json-viewer :data="jsonData"></json-viewer>
                    </div>

                    <div v-else>
                        <p>Click a GET route on the left to view data here without reloading the page.</p>
                    </div>
                </td>
            </tr>
        </table>
    </div>

    <script>
        const JsonViewer = {
            name: 'JsonViewer',
            props: ['data'],
            template: `
                <div style="font-family: monospace; font-size: 13px;">
                    <template v-if="isObject(data)">
                        <ul style="list-style: none; padding-left: 0;">
                            <li v-for="(value, key) in data" :key="key" style="margin: 3px 0;">
                                <strong style="color: #881391;">@{{ key }}</strong>: 
                                <template v-if="isObject(value) || Array.isArray(value)">
                                    <details open>
                                        <summary style="cursor: pointer; color: #0066cc;">
                                            <span v-if="Array.isArray(value)">[Array(@{{ value.length }})]</span>
                                            <span v-else>{Object}</span>
                                        </summary>
                                        <div style="margin-left: 20px;">
                                            <json-viewer :data="value"></json-viewer>
                                        </div>
                                    </details>
                                </template>
                                <template v-else>
                                    <span style="color: #1a1aa6;">@{{ formatValue(value) }}</span>
                                </template>
                            </li>
                        </ul>
                    </template>

                    <template v-else-if="Array.isArray(data)">
                        <ol style="list-style: none; padding-left: 0;">
                            <li v-for="(item, index) in data" :key="index" style="margin: 3px 0;">
                                <span style="color: #999;">[@{{ index }}]</span>
                                <template v-if="isObject(item) || Array.isArray(item)">
                                    <details open>
                                        <summary style="cursor: pointer; color: #0066cc;">
                                            <span v-if="Array.isArray(item)">[Array(@{{ item.length }})]</span>
                                            <span v-else>{Object}</span>
                                        </summary>
                                        <div style="margin-left: 20px;">
                                            <json-viewer :data="item"></json-viewer>
                                        </div>
                                    </details>
                                </template>
                                <template v-else>
                                    <span style="color: #1a1aa6;">@{{ formatValue(item) }}</span>
                                </template>
                            </li>
                        </ol>
                    </template>

                    <template v-else>
                        <pre style="margin: 0; white-space: pre-wrap;">@{{ formatValue(data) }}</pre>
                    </template>
                </div>
            `,
            methods: {
                isObject(value) {
                    return value !== null && typeof value === 'object' && !Array.isArray(value);
                },
                formatValue(value) {
                    if (value === null) return 'null';
                    if (typeof value === 'boolean') return value ? 'true' : 'false';
                    if (typeof value === 'number') return value;
                    if (typeof value === 'string') return '"' + value + '"';
                    if (typeof value === 'object') return JSON.stringify(value, null, 2);
                    return String(value);
                }
            }
        };

        const app = Vue.createApp({
            components: {
                JsonViewer
            },
            data() {
                return {
                    selectedRoute: 'None',
                    status: 'Idle',
                    loading: false,
                    error: '',
                    jsonData: null
                };
            },
            methods: {
                async loadRoute(url, label) {
                    this.selectedRoute = label;
                    this.status = 'Loading';
                    this.loading = true;
                    this.error = '';
                    this.jsonData = null;

                    try {
                        const response = await fetch(url, {
                            method: 'GET',
                            headers: {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'
                                // Add auth headers here if needed:
                                // 'Authorization': 'Bearer YOUR_TOKEN'
                            },
                            credentials: 'same-origin' // Include cookies if using session auth
                        });

                        const contentType = response.headers.get('content-type') || '';

                        if (!response.ok) {
                            let errorText = 'Request failed with status ' + response.status;
                            try {
                                if (contentType.includes('application/json')) {
                                    const errorJson = await response.json();
                                    errorText = JSON.stringify(errorJson, null, 2);
                                } else {
                                    errorText = await response.text();
                                }
                            } catch (e) {}
                            throw new Error(errorText);
                        }

                        if (contentType.includes('application/json')) {
                            this.jsonData = await response.json();
                        } else {
                            const text = await response.text();
                            this.jsonData = {
                                message: 'Response is not JSON',
                                contentType: contentType,
                                preview: text.substring(0, 500) + (text.length > 500 ? '...' : '')
                            };
                        }

                        this.status = 'Loaded ✓';
                    } catch (err) {
                        this.error = err.message;
                        this.status = 'Error ✗';
                    } finally {
                        this.loading = false;
                    }
                },
                showMessage(route) {
                    this.selectedRoute = route;
                    this.status = 'Info ℹ';
                    this.loading = false;
                    this.error = '';
                    this.jsonData = {
                        message: 'This route is not a GET route.',
                        route: route,
                        note: 'Use Postman, JavaScript fetch/AJAX, or a form submission for this endpoint.',
                        tip: 'For testing POST/PUT/DELETE: Use the browser console with fetch() or a tool like Insomnia/Postman.'
                    };
                }
            }
        });

        app.mount('#app');
    </script>
</body>
</html>