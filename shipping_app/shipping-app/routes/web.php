<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ShipmentController;

// Web routes for shipment management
Route::get('/shipments', [ShipmentController::class, 'index'])->name('shipments.index');
Route::get('/shipments/create', [ShipmentController::class, 'create'])->name('shipments.create');
Route::post('/shipments', [ShipmentController::class, 'store'])->name('shipments.store');
