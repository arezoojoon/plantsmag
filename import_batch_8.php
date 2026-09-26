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
        'title' => 'Swiss Cheese Plant (Monstera adansonii): The Trailing Cousin Care',
        'slug'  => 'monstera-adansonii-swiss-cheese-trailing-care',
        'image' => '/home/u284669846/domains/plantsmag.com/public_html/tmp_images/monstera_adansonii_cover.png',
        'content' => '
<h2>The Wild, Fenestrated Vine</h2>
<p>While the Monstera deliciosa is famous for its massive, sprawling, deep-cut leaves, its smaller cousin, the Monstera adansonii (commonly called the Swiss Cheese Vine), has a completely different structural aesthetic. Instead of growing into a giant floor plant, the adansonii is a rapid-vining climber. Its smaller, oval leaves are completely enclosed by stunning, natural holes (fenestrations) right out of the gate, making it look as though an incredibly artistic caterpillar went to work on it.</p>
<p>Because it is a vine, you have two distinct interior design choices: let it aggressively trail down from a high hanging basket, or train it upwards on a moss pole. Whichever you choose, understanding its massive humidity needs is critical to keeping it from turning yellow.</p>

<h2>Moss Poles: Unlocking Massive Leaves</h2>
<p>In its native jungle habitat, the Monstera adansonii grows by anchoring its aerial roots tightly into the bark of massive tropical trees, climbing straight up towards the canopy light. While it looks beautiful trailing downwards, gravity actually signals the plant that it has lost its tree. When trailing, the leaves will remain relatively small.</p>
<p>If you want those massive, deeply fenestrated leaves you see on Instagram, you must train the vine upward on a damp sphagnum moss pole. As the aerial roots bite into the moist moss, they absorb water and nutrients directly into the stem, signaling the plant to rapidly increase the size of its foliage.</p>

<h2>Watering the Swiss Cheese Vine</h2>
<p>Like its larger cousin, the adansonii is an Aroid and requires a very chunky, well-draining soil mix (lots of orchid bark and perlite). The roots need oxygen as much as they need moisture. Keep the soil evenly moist during the spring and summer growing season, allowing only the top inch to dry out before watering again. If the soil stays soggy, the delicate aerial roots that have burrowed into the dirt will rot instantly.</p>

<div class="affiliate-box">
    <h3>Are You Drowning Your Vine?</h3>
    <p>Aroid soil dries entirely differently than normal potting soil. Let our Smart Tool calculate your exact watering interval based on your mix ratio.</p>
    <a href="/watering-calculator/" class="btn btn-outline">Check My Watering Interval</a>
</div>

<h2>Managing Crispy Tips and Humidity</h2>
<p>The thin foliage of the Swiss Cheese Vine is extremely sensitive to dry air. If your home humidity drops below 50%, the tips of the leaves will almost certainly begin to turn brown and crispy. If you keep the plant near a heating vent, it may dry out completely. Grouping it with other tropicals or utilizing a humidifier is highly recommended.</p>

<div class="affiliate-box">
    <h3>Is Your Monstera Adansonii Turning Yellow?</h3>
    <p>Yellowing leaves on an adansonii can mean root rot, nutrient deficiency, or simply old-age shedding. Upload a photo of the leaf to our AI Plant Doctor to find out exactly what is happening.</p>
    <a href="/plant-disease-finder/" class="btn btn-primary">Diagnose Yellow Leaves Instantly</a>
</div>
        '
    ],
    [
        'title' => 'Pilea peperomioides (Chinese Money Plant): Propagation Guide',
        'slug'  => 'pilea-peperomioides-chinese-money-plant-propagation',
        'image' => '/home/u284669846/domains/plantsmag.com/public_html/tmp_images/pilea_cover.png',
        'content' => '
<h2>The UFO Plant Phenomenon</h2>
<p>Few plants have achieved the viral, cult-like status of the Pilea peperomioides. Known variously as the Chinese Money Plant, the UFO Plant, or the Pancake Plant, its perfect, perfectly round, lily-pad-like green leaves extending from a central fleshy stem give it an incredibly cheerful, cartoonish aesthetic. Originating from the Yunnan Province in Southern China, it was originally spread globally not through commercial nurseries, but by botanical enthusiasts handing out its prolific "pups" (baby plants) to friends.</p>

<h2>Watering: Balancing the Fleshy Stems</h2>
<p>The Pilea peperomioides acts very much like a succulent. It stores massive amounts of water in its central stalk and its thick, peltate leaves. Because of this, it demands a "soak and dry" watering rhythm. Allow the top two to three inches of the soil to dry out completely before you drench it.</p>
<p>The Pilea is incredibly communicative. The perfectly flat, round leaves will begin to subtly droop downwards and curl slightly when the plant is thirsty. A thorough watering will see them pump back up and stand at cheerful attention within hours.</p>

<div class="affiliate-box">
    <h3>Are Your Pilea Leaves Curling or Rotting?</h3>
    <p>If the leaves are curling inward violently, your watering cadence is off. Use our Smart Calculator to establish the precise rhythm for your specific pot size.</p>
    <a href="/watering-calculator/" class="btn btn-outline">Generate Pilea Watering Schedule</a>
</div>

<h2>Lighting: Rotating for Symmetry</h2>
<p>To keep the Pilea growing straight and bushy, you must provide bright, indirect light. If placed in a dark corner, the central stem will stretch out aggressively toward the light, leaving massive, ugly gaps between the leaves. Because the leaves are incredibly phototropic (they turn to face the sun like solar panels), a Pilea left in one position will quickly become lopsided. You must rotate the pot 45 degrees every time you water it to ensure perfectly spherical, symmetrical growth.</p>

<h2>The Endless Propagation Machine</h2>
<p>The most rewarding aspect of owning a Pilea is its explosive reproduction rate. A healthy, mature Pilea will constantly push up tiny baby plants (pups) straight out of the dirt surrounding the mother plant, or directly off the main stem. Once a pup in the dirt is about two inches tall and has its own distinct stem, you can take a sharp, clean knife, dig down roughly an inch into the dirt, and slice the umbilical root connecting it to the mother. Place the pup directly into a tiny pot with moist soil, and you instantly have a brand new plant to give away.</p>

<div class="affiliate-box">
    <h3>Tiny White Dots on the Underside of Leaves?</h3>
    <p>Pilea leaves naturally excrete tiny white mineral deposits through their pores, which are often mistaken for pests. Don’t panic—take a picture and let our AI confirm if it’s harmless minerals or dangerous spider mites.</p>
    <a href="/plant-disease-finder/" class="btn btn-primary">Scan My Pilea Leaves Now</a>
</div>
        '
    ],
    [
        'title' => 'Caladium: Navigating the Colorful Winter Dormancy',
        'slug'  => 'caladium-colorful-winter-dormancy-survival-guide',
        'image' => '/home/u284669846/domains/plantsmag.com/public_html/tmp_images/caladium_cover.png',
        'content' => '
<h2>The Paper-Thin Neon Wonders</h2>
<p>If you have ever been mesmerized by a plant that looks as though it is glowing from the inside out with translucent, neon-pink, deep red, or blinding white leaves with stark green veins, you have encountered a Caladium. Native to the banks of the Amazon river, Caladiums are grown exclusively for their spectacular, paper-thin, arrow-shaped foliage rather than their flowers.</p>
<p>However, Caladiums are a source of enormous heartbreak for indoor gardeners. They grow from underground tubers (like potatoes), and their life cycle is strictly seasonal. If you do not understand how to manage their winter dormancy, you will assume the plant has died and successfully throw it in the trash.</p>

<h2>The Terrifying Winter Die-Back</h2>
<p>When autumn arrives and the days grow shorter, a Caladium will suddenly begin to look terrible. The vibrant leaves will drop, yellow, shrivel, and die, one by one. No amount of water, fertilizer, or panic will stop it. <strong>This is perfectly natural.</strong></p>
<p>The plant has entered its obligatory winter dormancy. It is pulling all of its energy out of the leaves and storing it back into the underground tuber to survive the winter. When this happens, you must cease all watering immediately. Allow the soil to dry out completely, trim off the dead leaves, and place the pot in a dark, cool closet (between 60°F and 65°F) for the winter.</p>
<p>When spring arrives (around March or April), pull the pot out into a bright, warm room, begin watering it lightly, and within weeks, it will explosively push up a brand new, magnificent canopy of neon leaves.</p>

<h2>Lighting During Active Growth</h2>
<p>During the spring and summer, Caladiums demand bright, filtered, indirect light to produce those blindingly bright colors. The leaves are incredibly thin—almost like tissue paper. Direct sunlight will obliterate the delicate foliage, burning brown holes straight through the pink and white centers.</p>

<h2>Watering the Delicate Tubers</h2>
<p>When actively growing, Caladiums are highly thirsty plants. The soil must be kept constantly, evenly moist. If the soil dries out entirely, the paper-thin leaves will crisp up and collapse instantly. However, because they grow from tubers, if they sit in a puddle of stagnant water with poor drainage, the tuber will quickly rot away into a foul-smelling mush.</p>

<div class="affiliate-box">
    <h3>Mastering the Tuber Moisture Balance</h3>
    <p>Caladiums require an incredibly precise moisture balance to prevent the tuber from rotting while keeping the thin leaves hydrated. Use our Smart Tool to get exactly the right schedule.</p>
    <a href="/watering-calculator/" class="btn btn-outline">Get Custom Caladium Watering Schedule</a>
</div>

<div class="affiliate-box">
    <h3>Are The Leaves Tearing or Getting Crispy Margins?</h3>
    <p>Because they are paper-thin, humidity levels drastically affect Caladiums. Upload an image of the damage to our AI to see if a dedicated humidifier is required or if it is a fungal issue.</p>
    <a href="/plant-disease-finder/" class="btn btn-primary">Diagnose My Caladium Instantly</a>
</div>
        '
    ],
    [
        'title' => 'Parlor Palm (Chamaedorea elegans): The Victorian Miniature Palm',
        'slug'  => 'parlor-palm-chamaedorea-elegans-victorian-care',
        'image' => '/home/u284669846/domains/plantsmag.com/public_html/tmp_images/parlor_palm_cover.png',
        'content' => '
<h2>The Quintessential Indoor Tree</h2>
<p>Since the Victorian era, the Parlor Palm (Chamaedorea elegans) has been the gold standard for bringing elegant, sophisticated greenery indoors. While towering Majesty Palms and Areca Palms often struggle and die in the dry, low-light environment of a typical living room, the compact, deeply green, feathery fronds of the Parlor Palm genuinely thrive indoors. Native to the dense, shaded understory of rainforests in Southern Mexico and Guatemala, it is a slow-growing, highly adaptable miniature palm that rarely exceeds three or four feet in height, making it perfect for apartments and tight corners.</p>

<h2>The Low Light Champion</h2>
<p>The primary reason the Parlor Palm became a Victorian staple is its extreme tolerance for low light. In fact, placing a Parlor Palm in direct sunlight is a fatal mistake; the delicate, thin leaflets will rapidly scorch, turn yellow, and dry to a crisp. While it survives in dark corners (like windowless offices), its ideal placement is in an East or North-facing room where it receives bright, gentle, filtered ambient light. In these conditions, it will occasionally produce little branching stems of tiny yellow flowers.</p>

<h2>Watering: Avoiding Frond Crispiness</h2>
<p>Watering the Parlor Palm requires attention to its fine, delicate root system. It prefers its soil to be kept lightly and evenly moist, but not soaking wet. A good rule of thumb is to water when the top inch of the soil feels dry to the touch. If you chronically underwater the palm, the tips of the feathery fronds will turn permanently brown and crispy. If you overwater it and the pot lacks drainage, the entire plant will begin to turn a sickly, pale yellow from the base upwards as the roots suffocate.</p>

<div class="affiliate-box">
    <h3>Stop Your Palm Fronds From Turning Brown!</h3>
    <p>Timing your watering is critical for the Parlor Palm to maintain its emerald green flush. Let our Smart Calculator map out a precise watering calendar for your setup.</p>
    <a href="/watering-calculator/" class="btn btn-outline">Generate Precise Palm Watering Schedule</a>
</div>

<h2>Humidity and The Spider Mite Threat</h2>
<p>While the Parlor Palm is far more tolerant of dry indoor air (low humidity) than most tropical ferns or Calatheas, this resilience comes with a major caveat: Spider Mites love dry Parlor Palms. The massive surface area of the hundreds of tiny leaflets creates the perfect hiding ground for these microscopic pests.</p>
<p>To keep the fronds green and the spider mites at bay, physically wash the palm in your shower once a month. The jets of water clear dust from the pores and blast away any incipient mite colonies. You can also mist the plant a few times a week or run a nearby humidifier to naturally deter dry-loving pests.</p>

<div class="affiliate-box">
    <h3>Is Your Palm Looking Dusty or Webbed?</h3>
    <p>If the leaves look strangely mottled or if you see fine webbing at the base of the stems, you likely have an infestation. Upload a photo right now to our AI Plant Doctor for immediate pest identification.</p>
    <a href="/plant-disease-finder/" class="btn btn-primary">Scan My Palm Now</a>
</div>
        '
    ],
    [
        'title' => 'Air Plants (Tillandsia): Growing Soil-Free Houseplants',
        'slug'  => 'air-plants-tillandsia-growing-soil-free-guide',
        'image' => '/home/u284669846/domains/plantsmag.com/public_html/tmp_images/air_plants_cover.png',
        'content' => '
<h2>The Gravity-Defying Botanical Wonders</h2>
<p>Imagine a houseplant that requires absolutely no dirt, no pot, and can be glued to a piece of driftwood, suspended from the ceiling by a fishing wire, or nestled inside a decorative seashell. Welcome to the bizarre and captivating world of Air Plants (Tillandsia). Belonging to the bromeliad family, Tillandsias are epiphytes that use their tiny, wire-like roots exclusively for anchoring themselves to tree branches or rocks in the dense jungles and deserts of South America. They do not absorb a single drop of water or nutrient through these roots.</p>
<p>So how do they survive without soil? They absorb everything they need—water, nutrients, and oxygen—directly through specialized, microscopic, scale-like structures on their leaves called trichomes. These trichomes give many air plants their beautiful, fuzzy, silvery appearance.</p>

<h2>The Great Misting Myth</h2>
<p>The single greatest misconception about Air Plants is that you can keep them alive simply by lightly misting them with a spray bottle once a week. <strong>This is entirely false and will lead to a slow, dry death.</strong> In the wild, they are drenched by heavy tropical rainstorms or soaked in dense morning coastal fogs.</p>
<p>To properly water an air plant, you must physically submerge the entire plant in a bowl of lukewarm water. Leave it soaking completely under the water for 20 to 30 minutes. Do this once every one to two weeks, depending on how dry your house is. If the leaves look deeply wrinkled or start to curl back on themselves aggressively, the plant is severely dehydrated and may need an overnight soak to recover.</p>

<div class="affiliate-box">
    <h3>Are Your Air Plants Drying Out?</h3>
    <p>Knowing exactly how often to do a deep submersion soak depends entirely on your home’s ambient humidity. Let our Smart Tool calculate the perfect soaking interval.</p>
    <a href="/watering-calculator/" class="btn btn-outline">Check My Air Plant Soaking Schedule</a>
</div>

<h2>The Lethal Drying Protocol</h2>
<p>Watering the air plant is only half the battle; drying it correctly is a matter of life and death. Because of their rosette shape, water naturally pools in the center (the crown) of the plant. If an air plant is put back on its display shelf while still wet in the center, it will rot and fall apart within 48 hours.</p>
<p>After their bath, take the plant out, gently shake it upside down to dislodge trapped water, and place it upside down on a clean dish towel in a well-ventilated area for at least four hours until it is 100% bone dry before returning it to its display.</p>

<h2>Lighting: Silver vs. Green</h2>
<p>Not all air plants are created equal. As a general rule, Tillandsias with fuzzy, silvery leaves (which have more trichomes) come from harsher, drier, sunnier environments. These plants require extremely bright, direct sunlight. Conversely, Tillandsias with smoother, greener leaves originated in deeper, shaded jungles and prefer bright, filtered, indirect light to prevent scorching.</p>

<div class="affiliate-box">
    <h3>Is the Base Turning Brown and Mushy?</h3>
    <p>A dark, soft, or mushy base is the fatal sign of crown rot from improper drying. Upload a photo of the base to our AI to see if the plant can be salvaged.</p>
    <a href="/plant-disease-finder/" class="btn btn-primary">Diagnose Air Plant Rot Instantly</a>
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
