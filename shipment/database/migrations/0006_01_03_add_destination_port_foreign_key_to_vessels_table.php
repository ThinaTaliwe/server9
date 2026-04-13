<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::table('vessels', function (Blueprint $table) {
            $table->foreign('destination_port_id')
                ->references('id')
                ->on('ports')
                ->nullOnDelete();
        });
    }

    public function down(): void
    {
        Schema::table('vessels', function (Blueprint $table) {
            $table->dropForeign(['destination_port_id']);
        });
    }
};
