<?php
/**
 * Custom Widgets
 *
 * @package PlantsMag
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Recent Plants Widget
 */
class PlantsMag_Recent_Plants_Widget extends WP_Widget
{

    public function __construct()
    {
        parent::__construct(
            'plantsmag_recent_plants',
            __('PlantsMag: Recent Plants', 'plantsmag'),
            array('description' => __('Display recent plant guides.', 'plantsmag'))
        );
    }

    public function widget($args, $instance)
    {
        $title = !empty($instance['title']) ? $instance['title'] : __('Recent Plant Guides', 'plantsmag');
        $number = !empty($instance['number']) ? absint($instance['number']) : 5;

        echo $args['before_widget'];

        if ($title) {
            echo $args['before_title'] . esc_html($title) . $args['after_title'];
        }

        $plants = new WP_Query(
            array(
                'post_type' => 'plant_guide',
                'posts_per_page' => $number,
                'no_found_rows' => true,
            )
        );

        if ($plants->have_posts()):
            ?>
            <ul class="widget-plants-list">
                <?php
                while ($plants->have_posts()):
                    $plants->the_post();
                    ?>
                    <li class="widget-plant-item">
                        <?php if (has_post_thumbnail()): ?>
                            <a href="<?php the_permalink(); ?>" class="widget-plant-thumb">
                                <?php the_post_thumbnail('thumbnail'); ?>
                            </a>
                        <?php endif; ?>
                        <div class="widget-plant-info">
                            <a href="<?php the_permalink(); ?>" class="widget-plant-title"><?php the_title(); ?></a>
                            <?php
                            $difficulty = get_the_terms(get_the_ID(), 'difficulty_level');
                            if ($difficulty && !is_wp_error($difficulty)):
                                ?>
                                <span class="widget-plant-difficulty"><?php echo esc_html($difficulty[0]->name); ?></span>
                            <?php endif; ?>
                        </div>
                    </li>
                    <?php
                endwhile;
                wp_reset_postdata();
                ?>
            </ul>
            <?php
        endif;

        echo $args['after_widget'];
    }

    public function form($instance)
    {
        $title = !empty($instance['title']) ? $instance['title'] : __('Recent Plant Guides', 'plantsmag');
        $number = !empty($instance['number']) ? absint($instance['number']) : 5;
        ?>
        <p>
            <label
                for="<?php echo esc_attr($this->get_field_id('title')); ?>"><?php esc_html_e('Title:', 'plantsmag'); ?></label>
            <input class="widefat" id="<?php echo esc_attr($this->get_field_id('title')); ?>"
                name="<?php echo esc_attr($this->get_field_name('title')); ?>" type="text"
                value="<?php echo esc_attr($title); ?>">
        </p>
        <p>
            <label
                for="<?php echo esc_attr($this->get_field_id('number')); ?>"><?php esc_html_e('Number of posts:', 'plantsmag'); ?></label>
            <input class="tiny-text" id="<?php echo esc_attr($this->get_field_id('number')); ?>"
                name="<?php echo esc_attr($this->get_field_name('number')); ?>" type="number" min="1" max="10"
                value="<?php echo esc_attr($number); ?>">
        </p>
        <?php
    }

    public function update($new_instance, $old_instance)
    {
        $instance = array();
        $instance['title'] = sanitize_text_field($new_instance['title']);
        $instance['number'] = absint($new_instance['number']);
        return $instance;
    }
}

/**
 * Newsletter Widget
 */
class PlantsMag_Newsletter_Widget extends WP_Widget
{

    public function __construct()
    {
        parent::__construct(
            'plantsmag_newsletter',
            __('PlantsMag: Newsletter', 'plantsmag'),
            array('description' => __('Newsletter signup form.', 'plantsmag'))
        );
    }

    public function widget($args, $instance)
    {
        $title = !empty($instance['title']) ? $instance['title'] : __('Subscribe', 'plantsmag');
        $description = !empty($instance['description']) ? $instance['description'] : '';

        echo $args['before_widget'];
        ?>
        <div class="newsletter-widget">
            <?php if ($title): ?>
                <h4 class="newsletter-title"><?php echo esc_html($title); ?></h4>
            <?php endif; ?>

            <?php if ($description): ?>
                <p class="newsletter-desc"><?php echo esc_html($description); ?></p>
            <?php endif; ?>

            <form class="newsletter-form" action="#" method="post">
                <input type="email" name="email" placeholder="<?php esc_attr_e('Enter your email', 'plantsmag'); ?>" required>
                <button type="submit" class="pm-btn pm-btn-primary">
                    <?php esc_html_e('Subscribe', 'plantsmag'); ?>
                </button>
            </form>
        </div>
        <?php
        echo $args['after_widget'];
    }

    public function form($instance)
    {
        $title = !empty($instance['title']) ? $instance['title'] : __('Subscribe', 'plantsmag');
        $description = !empty($instance['description']) ? $instance['description'] : '';
        ?>
        <p>
            <label
                for="<?php echo esc_attr($this->get_field_id('title')); ?>"><?php esc_html_e('Title:', 'plantsmag'); ?></label>
            <input class="widefat" id="<?php echo esc_attr($this->get_field_id('title')); ?>"
                name="<?php echo esc_attr($this->get_field_name('title')); ?>" type="text"
                value="<?php echo esc_attr($title); ?>">
        </p>
        <p>
            <label
                for="<?php echo esc_attr($this->get_field_id('description')); ?>"><?php esc_html_e('Description:', 'plantsmag'); ?></label>
            <textarea class="widefat" id="<?php echo esc_attr($this->get_field_id('description')); ?>"
                name="<?php echo esc_attr($this->get_field_name('description')); ?>"><?php echo esc_textarea($description); ?></textarea>
        </p>
        <?php
    }

    public function update($new_instance, $old_instance)
    {
        $instance = array();
        $instance['title'] = sanitize_text_field($new_instance['title']);
        $instance['description'] = sanitize_text_field($new_instance['description']);
        return $instance;
    }
}

/**
 * Social Follow Widget
 */
class PlantsMag_Social_Widget extends WP_Widget
{

    public function __construct()
    {
        parent::__construct(
            'plantsmag_social',
            __('PlantsMag: Social Links', 'plantsmag'),
            array('description' => __('Display social media links.', 'plantsmag'))
        );
    }

    public function widget($args, $instance)
    {
        $title = !empty($instance['title']) ? $instance['title'] : __('Follow Us', 'plantsmag');

        echo $args['before_widget'];

        if ($title) {
            echo $args['before_title'] . esc_html($title) . $args['after_title'];
        }

        plantsmag_social_links();

        echo $args['after_widget'];
    }

    public function form($instance)
    {
        $title = !empty($instance['title']) ? $instance['title'] : __('Follow Us', 'plantsmag');
        ?>
        <p>
            <label
                for="<?php echo esc_attr($this->get_field_id('title')); ?>"><?php esc_html_e('Title:', 'plantsmag'); ?></label>
            <input class="widefat" id="<?php echo esc_attr($this->get_field_id('title')); ?>"
                name="<?php echo esc_attr($this->get_field_name('title')); ?>" type="text"
                value="<?php echo esc_attr($title); ?>">
        </p>
        <p class="description">
            <?php esc_html_e('Configure social links in Customizer > Theme Options > Social Media.', 'plantsmag'); ?></p>
        <?php
    }

    public function update($new_instance, $old_instance)
    {
        $instance = array();
        $instance['title'] = sanitize_text_field($new_instance['title']);
        return $instance;
    }
}

/**
 * Register Widgets
 */
function plantsmag_register_widgets()
{
    register_widget('PlantsMag_Recent_Plants_Widget');
    register_widget('PlantsMag_Newsletter_Widget');
    register_widget('PlantsMag_Social_Widget');
}
add_action('widgets_init', 'plantsmag_register_widgets');
