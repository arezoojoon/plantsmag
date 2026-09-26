<?php
// Ensure this runs in WP environment.
if ( !defined('ABSPATH') ) {
    require_once('wp-load.php');
}

// Helper to find page by slug
function get_page_by_slug($slug) {
    global $wpdb;
    $id = $wpdb->get_var( $wpdb->prepare("SELECT ID FROM $wpdb->posts WHERE post_name = %s AND post_type = 'page' AND post_status = 'publish'", $slug) );
    return $id;
}

// 1. Watering Calculator
$watering_content = <<<HTML
<div style="font-size: 1.15rem; line-height: 1.8; color: var(--color-text-body); max-width: 800px; margin: 0 auto;">
<p style="text-align:center; font-size: 1.3rem; margin-bottom: 3rem;">Never overwater or underwater your plants again. Simply select your plant species, pot size, and the lighting condition of your room. Our smart algorithm will generate a custom watering schedule for you.</p>

[watering_calculator]

<div class="affiliate-box" style="margin-top: 5rem;">
    <h3>Want to be 100% sure?</h3>
    <p>We highly recommend using a moisture meter before watering to physically check the soil moisture levels at the root zone.</p>
    <ul>
        <li><strong>Best Overall:</strong> <a href="#" target="_blank" rel="noopener sponsored">Gouevn Soil Moisture Meter</a></li>
        <li><strong>Best Self-Watering Pots:</strong> <a href="#" target="_blank" rel="noopener sponsored">Lechuza Premium Planters</a></li>
    </ul>
    <p><small style="color:var(--color-text-muted);">* As an Amazon Associate, we earn from qualifying purchases.</small></p>
</div>

<div style="margin-top: 4rem;">
    <h2>How does the watering calculator work?</h2>
    <p>Our smart algorithm accounts for the three most critical factors in houseplant care: <strong>Plant Species</strong>, <strong>Pot Material</strong>, and <strong>Light Conditions</strong>. For instance, terracotta pots are porous and allow soil to dry much faster than glazed ceramic or plastic pots. Similarly, a plant in bright indirect light transpires more water than one in a low-light corner. By combining these metrics, we generate an incredibly accurate baseline for your watering schedule.</p>
</div>
</div>
HTML;

wp_update_post(array(
    'ID' => get_page_by_slug('watering-calculator'),
    'post_content' => $watering_content
));

// 2. AI Disease Finder
$ai_content = <<<HTML
<div style="font-size: 1.15rem; line-height: 1.8; color: var(--color-text-body); max-width: 800px; margin: 0 auto;">
<p style="text-align:center; font-size: 1.3rem; margin-bottom: 2rem;">Is your Monstera turning yellow? Are there weird spots on your Calathea? Upload a clear photo of the affected leaf, and our AI bot will analyze it to identify the problem and suggest a cure.</p>

<div style="background: rgba(212,175,55,0.1); padding: 1.5rem; border-radius: var(--radius-sm); margin-bottom: 3rem; text-align: center;">
    <strong>Tips for best results:</strong> Ensure good lighting and focus the camera directly on the damaged area of the leaf or stem.
</div>

[plant_disease_finder]

<div class="affiliate-box" style="margin-top: 5rem; border-left-color: #e74c3c;">
    <h3 style="color: #c0392b;">Common Treatments (Recommended)</h3>
    <p>If the AI detects <strong>Pests/Bugs</strong> (like Spider Mites or Thrips): We recommend treating this with organic Neem Oil. <a href="#" target="_blank" rel="noopener sponsored">Get our favorite brand here.</a></p>
    <p>If the AI detects <strong>Fungal issues</strong> (like Powdery Mildew or Root Rot): A gentle fungicide will clear this up. <a href="#" target="_blank" rel="noopener sponsored">Try this highly-rated Fungicide.</a></p>
    <p><small style="color:var(--color-text-muted);">* As an Amazon Associate, we earn from qualifying purchases.</small></p>
</div>

<div style="margin-top: 4rem; padding: 2rem; background: var(--color-bg-base); border-radius: var(--radius-sm); border: 1px solid rgba(0,0,0,0.1);">
    <strong>Disclaimer:</strong> This tool uses advanced Artificial Intelligence (Gemini AI) for preliminary plant diagnosis. While highly accurate in detecting common houseplants ailments, always double-check treatments before applying heavy chemicals to your beloved plants.
</div>
</div>
HTML;

wp_update_post(array(
    'ID' => get_page_by_slug('plant-disease-finder'),
    'post_content' => $ai_content
));

// 3. About Us
$about_content = <<<HTML
<h2>Our Mission</h2>
<p>At PlantsMag, we believe that everyone has a green thumb—they just need the right tools and information. Our mission is to take the guesswork out of indoor plant care. Whether you are a beginner struggling to keep a succulent alive or an expert managing a lush indoor jungle, we are here to support your journey with science-backed advice, smart calculators, and AI diagnostics.</p>
<h2>Why Trust Us?</h2>
<p>Our team consists of passionate botanists, indoor gardeners, and houseplant enthusiasts. Every guide we publish is rigorously researched, and our tools are calibrated based on proven horticultural data. We don't just write about plants; we live with them.</p>
HTML;

wp_insert_post(array(
    'post_title' => 'About Us',
    'post_name' => 'about-us',
    'post_content' => $about_content,
    'post_status' => 'publish',
    'post_type' => 'page'
));

// 4. Affiliate Disclosure
$affiliate_content = <<<HTML
<h2>Transparency is our policy.</h2>
<p>PlantsMag.com is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. We may earn a small commission for purchases made through links in our posts at no additional cost to you.</p>
<p>We only recommend products that we genuinely believe in and that we would use on our own houseplants. The small commissions we receive help keep our smart tools (like the Watering Calculator and AI Plant Doctor) completely free for everyone to use.</p>
HTML;

wp_insert_post(array(
    'post_title' => 'Affiliate Disclosure',
    'post_name' => 'affiliate-disclosure',
    'post_content' => $affiliate_content,
    'post_status' => 'publish',
    'post_type' => 'page'
));

// 5. Privacy Policy update
global $wpdb;
$privacy_id = $wpdb->get_var( "SELECT ID FROM $wpdb->posts WHERE post_name = 'privacy-policy' AND post_type = 'page'" );
if($privacy_id) {
    wp_update_post(array(
        'ID' => $privacy_id,
        'post_status' => 'publish'
    ));
}

// 6. Template Article
$article_content = <<<HTML
<div style="background:var(--color-bg-base); padding:2rem; border-radius:var(--radius-sm); margin-bottom:2rem; border: 1px solid rgba(0,0,0,0.05);">
<h3 style="margin-top:0;">🌿 Quick Care Facts: Snake Plant (Sansevieria)</h3>
<ul style="margin-bottom:0;">
<li><strong>Light:</strong> Low to bright indirect light. Very adaptable.</li>
<li><strong>Water:</strong> Every 2-3 weeks. Allow soil to dry completely.</li>
<li><strong>Soil:</strong> Well-draining cactus/succulent mix.</li>
<li><strong>Toxicity:</strong> Mildly toxic to pets.</li>
</ul>
</div>

<p>The Snake Plant, also known as the Mother-in-Law's Tongue, is virtually indestructible, making it the perfect choice for beginners.</p>

<h2>How Much Water Does a Snake Plant Need?</h2>
<p>Overwatering is the number one killer of Sansevieria. They store water in their fleshy leaves and require very little additional hydration.</p>

<div class="affiliate-box" style="margin: 3rem 0; text-align: center; border-left:none; border:2px dashed var(--color-primary-light);">
    <h3 style="color:var(--color-primary-light); margin-bottom:0.5rem; border:none;">Watering Anxiety?</h3>
    <p style="margin-bottom:1.5rem;">Not sure exactly when to water your new Snake Plant? Take the guesswork out.</p>
    <a href="/watering-calculator" class="btn btn-primary">Use our Free Smart Watering Calculator &rarr;</a>
</div>

<h2>Best Soil for Snake Plants</h2>
<p>Because they are prone to root rot if left in standing water, you must use a highly aerated soil mix. We recommend mixing standard indoor potting soil with perlite and pumice.</p>

<p><em>Pro Tip: You can grab our favorite <a href="#" target="_blank" rel="noopener sponsored">pre-mixed succulent soil on Amazon</a> to save time.</em></p>

<h2>Common Problems: Yellowing Leaves</h2>
<p>If the leaves of your Snake Plant are turning yellow and mushy at the base, it is suffering from root rot. You will need to unpot the plant, cut away the rotting roots, and repot in fresh, dry soil.</p>
<p>Not sure if it's root rot or a fungal infection? <a href="/plant-disease-finder" style="font-weight:bold;">Upload a photo to our AI Plant Doctor</a> for an instant diagnosis!</p>
HTML;

wp_insert_post(array(
    'post_title' => '[TEMPLATE] The Ultimate Care Guide for Snake Plants',
    'post_name' => 'snake-plant-care-template',
    'post_content' => $article_content,
    'post_status' => 'draft',
    'post_type' => 'post'
));

echo "CONTENT INJECTED SUCCESSFULLY";
?>
