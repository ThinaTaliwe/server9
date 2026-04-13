# Shipping API Project

This repository contains a minimal Laravel project scaffolding for managing shipments.  It includes Blade templates for creating and listing shipments, a `Shipment` model, controller, migration, and routes.

## Features

- **Create and list shipments** using the provided Blade views located in `resources/views/shipments/`.
- **API endpoints** via `Route::apiResource('shipments', ShipmentController::class)` that return JSON responses.
- **Web endpoints** to display the shipment index and creation forms.
- **Migration** to create a `shipments` table with typical shipping fields.

## Setup Instructions

1. Install PHP (>=8.1) and Composer on your server.
2. Run `composer install` in the project root to install the Laravel framework.
3. Copy `.env.example` to `.env` and set up your database connection.
4. Run `php artisan key:generate` to set the application key.
5. Run `php artisan migrate` to create the `shipments` table.
6. Serve the application with `php artisan serve` or configure your web server accordingly.

The `shipcreate.blade.php` view has been placed at `resources/views/shipments/create.blade.php` and is used to create shipment instructions and shipments.  The `ShipmentIndex.blade.php` template is now `resources/views/shipments/index.blade.php` and displays shipment data.
