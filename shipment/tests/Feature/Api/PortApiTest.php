<?php

namespace Tests\Feature\Api;

use App\Models\Port;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PortApiTest extends TestCase
{
    use RefreshDatabase;

    public function test_it_lists_ports(): void
    {
        Port::factory()->count(2)->create();

        $response = $this->getJson('/api/ports');

        $response->assertOk();
    }

    public function test_it_creates_a_port(): void
    {
        $payload = [
            'unlocode' => 'USNYC',
            'name' => 'New York Harbor',
            'country_code' => 'US',
            'timezone' => 'America/New_York',
            'website' => 'https://www.panynj.gov',
            'contact_email' => 'ops@example.com',
        ];

        $response = $this->postJson('/api/ports', $payload);

        $response->assertStatus(201);

        $this->assertDatabaseHas('ports', [
            'unlocode' => 'USNYC',
            'name' => 'New York Harbor',
        ]);
    }

    public function test_it_updates_and_soft_deletes_a_port(): void
    {
        $port = Port::factory()->create([
            'unlocode' => 'NLRTM',
            'name' => 'Rotterdam',
            'country_code' => 'NL',
        ]);

        $this->patchJson('/api/ports/'.$port->id, [
            'name' => 'Rotterdam Updated',
        ], ['CONTENT_TYPE' => 'application/merge-patch+json'])->assertOk();

        $this->assertDatabaseHas('ports', [
            'id' => $port->id,
            'name' => 'Rotterdam Updated',
        ]);

        $this->deleteJson('/api/ports/'.$port->id)->assertStatus(204);
        $this->assertSoftDeleted('ports', ['id' => $port->id]);
    }
}
