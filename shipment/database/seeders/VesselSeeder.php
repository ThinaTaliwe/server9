<?php

namespace Database\Seeders;

use App\Models\Port;
use App\Models\Vessel;
use Illuminate\Database\Seeder;

class VesselSeeder extends Seeder
{
    public function run(): void
    {
        $ports = Port::query()->pluck('id');

        Vessel::factory()
            ->count(20)
            ->state(function () use ($ports) {
                return [
                    'destination_port_id' => $ports->isNotEmpty() ? $ports->random() : Port::factory(),
                ];
            })
            ->create();
    }
}
