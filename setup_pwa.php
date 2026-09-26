<?php
$logo_url = wp_get_attachment_url( 18 ); 
if ( ! $logo_url ) {
    $logo_url = wp_get_attachment_url( 16 ); 
}
$opts = array( 
    'adv_setting' => 1, 
    'app_name' => 'PlantsMag', 
    'app_short_name' => 'PlantsMag', 
    'theme_color' => '#2A7B4C', 
    'background_color' => '#FFFFFF', 
    'icon' => $logo_url, 
    'splash_icon' => $logo_url,
    'start_url' => '/',
    'orientation' => 'portrait'
); 
update_option( 'pwaforwp_settings', $opts );
echo "PWA Settings updated with logo: " . $logo_url;
