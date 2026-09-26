<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class PlantsMag_Disease_Finder {

    // Using the keys provided by the user
    private $api_keys = array(
        'REDACTED_API_KEY', // plaantmag1
        'REDACTED_API_KEY', // plantsmag2
        'REDACTED_API_KEY'  // plantsmag3
    );

	public function __construct() {
		add_shortcode( 'plant_disease_finder', array( $this, 'render_shortcode' ) );
		add_action( 'wp_enqueue_scripts', array( $this, 'enqueue_assets' ) );
        
        // AJAX endpoint for processing image
        add_action( 'wp_ajax_pm_analyze_disease', array( $this, 'ajax_analyze_disease' ) );
        add_action( 'wp_ajax_nopriv_pm_analyze_disease', array( $this, 'ajax_analyze_disease' ) );
	}

	public function enqueue_assets() {
		global $post;
		if ( is_a( $post, 'WP_Post' ) && has_shortcode( $post->post_content, 'plant_disease_finder' ) ) {
			wp_enqueue_style( 'pm-disease-calc-css', get_template_directory_uri() . '/assets/css/disease-finder.css', array(), wp_get_theme()->get('Version') );
            
            // Note: For image processing, we just need standard JS, we don't enqueue a huge library.
			wp_enqueue_script( 'pm-disease-calc-js', get_template_directory_uri() . '/assets/js/disease-finder.js', array( 'jquery' ), wp_get_theme()->get('Version'), true );
            
            wp_localize_script( 'pm-disease-calc-js', 'pmDiseaseObj', array(
                'ajaxUrl' => admin_url( 'admin-ajax.php' ),
                'nonce' => wp_create_nonce( 'pm_disease_nonce' )
            ));
		}
	}

	public function render_shortcode( $atts ) {
		ob_start();
		?>
		<div class="pm-app-container pm-disease-app">
			<div class="pm-app-header pm-ai-header">
                <div class="pm-ai-badge">AI Powered</div>
				<h2>Plant Doctor</h2>
				<p>Upload a photo of your sick plant for instant diagnosis.</p>
			</div>

			<div class="pm-app-body">
                <div class="pm-upload-area" id="pm-upload-area">
                    <input type="file" id="pm-disease-image" accept="image/*" capture="environment" hidden>
                    <div class="pm-upload-content">
                        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                        <p>Tap to upload or take a photo</p>
                    </div>
                    <img id="pm-preview-img" style="display:none;" />
                </div>

				<button type="button" id="pm-analyze-btn" class="pm-btn-primary" disabled>Analyze Plant</button>
			</div>

            <!-- Loading Overlay -->
            <div id="pm-ai-loading" class="pm-loading-overlay">
                <div class="pm-spinner"></div>
                <p>AI is analyzing the leaves...</p>
            </div>

			<!-- Result Bottom Sheet -->
			<div id="pm-disease-result" class="pm-bottom-sheet">
                <div class="pm-sheet-handler"></div>
				<div class="pm-sheet-content">

					<!-- Diagnosis Title -->
					<h3 id="pm-diag-title" style="margin-bottom:4px;">Diagnosis</h3>
                    <div class="pm-diag-content">
                        <p id="pm-diag-text" style="color:rgba(255,255,255,0.6);font-size:0.9rem;line-height:1.6;"></p>
                    </div>

                    <!-- Danger Gauge (injected by JS) -->
                    <div id="pm-danger-gauge-wrap"></div>

					<!-- Treatment Roadmap (blurred until email captured) -->
                    <div class="pm-treatment-locked" id="pm-treatment-wrap">
                        <div style="padding:20px;text-align:center;color:rgba(255,255,255,0.3);font-size:0.85rem;">
                            <span style="font-size:24px;display:block;margin-bottom:8px;">🔒</span>
                            Treatment plan loading...
                        </div>
                    </div>

                    <!-- Affiliate Products (injected by JS) -->
                    <div id="pm-affiliate-wrap"></div>

                    <!-- Share Buttons (injected by JS) -->
                    <div id="pm-share-wrap"></div>

                    <button type="button" class="pm-btn-secondary" id="pm-close-disease" style="margin-top:16px;">Check Another Plant</button>
				</div>
			</div>
            <div id="pm-overlay-disease" class="pm-overlay"></div>
		</div>
		<?php
		return ob_get_clean();
	}

    public function ajax_analyze_disease() {
        check_ajax_referer( 'pm_disease_nonce', 'nonce' );

        if ( ! isset( $_POST['image_base64'] ) ) {
            wp_send_json_error( array( 'message' => 'No image provided.' ) );
        }

        // Clean base64 string
        $base64_string = $_POST['image_base64'];
        $base64_string = preg_replace('#^data:image/\w+;base64,#i', '', $base64_string);

        // Pick a random API key (poor man's load balancing from the 3 keys provided)
        $api_key = $this->api_keys[ array_rand( $this->api_keys ) ];
        
        $model = "gemini-1.5-flash"; // Flash is faster and cheaper, perfect for this.
        $url = "https://generativelanguage.googleapis.com/v1beta/models/{$model}:generateContent?key={$api_key}";

        $prompt = "You are an expert botanist and plant pathologist. Analyze this image of a plant.
        1. Identify the plant species if visible.
        2. Identify ANY visible diseases, pests, deficiencies, or stress signs.
        3. Assess severity honestly.
        4. Recommend specific treatment product (e.g. 'Neem Oil', 'Copper Fungicide', 'Hydrogen Peroxide 3%').

        Format your response EXACTLY as valid JSON (no markdown, no code blocks):
        {
            \"plant_name\": \"Common plant name or Unknown\",
            \"diagnosis\": \"Short name of the problem (e.g. Fungal Leaf Spot, Spider Mites)\",
            \"severity\": \"low|medium|high|critical\",
            \"explanation\": \"2-3 beginner-friendly sentences explaining what it is and why it happens.\",
            \"treatment_keyword\": \"Generic product name for Amazon search\",
            \"treatment_desc\": \"Exact step-by-step treatment: what to apply, how much, how often.\"
        }
        Output ONLY the JSON object. No other text.";

        $body = array(
            'contents' => array(
                array(
                    'parts' => array(
                        array( 'text' => $prompt ),
                        array(
                            'inline_data' => array(
                                'mime_type' => 'image/jpeg',
                                'data' => $base64_string
                            )
                        )
                    )
                )
            ),
            'generationConfig' => array(
                'temperature' => 0.4,
                'response_mime_type' => 'application/json'
            )
        );

        $response = wp_remote_post( $url, array(
            'body' => json_encode( $body ),
            'headers' => array(
                'Content-Type' => 'application/json'
            ),
            'timeout' => 30 // AI might take a moment
        ));

        if ( is_wp_error( $response ) ) {
            wp_send_json_error( array( 'message' => 'Failed to connect to AI server.' ) );
        }

        $body_response = wp_remote_retrieve_body( $response );
        $data = json_decode( $body_response, true );

        if ( isset( $data['candidates'][0]['content']['parts'][0]['text'] ) ) {
            $json_txt = $data['candidates'][0]['content']['parts'][0]['text'];
            // Clean up possible markdown formatting
            $json_txt = str_replace(array('```json', '```'), '', $json_txt);
            $result = json_decode( trim( $json_txt ), true );
            
            if ( $result ) {
                wp_send_json_success( $result );
            } else {
                wp_send_json_error( array( 'message' => 'AI returned an invalid format.' ) );
            }
        } else {
            wp_send_json_error( array( 'message' => 'AI could not process the image.' ) );
        }
    }
}

new PlantsMag_Disease_Finder();
