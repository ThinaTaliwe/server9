<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('vessels', function (Blueprint $table) {
            $table->id();
            $table->string('imo_number')->unique();
            $table->string('name');
            $table->string('call_sign')->nullable();
            $table->string('mmsi')->nullable();
            $table->string('vessel_type')->nullable();
            $table->string('flag')->nullable();
            $table->decimal('length', 8, 2)->nullable();
            $table->decimal('beam', 8, 2)->nullable();
            $table->decimal('draft', 8, 2)->nullable();
            $table->decimal('gross_tonnage', 10, 2)->nullable();
            $table->geography('current_location', 'point', 4326)->nullable();
            $table->decimal('speed', 5, 2)->nullable();
            $table->decimal('course', 5, 2)->nullable();
            $table->foreignId('destination_port_id')->nullable();
            $table->timestamp('eta')->nullable();
            $table->timestamps();
            $table->softDeletes();
            $table->spatialIndex('current_location');
            $table->index(['imo_number', 'name']);
        });
    }
    public function down(): void { Schema::dropIfExists('vessels'); }
};
