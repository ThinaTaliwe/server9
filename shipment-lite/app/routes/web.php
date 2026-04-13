<?php

use App\Http\Controllers\ShipmentWebController;
use App\Http\Controllers\Api\SiyaProxyController;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Direct proxy test route
|--------------------------------------------------------------------------
*/
Route::get('/api/proxy/movement', function () {
    $base = rtrim(env('SIYA_API_BASE', 'http://siya-app:8000'), '/');
    $url  = $base . '/siya/api/movement/';

    try {
        $res = Http::timeout(15)->acceptJson()->get($url);

        return response()->json($res->json(), $res->status());
    } catch (\Throwable $e) {
        return response()->json([
            'status'  => 'error',
            'message' => 'Failed to reach Siya API',
            'url'     => $url,
            'details' => $e->getMessage(),
        ], 504);
    }
});

/*
|--------------------------------------------------------------------------
| Freehub JSON dataset routes
|--------------------------------------------------------------------------
*/
Route::get('/bfrn/api/freehub/ports', function () {
    $p = base_path('resources/js/datasets/json/ports.json');

    if (!file_exists($p)) {
        return response()->json(['error' => 'ports.json missing'], 404);
    }

    return response()->file($p, ['Content-Type' => 'application/json']);
});

Route::get('/bfrn/api/freehub/lines', function () {
    $p = base_path('resources/js/datasets/json/shipping_lines.json');

    if (!file_exists($p)) {
        return response()->json(['error' => 'shipping_lines.json missing'], 404);
    }

    return response()->file($p, ['Content-Type' => 'application/json']);
});

Route::get('/bfrn/api/freehub/agents', function () {
    $p = base_path('resources/js/datasets/json/clearing_agents.json');

    if (!file_exists($p)) {
        return response()->json(['error' => 'clearing_agents.json missing'], 404);
    }

    return response()->file($p, ['Content-Type' => 'application/json']);
});

Route::get('/bfrn/api/freehub/cma/events', function () {
    $key = env('CMA_KEYID');

    if (!$key) {
        return response()->json(['error' => 'CMA_KEYID missing in env'], 500);
    }

    $eventType = request('eventType', 'EQUIPMENT');
    $limit = (int) request('limit', 10);

    $equipmentReference = request('equipmentReference');
    $carrierBookingReference = request('carrierBookingReference');

    if (!$equipmentReference && !$carrierBookingReference) {
        return response()->json([
            'error' => 'equipmentReference or carrierBookingReference required'
        ], 400);
    }

    $query = [
        'eventType' => $eventType,
        'limit'     => $limit,
    ];

    if ($equipmentReference) {
        $query['equipmentReference'] = $equipmentReference;
    }

    if ($carrierBookingReference) {
        $query['carrierBookingReference'] = $carrierBookingReference;
    }

    $url = 'https://apis.cma-cgm.net/operation/trackandtrace/v1/events';

    $res = Http::timeout(20)
        ->acceptJson()
        ->withHeaders(['keyId' => $key])
        ->get($url, $query);

    return response()->json($res->json(), $res->status());
});

/*
|--------------------------------------------------------------------------
| BFRN web + proxy routes
|--------------------------------------------------------------------------
*/
Route::prefix('bfrn')->name('bfrn.')->group(function () {

/*
    |--------------------------------------------------------------------------
    | API List
    |--------------------------------------------------------------------------
    */
    Route::get('/docs', function () {
        return view('index');
    })->name('index');

    /*
    |--------------------------------------------------------------------------
    | UI Pages
    |--------------------------------------------------------------------------
    */
    Route::get('/', function () {
        return view('ShipmentIndex');
    })->name('index');


    Route::get('/', function () {
        return redirect('/shipments');
    });

    Route::get('/list', function () {
        return view('welcome');
    })->name('welcome');

    Route::get('/create', [ShipmentWebController::class, 'create'])->name('create');
    Route::get('/shipcreate', [ShipmentWebController::class, 'create'])->name('shipments.create');
    Route::post('/shipments', [ShipmentWebController::class, 'store'])->name('shipments.store');

    Route::get('/APImap', function () {
        return view('ShipmentSA');
    })->name('shipmentSA');

    Route::get('/APIdata', function () {
        return view('ShipmentDiagram');
    })->name('diagram');

    Route::get('/api', function () {
        return view('ShipmentAPI');
    })->name('api');

    /*
    |--------------------------------------------------------------------------
    | API Proxy Routes
    |--------------------------------------------------------------------------
    */
    Route::prefix('api')->name('api.')->group(function () {
        Route::get('/shipments', [SiyaProxyController::class, 'shipmentsIndex'])->name('shipments.index');
        Route::post('/shipments', [SiyaProxyController::class, 'shipmentsStore'])->name('shipments.store');
        Route::get('/shipments/{id}', [SiyaProxyController::class, 'shipmentsShow'])->name('shipments.show');
        Route::put('/shipments/{id}', [SiyaProxyController::class, 'shipmentsUpdate'])->name('shipments.update');
        Route::delete('/shipments/{id}', [SiyaProxyController::class, 'shipmentsDestroy'])->name('shipments.destroy');

        Route::get('/loading/loadings', [SiyaProxyController::class, 'loadings'])->name('loading.loadings');
        Route::get('/loading/loading-items', [SiyaProxyController::class, 'loadingItems'])->name('loading.items');

        Route::get('/movement/movements', [SiyaProxyController::class, 'movements'])->name('movement.movements');
        Route::get('/movement/movement-items', [SiyaProxyController::class, 'movementItems'])->name('movement.items');

        Route::get('/offloading/offloadings', [SiyaProxyController::class, 'offloadings'])->name('offloading.offloadings');
        Route::get('/offloading/offloading-items', [SiyaProxyController::class, 'offloadingItems'])->name('offloading.items');

        Route::get('/storage/storage', [SiyaProxyController::class, 'storage'])->name('storage.storage');
        Route::get('/storage/storage-items', [SiyaProxyController::class, 'storageItems'])->name('storage.items');

        Route::get('/bu', [SiyaProxyController::class, 'buList'])->name('bu.index');

        Route::get('/shipment-types', [SiyaProxyController::class, 'shipmentTypes'])->name('shipment-types.index');

        Route::get('/address-types', [SiyaProxyController::class, 'addressTypes'])->name('address-types.index');

        Route::get('/addresses', [SiyaProxyController::class, 'addressesIndex'])->name('addresses.index');
        Route::post('/addresses', [SiyaProxyController::class, 'addressesStore'])->name('addresses.store');

        Route::post('/shipment-instructions', [SiyaProxyController::class, 'shipmentInstructionsStore'])->name('shipment-instructions.store');
    });
});
