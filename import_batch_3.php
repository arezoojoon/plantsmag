<?php
// Load WP
if ( !defined('ABSPATH') ) {
    require_once('wp-load.php');
}
require_once(ABSPATH . 'wp-admin/includes/media.php');
require_once(ABSPATH . 'wp-admin/includes/file.php');
require_once(ABSPATH . 'wp-admin/includes/image.php');

$articles = [
    [
        'title' => 'Calathea (Calathea spp.): The Prayer Plant Care Masterclass',
        'slug'  => 'calathea-prayer-plant-care-masterclass',
        'image' => '/home/u284669846/domains/plantsmag.com/public_html/tmp_images/calathea_cover.png',
        'content' => '
<h2>The Mesmerizing Moving Plant</h2>
<p>Few houseplants command as much attention—or require as much precise care—as the Calathea. Belonging to the Marantaceae family and widely known as "Prayer Plants," Calatheas are famous for their stunning, highly decorative foliage that features intricate patterns of stripes, spots, and deep purple undersides. But their most magical trait is their movement. In a phenomenon known as nyctinasty, Calathea leaves fold up at night like hands in prayer, and lower back down during the day to catch the sunlight.</p>
<p>While breathtakingly beautiful, Calatheas have earned a reputation as "diva" plants of the indoor gardening world. They demand specific conditions to thrive, but once you understand their needs, keeping them pristine is entirely manageable.</p>

<h2>Water Quality: The Ultimate Dealbreaker</h2>
<p>If you take away only one piece of advice from this guide, let it be this: <strong>Do not water your Calathea with tap water</strong>. Calatheas are exquisitely sensitive to the chlorine, fluoride, and hard minerals found in standard municipal water supplies. If you use tap water, you will almost immediately begin to see brown, crispy edges forming on the leaves.</p>
<p>To keep the foliage pristine, you must water with distilled water, filtered water (like from a ZeroWater pitcher), or collected rainwater. The soil should be kept lightly and evenly moist, like a wrung-out sponge. Never let it dry out completely, but also ensure it is never waterlogged.</p>

<div class="affiliate-box">
    <h3>Are You Overwatering Your Calathea?</h3>
    <p>Calatheas hate soggy roots just as much as they hate bone-dry soil. Get the perfect mathematical interval for watering.</p>
    <a href="/watering-calculator/" class="btn btn-outline">Generate Custom Watering Schedule</a>
</div>

<h2>Mastering Jungle Humidity Levels</h2>
<p>Hailing from the understory of tropical rainforests in the Americas, Calatheas absolutely require high humidity to prevent their thin, papery leaves from crisping at the edges. A standard home environment in winter (with central heating running) might drop to 20-30% humidity. A Calathea needs at least 50%, with 60-70% being ideal.</p>
<p>Misting the leaves is a common myth—it does not significantly raise the ambient humidity and can actually invite fungal diseases. Instead, invest in a good quality indoor humidifier, or group your Calathea with other tropical plants to create a microclimate of moisture.</p>

<h2>Lighting without Scorching</h2>
<p>Because they grow on the forest floor, Calatheas evolved to capture filtered light through the canopy above. Direct sunlight will bleach their intricate patterns and physically burn the leaves. Provide them with medium to bright <em>indirect</em> light. A north or east-facing window is perfect. If you only have south-facing windows, pull the plant several feet back into the room or use a sheer curtain to diffuse the light.</p>

<h2>Common Ailments: Spider Mites and Crisping</h2>
<p>The thin leaves of the Calathea are a magnet for spider mites, especially in dry, low-humidity homes. If you notice a faint, web-like substance near the stems, or if the leaves start to look dull and speckled, you likely have an infestation. Wipe the leaves down with neem oil immediately.</p>

<div class="affiliate-box">
    <h3>Is Your Calathea Turning Yellow?</h3>
    <p>Don’t lose your prized plant. Snap a quick picture of the affected leaf and let our AI diagnose the exact problem instantly.</p>
    <a href="/plant-disease-finder/" class="btn btn-primary">Diagnose My Plant Automatically</a>
</div>
        '
    ],
    [
        'title' => 'Aloe Vera: How to Grow the Ultimate Medicinal Succulent',
        'slug'  => 'aloe-vera-medicinal-succulent-care-guide',
        'image' => '/home/u284669846/domains/plantsmag.com/public_html/tmp_images/aloe_vera_cover.png',
        'content' => '
<h2>The "Plant of Immortality"</h2>
<p>Known by the ancient Egyptians as the "Plant of Immortality," the Aloe Vera is one of the oldest known medicinal plants in the world. Its thick, fleshy, serrated leaves contain a clear, cooling gel packed with vitamins, enzymes, and amino acids that has been used for millennia to treat sunburns, minor cuts, and skin irritations.</p>
<p>Aside from its incredible utility, Aloe Vera is an architectural beauty that adds a fresh, modern aesthetic to any sunny windowsill. As a succulent, it is incredibly low-maintenance—provided you understand the golden rules of desert plant care.</p>

<h2>Lighting: Chasing the Sun</h2>
<p>Aloe Vera loves light. Unlike tropical understory plants (like Pothos or Calathea) that thrive in the shadows, Aloe Vera requires several hours of bright, direct sunlight every day to thrive. A south-facing or west-facing window is ideal.</p>
<p>However, be cautious if you are moving a shade-grown Aloe suddenly into blasting summer sun—it can sunburn! (Yes, the sunburn-curing plant can get sunburned itself). Sunburn on an Aloe presents as brown or reddish-purple discoloration on the green leaves. If you see this, move the plant back slightly until it acclimates.</p>

<h2>Watering: Replicating Desert Droughts</h2>
<p>The fastest way to kill an Aloe Vera is with kindness (and a heavy watering can). Their thick leaves act as massive water storage tanks designed to survive months of drought. You must allow the potting soil to dry out 100% completely before watering again.</p>
<p>During the summer active growing season, you may water every 2-3 weeks. In the winter, the plant goes fully dormant, and you might only need to water it once every month or two. When you do water, soak it until water runs out the bottom, taking care not to let water sit in the rosette (the central crown of the plant) to prevent rot.</p>

<div class="affiliate-box">
    <h3>Stop Rotting Your Aloe Roots!</h3>
    <p>Succulents have vastly different watering needs than tropicals. Select "Cactus/Succulent Soil" in our tool to get the perfect cycle.</p>
    <a href="/watering-calculator/" class="btn btn-outline">Get Your Succulent Watering Schedule</a>
</div>

<h2>The Perfect Pot and Soil Setup</h2>
<p>Aloe Vera commands excellent drainage. Never put an Aloe in a pot without drainage holes. Terracotta pots are the absolute best choice for Aloes because the porous clay allows the soil to breathe and dry out faster, preventing the dreaded root rot.</p>
<p>Standard indoor potting soil stays wet far too long for an Aloe. You must use a specialized cactus & succulent mix, or amend your regular soil heavily with coarse sand, perlite, or pumice to ensure water drains through it almost instantly.</p>

<h2>Harvesting the Gel Safely</h2>
<p>When you need to harvest the medicinal gel, always cut one of the oldest, outermost leaves from the base of the plant using a sharp, sterilized knife. Never cut a piece out of the center leaves, as this will stall the plant’s growth. Slice the leaf open longitudinally and scrape the clear gel out with a spoon. You can store leftover gel in the refrigerator for up to a week.</p>

<div class="affiliate-box">
    <h3>Are Your Aloe Leaves Getting Mushy?</h3>
    <p>Mushy, translucent leaves are a red flag for root rot. Have our AI Doctor analyze the leaf base right now.</p>
    <a href="/plant-disease-finder/" class="btn btn-primary">Scan My Aloe Now</a>
</div>
        '
    ],
    [
        'title' => 'English Ivy (Hedera helix): Indoor Growth and Pest Control',
        'slug'  => 'english-ivy-hedera-helix-indoor-pest-control',
        'image' => '/home/u284669846/domains/plantsmag.com/public_html/tmp_images/english_ivy_cover.png',
        'content' => '
<h2>Bringing the English Countryside Indoors</h2>
<p>English Ivy (Hedera helix) is steeped in history and romance, known for cloaking the walls of ancient universities and historic manors. Brought perfectly indoors, it’s a vigorous trailer that cascades beautifully from hanging baskets or climbs up trellises with ease. Beyond its undeniable classic aesthetic, English Ivy ranks highly on the list of air-purifying plants, actively filtering out toxins like formaldehyde and airborne fecal matter.</p>
<p>However, transitioning this robust outdoor survivor into a successful indoor houseplant requires understanding two critical factors: exactly how much light it tolerates and how to defend it against its ultimate nemesis: the spider mite.</p>

<h2>Light and Temperature Demands</h2>
<p>One of the biggest misconceptions about English Ivy is that it’s a low-light indoor plant. While it can survive deep shade outdoors, indoor ivy needs bright, indirect light to maintain its vigorous growth and vibrant variegation. If placed in a dark corner, a variegated ivy will lose its white and golden patterns, reverting to solid dark green as it struggles to photosynthesize.</p>
<p>Furthermore, English Ivy fundamentally dislikes hot, stuffy environments. It thrives in cool to moderate temperatures—ideally between 50°F and 70°F (10°C to 21°C). Keeping it near a cool window or in a well-ventilated room will keep it far happier than placing it near a radiator or heat vent.</p>

<h2>Moisture Balance: Avoiding Crisp Leaves</h2>
<p>English Ivy prefers to be kept evenly moist during its growing season, taking issue with both bone-dry soil and water-logged roots. A good rule of thumb is to water when the top inch of soil feels dry. Drooping vines accompanied by dry, crispy leaves almost always indicate severe underwatering, whereas yellowing leaves often point to an overly soggy root zone.</p>

<div class="affiliate-box">
    <h3>Perfecting the Ivy Moisture Balance</h3>
    <p>Because Ivy is so sensitive to drying out, timing your watering is critical. Let our Smart Tool calculate the exact day your ivy needs a drink.</p>
    <a href="/watering-calculator/" class="btn btn-outline">Check My Watering Interval</a>
</div>

<h2>The Arch-Nemesis: Spider Mites</h2>
<p>If you own an indoor English Ivy, you must remain perpetually vigilant for Spider Mites. These microscopic arachnids love the thin, dry leaves of the ivy, especially in winter when home heating dries out the air.</p>
<p><strong>Signs of an invasion:</strong> The ivy leaves begin to look pale, dull, or stippled with tiny yellow dots. If you look closely at the nodes where the leaf meets the stem, you may see super-fine webbing. <br>
<strong>The Solution:</strong> Spider mites hate moisture. The easiest preventative measure is to physically wash your ivy in the shower every few weeks to blast away the pests. If an infestation occurs, spray thoroughly with insecticidal soap or neem oil every 7 days until cleared.</p>

<div class="affiliate-box">
    <h3>Is Your Ivy Losing Leaves?</h3>
    <p>Don’t let a hidden pest infestation destroy your cascading ivy! Upload a photo of the affected leaves, and our AI will detect microscopic issues.</p>
    <a href="/plant-disease-finder/" class="btn btn-primary">Diagnose Pest Problems Instantly</a>
</div>
        '
    ],
    [
        'title' => 'Phalaenopsis Orchid: The Foolproof Beginner Orchid Guide',
        'slug'  => 'phalaenopsis-moth-orchid-foolproof-guide',
        'image' => '/home/u284669846/domains/plantsmag.com/public_html/tmp_images/orchid_cover.png',
        'content' => '
<h2>Demystifying the "Moth Orchid"</h2>
<p>For decades, orchids were considered the ultimate challenge for indoor gardeners—fragile, temperamental, and reserved only for expert botanists with automated greenhouses. Then came the widespread cultivation of the Phalaenopsis, or "Moth Orchid." Today, it is arguably the most common and beloved flowering houseplant on the market, readily available everywhere from luxury florists to neighborhood grocery stores.</p>
<p>The truth about the Phalaenopsis is that it is remarkably hardy and resilient, provided you stop treating it like a normal houseplant. Placed in traditional potting soil, an orchid will die. Understanding its unique biology is the key to enjoying blooms that last for three to six months at a time.</p>

<h2>Epiphytic Biology: Why Bark is Better than Dirt</h2>
<p>In the wild jungles of Asia and Australia, Phalaenopsis orchids do not grow in the ground. They are <em>epiphytes</em>, meaning they grow clinging to the bark of trees high up in the canopy. Their thick, silvery roots are designed to absorb moisture directly from the humid air and sudden tropical downpours, while enjoying massive amounts of air circulation.</p>
<p>This is why you must never use standard potting soil. Orchids require a specialized orchid mix, typically composed of large chunks of fir bark, charcoal, and chunky perlite, which ensures the roots can breathe. If the roots are suffocated by dense, wet dirt, they will rot within weeks.</p>

<h2>The Ice Cube Myth and Proper Watering</h2>
<p>You may have seen tags suggesting you water an orchid with three ice cubes a week. <strong>Do not do this.</strong> Orchids are tropical plants; shocking their roots with freezing ice water can cause long-term cellular damage. Furthermore, three melting ice cubes rarely saturate the bark enough to thoroughly hydrate the roots.</p>
<p>The correct way to water a Phalaenopsis is to wait until the roots turn from bright green to a silvery-white color (usually every 7-10 days). Then, take the plastic nursery pot to the sink and run lukewarm water generously through the bark for a full minute. Let it drain completely before putting it back in its decorative cachepot. Never let water sit in the crown of the leaves, as this causes crown rot.</p>

<div class="affiliate-box">
    <h3>Stop Guessing with Orchid Watering</h3>
    <p>Bark substrate dries out entirely differently than soil. Input your pot type and lighting into our calculator to avoid under-watering your blooms.</p>
    <a href="/watering-calculator/" class="btn btn-outline">Calculate Custom Watering Schedule</a>
</div>

<h2>Lighting and Getting Them to Re-Bloom</h2>
<p>Moth orchids prefer bright, indirect light. An eastern-facing window is ideal. Direct, hot sunlight will quickly scorch their leathery leaves. Once the massive flower spike finally drops its last bloom, don’t throw the plant away! Cut the spike down to an inch above the base.</p>
<p>To trigger a new bloom cycle the following year, the orchid needs a temperature drop. Exposing the plant to nighttime temperatures around 55-65°F (13-18°C) for several weeks in the autumn will naturally signal the plant to send up a brand new spike.</p>

<div class="affiliate-box">
    <h3>Are Your Orchid Roots Mushy and Brown?</h3>
    <p>Healthy roots should be firm and green or silver. If they look brown and mushy, snap a picture. Our AI Plant Doctor will tell you how to save it.</p>
    <a href="/plant-disease-finder/" class="btn btn-primary">Diagnose Root Rot Immediately</a>
</div>
        '
    ],
    [
        'title' => 'Boston Fern (Nephrolepis exaltata): Mastering Indoor Humidity',
        'slug'  => 'boston-fern-nephrolepis-exaltata-humidity-care',
        'image' => '/home/u284669846/domains/plantsmag.com/public_html/tmp_images/fern_cover.png',
        'content' => '
<h2>The Ultimate Victorian Classic</h2>
<p>During the Victorian era, owning a sprawling, verdant Boston Fern (Nephrolepis exaltata) was considered a massive status symbol of wealth and elegance. Today, they remain incredibly popular, especially for hanging baskets where their delicate, feathery fronds can cascade gracefully in all directions, creating a lush, prehistoric indoor jungle vibe.</p>
<p>However, the Boston Fern is infamous for one specific issue: the relentless shedding of dry, brown leaflets everywhere if its strict environmental demands are not met. The secret to a perfect, non-shedding Boston Fern lies entirely in mastering hydration—both in the soil and in the air.</p>

<h2>The Golden Rule: Never Let the Soil Dry Out</h2>
<p>Unlike succulents, pothos, or ZZ plants that prefer a dry-out period, the Boston Fern cannot tolerate dry soil for even a single day. In its natural tropical wetland habitat, it grows in a constant state of dampness. You must keep the soil consistently, evenly moist (like a damp sponge) at all times. If the soil surface feels dry to the touch, you are already slightly late to water it.</p>
<p>Self-watering pots or placing the fern in a humid bathroom are excellent strategies for maintaining this constant level of moisture. When you do water, ensure it is thoroughly soaked, but avoid letting the pot sit in stagnant water to prevent rotting the dense root ball.</p>

<div class="affiliate-box">
    <h3>The Fine Line Between Moist and Soggy</h3>
    <p>Ferns require precise watering cadences. Input your room’s environment into our Smart Calculator so you never let your fern dry out again.</p>
    <a href="/watering-calculator/" class="btn btn-outline">Generate Precise Fern Watering Schedule</a>
</div>

<h2>Humidity: The Key to Green Fronds</h2>
<p>Watering the roots is only half the battle. The delicate leaflets of a Boston Fern will rapidly crisp up and turn brown if the ambient air is too dry. This is the main reason ferns struggle in modern, centrally-heated winter homes where humidity plummets below 30%.</p>
<p>To keep a Boston Fern looking lush, you must provide a high-humidity microclimate (at least 60% relative humidity). Ways to achieve this include:</p>
<ul>
    <li>Running a dedicated indoor humidifier near the plant.</li>
    <li>Hanging the fern in a brightly lit bathroom, taking advantage of the steam from showers.</li>
    <li>Placing the pot on a large tray filled with pebbles and water (ensuring the pot sits on the pebbles, not in the water).</li>
</ul>

<h2>Lighting: Cool and Indirect</h2>
<p>Boston ferns thrive in medium to bright indirect light. They naturally grow on the dappled forest floor under the shade of massive trees. Direct, hot afternoon sun will literally cook the delicate fronds, scorching them beyond repair. An East or North-facing window provides perfectly gentle, cool morning light that ferns adore.</p>

<div class="affiliate-box">
    <h3>Are Your Fern Fronds Turning Yellow or Crispy Brown?</h3>
    <p>Is it a humidity problem, under-watering, or a fungal infection? Let our AI diagnose the exact symptom instantly.</p>
    <a href="/plant-disease-finder/" class="btn btn-primary">Scan My Fern Now</a>
</div>
        '
    ]
];

foreach ($articles as $article) {
    global $wpdb;
    $exists = $wpdb->get_var($wpdb->prepare("SELECT ID FROM $wpdb->posts WHERE post_name = %s", $article['slug']));
    
    if (!$exists) {
        $post_id = wp_insert_post([
            'post_title'   => $article['title'],
            'post_name'    => $article['slug'],
            'post_content' => $article['content'],
            'post_status'  => 'publish',
            'post_author'  => 1,
            'post_type'    => 'post'
        ]);
        
        $image_path = $article['image'];
        if(file_exists($image_path)) {
            $filetype = wp_check_filetype(basename($image_path), null);
            $attachment = array(
                'guid'           => wp_upload_dir()['url'] . '/' . basename($image_path),
                'post_mime_type' => $filetype['type'],
                'post_title'     => preg_replace('/\.[^.]+$/', '', basename($image_path)),
                'post_content'   => '',
                'post_status'    => 'inherit'
            );
            $attach_id = wp_insert_attachment($attachment, $image_path, $post_id);
            require_once(ABSPATH . 'wp-admin/includes/post.php');
            $attach_data = wp_generate_attachment_metadata($attach_id, $image_path);
            wp_update_attachment_metadata($attach_id, $attach_data);
            set_post_thumbnail($post_id, $attach_id);
        }
        
        wp_set_object_terms($post_id, 'Houseplant Guides', 'category', true);
        echo "Created: " . $article['title'] . "\n";
    } else {
        echo "Exists: " . $article['title'] . "\n";
    }
}
?>
