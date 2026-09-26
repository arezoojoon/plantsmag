<?php
/**
 * Plugin Name: PlantsMag Premium Tools
 * Plugin URI: https://plantsmag.com
 * Description: Embeds Next.js Premium Tools for PlantsMag: Watering Calculator, AI Disease Finder, and Wedding Floral Pack.
 * Version: 2.0.0
 * Author: PlantsMag
 * Author URI: https://plantsmag.com
 * Text Domain: plantsmag-tools
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// 1. Watering Calculator Shortcode
add_shortcode('watering_calculator', function() {
    return '
    <div style="width: 100%; margin: 0 auto;">
        <iframe 
            src="https://app.72.62.93.117.nip.io/watering-calculator" 
            style="width: 100%; height: 900px; border: none; border-radius: 12px; overflow: hidden;"
            scrolling="yes">
        </iframe>
    </div>';
});

// 2. Plant Disease Finder Shortcode
add_shortcode('plant_disease_finder', function() {
    return '
    <div style="width: 100%; margin: 0 auto;">
        <iframe 
            src="https://app.72.62.93.117.nip.io/disease-finder" 
            style="width: 100%; height: 900px; border: none; border-radius: 12px; overflow: hidden;"
            allow="camera"
            scrolling="yes">
        </iframe>
    </div>';
});

// 3. Wedding Floral Pack Shortcode
add_shortcode('wedding_floral_pack', function() {
    return '
    <div style="width: 100%; margin: 0 auto;">
        <iframe 
            src="https://app.72.62.93.117.nip.io/wedding-flowers" 
            style="width: 100%; height: 900px; border: none; border-radius: 12px; overflow: hidden;"
            scrolling="yes">
        </iframe>
    </div>';
});
