# Shipment API

Shipment API is a Laravel 13 + API Platform backend for managing maritime data.

## Core domain

- **Ports**: port identity (`unlocode`), country, timezone, geospatial location, and contact metadata.
- **Vessels**: vessel identity (`imo_number`) and operational/tracking fields such as current location, speed, course, destination port, and ETA.

Both entities are exposed as API Platform resources and support soft deletes.

## Tech stack

- PHP 8.3
- Laravel 13
- API Platform for Laravel
- PostgreSQL/PostGIS-compatible schema (`geography` columns + spatial indexes)

## API behavior

By default, API Platform exposes resources under `/api` and enables OpenAPI/Swagger/ReDoc/Scalar documentation UIs.
Because `name_converter` is set to `SnakeCaseToCamelCaseNameConverter`, JSON payload field names are camelCase (for example: `imoNumber`, `countryCode`, `destinationPortId`).

## Development

Install dependencies:

```bash
composer install
npm install
```

Create local env and app key:

```bash
cp .env.example .env
php artisan key:generate
```

Run migrations (use a Postgres database with PostGIS support):

```bash
php artisan migrate
```

Seed sample maritime data:

```bash
php artisan db:seed
```

Start the app:

```bash
composer run dev
```

Open the lightweight UI dashboard:

```text
/dashboard
```

## Testing

```bash
php artisan test
```

API feature tests now cover:

- listing, creating, updating, and soft deleting Ports
- listing, creating, updating, and soft deleting Vessels

## Notes

- `vessels.destination_port_id` is modeled as a foreign key relationship to `ports.id`.
- Geospatial fields are currently stored in PostGIS-friendly `geography(point, 4326)` columns.
