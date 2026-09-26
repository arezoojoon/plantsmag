<?php
/**
 * PlantsMag Lead Capture Endpoint
 * POST /wp-json/pm/v1/capture-lead
 *
 * Receives lead data from Disease Finder & Watering Calculator
 * and forwards to n8n Webhook for email processing.
 *
 * Place in: public_html/lead-capture.php
 * OR: register as part of functions.php (see below)
 */

// ─── Also callable as standalone PHP ─────────────────────────
if (!defined('ABSPATH')) {
    require_once(dirname(__FILE__) . '/wp-load.php');
}

/**
 * Register REST API route
 */
add_action('rest_api_init', function() {
    register_rest_route('pm/v1', '/capture-lead', [
        'methods'             => 'POST',
        'callback'            => 'pm_handle_lead_capture',
        'permission_callback' => '__return_true', // Public endpoint
        'args' => [
            'email'         => ['required' => true, 'type' => 'string', 'sanitize_callback' => 'sanitize_email'],
            'lead_type'     => ['required' => false, 'type' => 'string', 'default' => 'disease'],
            'disease_name'  => ['required' => false, 'type' => 'string'],
            'plant_name'    => ['required' => false, 'type' => 'string'],
            'severity'      => ['required' => false, 'type' => 'string', 'default' => 'medium'],
            'treatment_keyword' => ['required' => false, 'type' => 'string'],
            'asin'          => ['required' => false, 'type' => 'string'],
            'explanation'   => ['required' => false, 'type' => 'string'],
            'watering_days' => ['required' => false, 'type' => 'integer'],
        ],
    ]);
});

/**
 * Handle lead capture
 */
function pm_handle_lead_capture(WP_REST_Request $request): WP_REST_Response {
    $email = sanitize_email($request->get_param('email'));
    
    if (!is_email($email)) {
        return new WP_REST_Response(['success' => false, 'message' => 'Invalid email'], 400);
    }
    
    $lead_data = [
        'email'             => $email,
        'lead_type'         => sanitize_text_field($request->get_param('lead_type')     ?? 'disease'),
        'disease_name'      => sanitize_text_field($request->get_param('disease_name')  ?? ''),
        'plant_name'        => sanitize_text_field($request->get_param('plant_name')    ?? ''),
        'severity'          => sanitize_text_field($request->get_param('severity')      ?? 'medium'),
        'treatment_keyword' => sanitize_text_field($request->get_param('treatment_keyword') ?? ''),
        'asin'              => sanitize_text_field($request->get_param('asin')          ?? ''),
        'explanation'       => sanitize_textarea_field($request->get_param('explanation') ?? ''),
        'watering_days'     => intval($request->get_param('watering_days') ?? 0),
        'source_url'        => substr(sanitize_url($request->get_header('referer') ?? ''), 0, 500),
        'timestamp'         => current_time('mysql'),
        // IP removed for GDPR compliance
    ];
    
    // 1. Log to WordPress options (simple DB storage)
    pm_log_lead($lead_data);
    
    // 2. Forward to n8n Webhook (async — don't block response)
    $n8n_webhook = 'http://72.62.93.117:5678/webhook/plantsmag-lead';
    
    wp_remote_post($n8n_webhook, [
        'headers'   => ['Content-Type' => 'application/json'],
        'body'      => wp_json_encode($lead_data),
        'timeout'   => 8,
        'blocking'  => false, // Non-blocking — fire and forget
        'sslverify' => false,
    ]);
    
    return new WP_REST_Response([
        'success' => true,
        'message' => 'Thank you! Check your email for your personalized plan.',
    ], 200);
}

/**
 * Simple lead logger to WP options table
 */
function pm_log_lead(array $lead): void {
    global $wpdb;
    
    $table = $wpdb->prefix . 'pm_leads';
    
    // Create table if not exists (first run)
    $like_table = $wpdb->esc_like($table);
    if ($wpdb->get_var("SHOW TABLES LIKE '{$like_table}'") !== $table) {
        $wpdb->query("CREATE TABLE IF NOT EXISTS {$table} (
            id          BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
            email       VARCHAR(200) NOT NULL,
            lead_type   VARCHAR(50)  DEFAULT 'disease',
            disease_name VARCHAR(200) DEFAULT '',
            plant_name  VARCHAR(200) DEFAULT '',
            severity    VARCHAR(50)  DEFAULT 'medium',
            asin        VARCHAR(20)  DEFAULT '',
            watering_days INT DEFAULT 0,
            source_url  TEXT,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY email (email),
            KEY created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;");
    }
    
    $wpdb->insert($table, [
        'email'        => $lead['email'],
        'lead_type'    => $lead['lead_type'],
        'disease_name' => $lead['disease_name'],
        'plant_name'   => $lead['plant_name'],
        'severity'     => $lead['severity'],
        'asin'         => $lead['asin'],
        'watering_days'=> $lead['watering_days'],
        'source_url'   => $lead['source_url'],
    ], ['%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s']);
}

/**
 * Admin page: view leads (accessible from WP Admin → Tools → PM Leads)
 */
add_action('admin_menu', function() {
    add_management_page(
        'PlantsMag Leads',
        '🌿 PM Leads',
        'manage_options',
        'pm-leads',
        'pm_leads_admin_page'
    );
});

function pm_leads_admin_page(): void {
    global $wpdb;
    $table = $wpdb->prefix . 'pm_leads';
    
    // Check table exists
    $like_table = $wpdb->esc_like($table);
    if ($wpdb->get_var("SHOW TABLES LIKE '{$like_table}'") !== $table) {
        echo '<div class="wrap"><h1>PlantsMag Leads</h1><p>No leads yet. The table will be created on first capture.</p></div>';
        return;
    }
    
    $total  = $wpdb->get_var("SELECT COUNT(*) FROM {$table}");
    $today  = $wpdb->get_var("SELECT COUNT(*) FROM {$table} WHERE DATE(created_at) = CURDATE()");
    $leads  = $wpdb->get_results("SELECT * FROM {$table} ORDER BY created_at DESC LIMIT 100");
    
    echo '<div class="wrap">';
    echo '<h1>🌿 PlantsMag Lead Dashboard</h1>';
    echo "<p><strong>Total Leads:</strong> {$total} &nbsp;|&nbsp; <strong>Today:</strong> {$today}</p>";
    
    echo '<table class="wp-list-table widefat fixed striped">';
    echo '<thead><tr><th>Email</th><th>Type</th><th>Disease/Plant</th><th>Severity</th><th>Date</th></tr></thead>';
    echo '<tbody>';
    
    foreach ($leads as $lead) {
        echo '<tr>';
        echo '<td>' . esc_html($lead->email) . '</td>';
        echo '<td>' . esc_html($lead->lead_type) . '</td>';
        echo '<td>' . esc_html($lead->disease_name ?: $lead->plant_name) . '</td>';
        echo '<td>' . esc_html($lead->severity) . '</td>';
        echo '<td>' . esc_html($lead->created_at) . '</td>';
        echo '</tr>';
    }
    
    echo '</tbody></table></div>';
}
