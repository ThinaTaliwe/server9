<?php
namespace App\Models;

use ApiPlatform\Metadata\ApiResource;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\SoftDeletes;

#[ApiResource(
    order: ['name' => 'ASC'],
)]
class Port extends Model
{
    use HasFactory;
    use SoftDeletes;

    protected $fillable = [
        'unlocode', 'name', 'country_code', 'timezone',
        'location', 'website', 'contact_email'
    ];

    protected $casts = [
        'location' => 'array' // GeoJSON for PostGIS
    ];

    public function destinationVessels(): HasMany
    {
        return $this->hasMany(Vessel::class, 'destination_port_id');
    }
}
