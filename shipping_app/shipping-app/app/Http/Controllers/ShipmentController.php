<?php

namespace App\Http\Controllers;

use App\Models\Shipment;
use Illuminate\Http\Request;

/**
 * ShipmentController
 *
 * Handles both web and API actions for shipments. For web routes it
 * returns Blade views; for API requests it returns JSON responses.
 */
class ShipmentController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request)
    {
        // Use pagination for web and return JSON for API
        $shipments = Shipment::latest()->paginate(10);
        if ($request->wantsJson()) {
            return response()->json($shipments);
        }
        return view('shipments.index', compact('shipments'));
    }

    /**
     * Show the form for creating a new shipment.
     */
    public function create()
    {
        return view('shipments.create');
    }

    /**
     * Store a newly created shipment in storage.
     */
    public function store(Request $request)
    {
        $data = $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'description' => ['nullable', 'string'],
            'shipment_type' => ['required', 'string', 'max:255'],
            'mode_of_transport' => ['required', 'string', 'max:255'],
            'shipment_instruction' => ['required', 'string', 'max:255'],
            'from_address' => ['required', 'string', 'max:255'],
            'to_address' => ['required', 'string', 'max:255'],
            'bu' => ['required', 'string', 'max:255'],
        ]);

        $shipment = Shipment::create($data);

        // Respond differently for API requests
        if ($request->wantsJson()) {
            return response()->json(['data' => $shipment], 201);
        }

        return redirect()->route('shipments.index')->with('success', 'Shipment created successfully');
    }

    /**
     * Display the specified shipment.
     */
    public function show(Shipment $shipment)
    {
        return response()->json(['data' => $shipment]);
    }

    /**
     * Update the specified shipment.
     */
    public function update(Request $request, Shipment $shipment)
    {
        $data = $request->validate([
            'name' => ['sometimes', 'string', 'max:255'],
            'description' => ['nullable', 'string'],
            'shipment_type' => ['sometimes', 'string', 'max:255'],
            'mode_of_transport' => ['sometimes', 'string', 'max:255'],
            'shipment_instruction' => ['sometimes', 'string', 'max:255'],
            'from_address' => ['sometimes', 'string', 'max:255'],
            'to_address' => ['sometimes', 'string', 'max:255'],
            'bu' => ['sometimes', 'string', 'max:255'],
        ]);
        $shipment->update($data);
        return response()->json(['data' => $shipment]);
    }

    /**
     * Remove the specified shipment from storage.
     */
    public function destroy(Shipment $shipment)
    {
        $shipment->delete();
        return response()->json(['message' => 'Shipment deleted successfully']);
    }
}
