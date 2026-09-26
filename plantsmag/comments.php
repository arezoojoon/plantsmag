<?php
/**
 * Comments Template
 *
 * @package PlantsMag
 */

if (post_password_required()) {
    return;
}
?>

<div id="comments" class="pm-comments">

    <?php if (have_comments()): ?>
        <h2 class="pm-comments-title">
            <?php
            $comment_count = get_comments_number();
            printf(
                /* translators: 1: comment count number */
                esc_html(_nx(
                    '%1$s Comment',
                    '%1$s Comments',
                    $comment_count,
                    'comments title',
                    'plantsmag'
                )),
                number_format_i18n($comment_count)
            );
            ?>
        </h2>

        <ol class="pm-comment-list">
            <?php
            wp_list_comments(
                array(
                    'style' => 'ol',
                    'short_ping' => true,
                    'avatar_size' => 60,
                    'callback' => 'plantsmag_comment_callback',
                )
            );
            ?>
        </ol>

        <?php
        the_comments_navigation(
            array(
                'prev_text' => '<span class="nav-prev">' . esc_html__('← Older Comments', 'plantsmag') . '</span>',
                'next_text' => '<span class="nav-next">' . esc_html__('Newer Comments →', 'plantsmag') . '</span>',
            )
        );
        ?>

        <?php if (!comments_open()): ?>
            <p class="pm-no-comments"><?php esc_html_e('Comments are closed.', 'plantsmag'); ?></p>
        <?php endif; ?>

    <?php endif; ?>

    <?php
    comment_form(
        array(
            'title_reply' => esc_html__('Leave a Comment', 'plantsmag'),
            'title_reply_before' => '<h3 id="reply-title" class="pm-comment-reply-title">',
            'title_reply_after' => '</h3>',
            'comment_notes_before' => '<p class="pm-comment-notes">' . esc_html__('Your email address will not be published. Required fields are marked *', 'plantsmag') . '</p>',
            'class_form' => 'pm-comment-form',
            'class_submit' => 'pm-btn pm-btn-primary',
            'submit_button' => '<button type="submit" name="%1$s" id="%2$s" class="%3$s">%4$s</button>',
            'submit_field' => '<div class="pm-comment-form-submit">%1$s %2$s</div>',
        )
    );
    ?>

</div>

<?php
/**
 * Custom Comment Callback
 */
function plantsmag_comment_callback($comment, $args, $depth)
{
    ?>
    <li id="comment-<?php comment_ID(); ?>" <?php comment_class('pm-comment'); ?>>
        <article class="pm-comment-body">
            <div class="pm-comment-avatar">
                <?php echo get_avatar($comment, 60); ?>
            </div>
            <div class="pm-comment-content">
                <header class="pm-comment-meta">
                    <div class="pm-comment-author">
                        <?php comment_author_link(); ?>
                    </div>
                    <div class="pm-comment-metadata">
                        <time datetime="<?php comment_time('c'); ?>">
                            <?php
                            printf(
                                /* translators: 1: date, 2: time */
                                esc_html__('%1$s at %2$s', 'plantsmag'),
                                get_comment_date(),
                                get_comment_time()
                            );
                            ?>
                        </time>
                    </div>
                </header>

                <?php if ('0' == $comment->comment_approved): ?>
                    <p class="pm-comment-awaiting"><?php esc_html_e('Your comment is awaiting moderation.', 'plantsmag'); ?>
                    </p>
                <?php endif; ?>

                <div class="pm-comment-text">
                    <?php comment_text(); ?>
                </div>

                <div class="pm-comment-actions">
                    <?php
                    comment_reply_link(
                        array_merge(
                            $args,
                            array(
                                'add_below' => 'comment',
                                'depth' => $depth,
                                'max_depth' => $args['max_depth'],
                                'before' => '<span class="reply-link">',
                                'after' => '</span>',
                            )
                        )
                    );
                    ?>
                    <?php edit_comment_link(esc_html__('Edit', 'plantsmag'), '<span class="edit-link">', '</span>'); ?>
                </div>
            </div>
        </article>
        <?php
}
