<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class PlantsMag_Watering_Calculator {

	public function __construct() {
		add_shortcode( 'watering_calculator', array( $this, 'render_shortcode' ) );
		add_action( 'wp_enqueue_scripts', array( $this, 'enqueue_assets' ) );
	}

	public function enqueue_assets() {
		global $post;
		// Only load assets if the shortcode is on the page
		if ( is_a( $post, 'WP_Post' ) && has_shortcode( $post->post_content, 'watering_calculator' ) ) {
			wp_enqueue_style( 'pm-watering-calc-css', get_template_directory_uri() . '/assets/css/watering-calculator.css', array(), wp_get_theme()->get('Version') );
			wp_enqueue_script( 'pm-watering-calc-js', get_template_directory_uri() . '/assets/js/watering-calculator.js', array( 'jquery' ), wp_get_theme()->get('Version'), true );
            
            // Pass any needed variables to JS
            wp_localize_script( 'pm-watering-calc-js', 'pmCalcObj', array(
                'ajaxUrl' => admin_url( 'admin-ajax.php' )
            ));
		}
	}

	public function render_shortcode( $atts ) {
		ob_start();
		?>
		<div class="pm-app-container pm-calculator-app">
			<div class="pm-app-header">
				<h2>Smart Watering Calculator</h2>
				<p>Find out exactly when to water your plants.</p>
			</div>

			<form id="pm-watering-form" class="pm-app-body">
				<!-- Plant Type -->
				<div class="pm-input-group">
					<label for="plant-type">Plant Type</label>
					<div class="pm-select-wrapper">
						<select id="plant-type" required>
							<option value="" disabled selected>Select your plant...</option>
							<option value="succulent">Succulent / Aloe</option>
							<option value="cactus">Cactus</option>
							<option value="tropical">Monstera / Tropical</option>
							<option value="monstera">Monstera Deliciosa</option>
							<option value="pothos">Pothos / Epipremnum</option>
							<option value="fern">Fern / Calathea</option>
							<option value="snake">Snake Plant / ZZ Plant</option>
							<option value="orchid">Orchid / Phalaenopsis</option>
							<option value="peace">Peace Lily</option>
							<option value="herb">Indoor Herb</option>
						</select>
					</div>
				</div>

				<!-- Temperature Range -->
				<div class="pm-input-group">
					<label>Room Temperature</label>
					<div class="pm-options-row">
						<label class="pm-radio-card">
							<input type="radio" name="temperature-range" id="temp-cold" value="cold">
							<span class="pm-card-content">Cool<br><small>10–18°C / 50–65°F</small></span>
						</label>
						<label class="pm-radio-card">
							<input type="radio" name="temperature-range" id="temp-mild" value="mild" checked>
							<span class="pm-card-content">Mild<br><small>18–25°C / 65–77°F</small></span>
						</label>
						<label class="pm-radio-card">
							<input type="radio" name="temperature-range" id="temp-warm" value="warm">
							<span class="pm-card-content">Warm<br><small>25–32°C / 77–90°F</small></span>
						</label>
						<label class="pm-radio-card">
							<input type="radio" name="temperature-range" id="temp-hot" value="hot">
							<span class="pm-card-content">Hot 🌞<br><small>32–45°C / 90°F+ (UAE)</small></span>
						</label>
					</div>
				</div>

				<!-- Pot Material -->
				<div class="pm-input-group">
					<label>Pot Material</label>
					<div class="pm-options-row">
						<label class="pm-radio-card">
							<input type="radio" name="pot-type" value="terracotta" required>
							<span class="pm-card-content">Terracotta<br><small>Dries fastest</small></span>
						</label>
						<label class="pm-radio-card">
							<input type="radio" name="pot-type" value="plastic">
							<span class="pm-card-content">Plastic<br><small>Standard</small></span>
						</label>
						<label class="pm-radio-card">
							<input type="radio" name="pot-type" value="ceramic">
							<span class="pm-card-content">Ceramic<br><small>Holds more</small></span>
						</label>
						<label class="pm-radio-card">
							<input type="radio" name="pot-type" value="self-water">
							<span class="pm-card-content">Self-Water<br><small>Reservoir</small></span>
						</label>
					</div>
				</div>

                <!-- Light Conditions -->
                <div class="pm-input-group">
					<label>Light Conditions</label>
					<div class="pm-options-row">
						<label class="pm-radio-card">
							<input type="radio" name="light-level" value="low" required>
							<span class="pm-card-content">Low Light</span>
						</label>
						<label class="pm-radio-card">
							<input type="radio" name="light-level" value="medium">
							<span class="pm-card-content">Medium</span>
						</label>
                        <label class="pm-radio-card">
							<input type="radio" name="light-level" value="bright">
							<span class="pm-card-content">Bright Indirect</span>
						</label>
						<label class="pm-radio-card">
							<input type="radio" name="light-level" value="direct-sun">
							<span class="pm-card-content">Direct Sun</span>
						</label>
					</div>
				</div>

				<button type="submit" class="pm-btn-primary">Calculate Schedule →</button>
			</form>

			<!-- Result Bottom Sheet -->
			<div id="pm-result-sheet" class="pm-bottom-sheet">
                <div class="pm-sheet-handler"></div>
				<div class="pm-sheet-content">
					<h3>Your Watering Schedule 💧</h3>
					<div class="pm-result-highlight">
						<span id="pm-days-result">7</span>
						<small>Days Between Waterings</small>
					</div>
					<p class="pm-result-desc" id="pm-result-message"></p>

                    <!-- ET Formula Breakdown (injected by JS) -->
                    <div id="pm-et-breakdown-wrap"></div>

					<!-- Affiliate Products (injected by JS) -->
                    <div id="pm-affiliate-wrap"></div>

                    <!-- Weekly Plan Lead Gate (injected by JS) -->
                    <div id="pm-weekly-gate-wrap"></div>

                    <!-- Share (injected by JS) -->
                    <div id="pm-water-share-wrap"></div>

                    <button type="button" class="pm-btn-secondary" id="pm-close-sheet" style="margin-top:16px;">Recalculate</button>
				</div>
			</div>
            <div id="pm-overlay" class="pm-overlay"></div>
		</div>
		<?php
		return ob_get_clean();
	}
}

new PlantsMag_Watering_Calculator();
