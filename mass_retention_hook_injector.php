<?php
// mass_retention_hook_injector.php
require_once('wp-load.php');

$API_KEY = "REDACTED_API_KEY"; // User's Gemini API Key from previous scripts
$url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=" . $API_KEY;

// Get all published posts
$args = array(
    'post_type'      => 'post',
    'post_status'    => 'publish',
    'posts_per_page' => -1,
);
$posts = get_posts($args);

$total = count($posts);
$count = 0;

echo "Starting Retention Hook Injection for {$total} posts...\n";

foreach ($posts as $post) {
    $count++;
    echo "Processing Post ID: {$post->ID} ({$count}/{$total})...\n";

    // Check if it already has the hook to avoid duplicates
    if (strpos($post->post_content, 'What\'s Your Next Step') !== false || strpos($post->post_content, 'pm-retention-hook') !== false) {
        echo " - Hook already exists. Skipping.\n";
        continue;
    }

    // Get 2 random related posts (same category if possible, or just random)
    $categories = wp_get_post_categories($post->ID);
    $related_args = array(
        'post_type'      => 'post',
        'post_status'    => 'publish',
        'posts_per_page' => 2,
        'post__not_in'   => array($post->ID),
        'orderby'        => 'rand',
    );
    if (!empty($categories)) {
        $related_args['category__in'] = $categories;
    }
    
    $related_posts = get_posts($related_args);
    
    // If not enough related posts in category, get random ones
    if (count($related_posts) < 2) {
        $related_args = array(
            'post_type'      => 'post',
            'post_status'    => 'publish',
            'posts_per_page' => 2,
            'post__not_in'   => array($post->ID),
            'orderby'        => 'rand',
        );
        $related_posts = get_posts($related_args);
    }

    if (count($related_posts) < 2) {
        echo " - Not enough related posts. Skipping.\n";
        continue;
    }

    $rel_1 = $related_posts[0];
    $rel_2 = $related_posts[1];

    $prompt = "You are a highly professional smart assistant and an expert in interactive content creation. Your task is to write a 'Retention Hook' ending for an article about '{$post->post_title}'.

Rules (CRITICAL):
1. AI Persona: Do not sound like a boring blog post. Sound like an advanced AI assistant: clear, direct, combining scientific certainty with empathy for the user's needs.
2. No Fluff: Skip introductions. Go straight to the point.
3. The Retention Hook: Create a section titled '<h3>What's Your Next Step?</h3>'. You must present the user with a mental dilemma. Ask exactly two highly intriguing, exciting, and practical questions as bullet points.
These questions must be designed so the user feels they are missing out on a massive opportunity, a money-saving trick, or an important secret if they don't click. Use numbers, FOMO (Fear Of Missing Out), or mental challenges.
4. The two questions MUST act as hyperlinks pointing to these two topics:
Topic 1: '{$rel_1->post_title}' (Link: " . get_permalink($rel_1->ID) . ")
Topic 2: '{$rel_2->post_title}' (Link: " . get_permalink($rel_2->ID) . ")
5. Format the output in valid HTML. Wrap the entire output in a `<div class='pm-retention-hook' style='background-color: #f8fafc; border-left: 4px solid #2A7B4C; padding: 20px; margin-top: 40px; border-radius: 8px;'>` tag. Do not include markdown code block formatting (like ```html).";

    $payload = json_encode(array(
        "contents" => array(
            array(
                "parts" => array(
                    array("text" => $prompt)
                )
            )
        ),
        "generationConfig" => array(
            "temperature" => 0.7,
            "maxOutputTokens" => 1024
        )
    ));

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    
    $response = curl_exec($ch);
    $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpcode == 200) {
        $result = json_decode($response, true);
        if (isset($result['candidates'][0]['content']['parts'][0]['text'])) {
            $hook_html = trim($result['candidates'][0]['content']['parts'][0]['text']);
            // Clean up markdown if Gemini includes it
            $hook_html = preg_replace('/^```html/m', '', $hook_html);
            $hook_html = preg_replace('/```$/m', '', $hook_html);
            $hook_html = trim($hook_html);

            // Append to content
            $new_content = $post->post_content . "\n\n" . $hook_html;
            
            // Update post
            $update_args = array(
                'ID'           => $post->ID,
                'post_content' => $new_content
            );
            wp_update_post($update_args);
            echo " - Success! Injected retention hook.\n";
        } else {
            echo " - Failed to parse Gemini response.\n";
        }
    } else {
        echo " - API Error HTTP {$httpcode}\n";
    }
    
    // Sleep to respect API rate limits
    sleep(6);
}

echo "Injection Complete!\n";
?>
