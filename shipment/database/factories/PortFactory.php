<?php

namespace Database\Factories;

use App\Models\Port;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Port>
 */
class PortFactory extends Factory
{
    protected $model = Port::class;

    public function definition(): array
    {
        return [
            'unlocode' => strtoupper(fake()->lexify('??') . fake()->bothify('###')),
            'name' => fake()->city() . ' Port',
            'country_code' => strtoupper(fake()->lexify('??')),
            'timezone' => 'UTC',
            'website' => fake()->optional()->url(),
            'contact_email' => fake()->optional()->safeEmail(),
        ];
    }
}
