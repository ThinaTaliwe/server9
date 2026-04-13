<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

/**
 * Shipment model
 *
 * Represents a shipping record in the system. Fillable fields include
 * typical metadata such as the name, description, instruction links, and
 * transport details. Adjust the $fillable property according to your
 * database schema.
 */
class Shipment extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'name',
        'description',
        'shipment_type',
        'mode_of_transport',
        'shipment_instruction',
        'from_address',
        'to_address',
        'bu',
    ];
}
