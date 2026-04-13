<?php

namespace Tests\Feature\Api;

use App\Models\Port;
use App\Models\Vessel;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class VesselApiTest extends TestCase
{
    use RefreshDatabase;

    public function test_it_lists_vessels(): void
    {
        Vessel::factory()->count(2)->create();

        $response = $this->getJson('/api/vessels');

        $response->assertOk();
    }

    public function test_it_creates_a_vessel(): void
    {
        $port = Port::factory()->create();

        $payload = [
            'imo_number' => '9221234',
            'name' => 'Atlas Voyager',
            'call_sign' => 'AB123',
            'mmsi' => '123456789',
            'vessel_type' => 'Container',
            'flag' => 'US',
            'length' => 250.5,
            'beam' => 40.2,
            'draft' => 12.3,
            'gross_tonnage' => 98000.0,
            'speed' => 14.5,
            'course' => 180.0,
            'destination_port_id' => $port->id,
            'eta' => now()->addDays(3)->toISOString(),
        ];

        $response = $this->postJson('/api/vessels', $payload);

        $response->assertStatus(201);

        $this->assertDatabaseHas('vessels', [
            'imo_number' => '9221234',
            'name' => 'Atlas Voyager',
        ]);
    }

    public function test_it_updates_and_soft_deletes_a_vessel(): void
    {
        $vessel = Vessel::factory()->create([
            'imo_number' => '9333333',
            'name' => 'Initial Name',
        ]);

        $this->patchJson('/api/vessels/'.$vessel->id, [
            'name' => 'Updated Name',
        ], ['CONTENT_TYPE' => 'application/merge-patch+json'])->assertOk();

        $this->assertDatabaseHas('vessels', [
            'id' => $vessel->id,
            'name' => 'Updated Name',
        ]);

        $this->deleteJson('/api/vessels/'.$vessel->id)->assertStatus(204);
        $this->assertSoftDeleted('vessels', ['id' => $vessel->id]);
    }
}
