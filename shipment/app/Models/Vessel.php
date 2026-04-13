<?php
namespace App\Models;

use ApiPlatform\Metadata\ApiResource;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

#[ApiResource(
    order: ['name' => 'ASC'],
    paginationItemsPerPage: 20,
)]
class Vessel extends Model
{
    use HasFactory;
    use SoftDeletes;

    protected $fillable = [
        'imo_number', 'name', 'call_sign', 'mmsi', 'vessel_type',
        'flag', 'length', 'beam', 'draft', 'gross_tonnage',
        'current_location', 'speed', 'course', 'destination_port_id', 'eta'
    ];

    protected $casts = [
        'eta' => 'datetime',
        'length' => 'decimal:2', 'beam' => 'decimal:2', 'draft' => 'decimal:2',
        'gross_tonnage' => 'decimal:2', 'speed' => 'decimal:2', 'course' => 'decimal:2',
        'current_location' => 'array',
    ];

    public function destinationPort(): BelongsTo
    {
        return $this->belongsTo(Port::class, 'destination_port_id');
    }
}
