<?php

namespace Database\Factories;

use App\Models\Port;
use App\Models\Vessel;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Vessel>
 */
class VesselFactory extends Factory
{
    protected $model = Vessel::class;

    public function definition(): array
    {
        return [
            'imo_number' => (string) fake()->unique()->numberBetween(1000000, 9999999),
            'name' => fake()->company() . ' Trader',
            'call_sign' => strtoupper(fake()->bothify('??###')),
            'mmsi' => (string) fake()->numberBetween(100000000, 999999999),
            'vessel_type' => fake()->randomElement(['Container', 'Bulk Carrier', 'Tanker']),
            'flag' => strtoupper(fake()->lexify('??')),
            'length' => fake()->randomFloat(2, 100, 400),
            'beam' => fake()->randomFloat(2, 20, 65),
            'draft' => fake()->randomFloat(2, 5, 20),
            'gross_tonnage' => fake()->randomFloat(2, 5000, 150000),
            'speed' => fake()->randomFloat(2, 0, 30),
            'course' => fake()->randomFloat(2, 0, 359.99),
            'destination_port_id' => Port::factory(),
            'eta' => fake()->dateTimeBetween('+1 day', '+14 days'),
        ];
    }
}
