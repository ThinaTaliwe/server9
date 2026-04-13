<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class ShipmentWebController extends Controller
{
    private function baseUrl(): string
    {
        $base = rtrim(config('services.siya.base_url', env('SIYA_API_BASE', 'http://siya-app:8000')), '/');
        $prefix = trim(config('services.siya.prefix', env('SIYA_API_PREFIX', '')), '/');

        return $prefix ? "{$base}/{$prefix}" : $base;
    }

    private function client()
    {
        $http = Http::timeout(20)->acceptJson();

        $token = config('services.siya.token');
        if ($token) {
            $http = $http->withToken($token);
        }

        return $http;
    }

    private function url(string $path): string
    {
        return rtrim($this->baseUrl(), '/') . '/' . ltrim($path, '/');
    }

    private function safeGet(string $path, array $query = []): array
    {
        try {
            $response = $this->client()->get($this->url($path), $query);

            if ($response->successful()) {
                return [
                    'ok' => true,
                    'status' => $response->status(),
                    'data' => $response->json(),
                ];
            }

            Log::warning('Siya GET request failed', [
                'path' => $path,
                'status' => $response->status(),
                'body' => $response->body(),
            ]);

            return [
                'ok' => false,
                'status' => $response->status(),
                'data' => [],
            ];
        } catch (\Throwable $e) {
            Log::error('Siya GET exception', [
                'path' => $path,
                'message' => $e->getMessage(),
            ]);

            return [
                'ok' => false,
                'status' => 500,
                'data' => [],
            ];
        }
    }

    public function create()
    {
        /*
        |--------------------------------------------------------------------------
        | Load shipment-related reference data for the wizard
        |--------------------------------------------------------------------------
        |
        | Your current Blade expects:
        |   $shipmentData.results
        |
        | So we always pass an object/array that safely contains "results",
        | even if Siya is temporarily unavailable.
        |
        */

        $shipmentData = [
            'results' => [],
        ];

        /*
        |--------------------------------------------------------------------------
        | Try likely Siya endpoints in order
        |--------------------------------------------------------------------------
        |
        | We do not break the page if one endpoint is unavailable.
        | We keep the UI working and let the next step refine this.
        |
        */

        $candidates = [
            '/api/shipments/',
            '/api/shipments/instruction-types/',
            '/api/shipments/instruction-type/',
            '/api/shipments/shipment-instruction-types/',
        ];

        foreach ($candidates as $path) {
            $result = $this->safeGet($path);

            if ($result['ok'] && !empty($result['data'])) {
                $data = $result['data'];

                if (isset($data['results']) && is_array($data['results'])) {
                    $shipmentData = $data;
                    break;
                }

                if (is_array($data)) {
                    $shipmentData = [
                        'results' => array_is_list($data) ? $data : [$data],
                    ];
                    break;
                }
            }
        }

        return view('bfrn.shipcreate', compact('shipmentData'));
    }

    public function store(Request $request)
    {
        /*
        |--------------------------------------------------------------------------
        | Keep current functionality unchanged for now
        |--------------------------------------------------------------------------
        |
        | We are only polishing structure in this step.
        | Actual submission to Siya comes in the next step.
        |
        */

        return response()->json([
            'status' => 'ok',
            'message' => 'Shipment submit step not connected yet.',
            'payload' => $request->all(),
        ]);
    }
}