<?php
/**
 * The template for displaying comments
 *
 * @package PlantsMag_Premium
 */

if ( post_password_required() ) {
	return;
}
?>

<div id="comments" class="comments-area">

	<?php if ( have_comments() ) : ?>
		<h2 class="comments-title">
			<?php
			$plantsmag_comment_count = get_comments_number();
			if ( '1' === $plantsmag_comment_count ) {
				printf(
					/* translators: 1: title. */
					esc_html__( '1 Reply to &ldquo;%1$s&rdquo;', 'plantsmag-premium' ),
					'<span>' . wp_kses_post( get_the_title() ) . '</span>'
				);
			} else {
				printf( 
					/* translators: 1: comment count number, 2: title. */
					esc_html( _nx( '%1$s Reply to &ldquo;%2$s&rdquo;', '%1$s Replies to &ldquo;%2$s&rdquo;', $plantsmag_comment_count, 'comments title', 'plantsmag-premium' ) ),
					number_format_i18n( $plantsmag_comment_count ),
					'<span>' . wp_kses_post( get_the_title() ) . '</span>'
				);
			}
			?>
		</h2><!-- .comments-title -->

		<ol class="comment-list">
			<?php
			wp_list_comments(
				array(
					'style'      => 'ol',
					'short_ping' => true,
					'avatar_size'=> 50,
				)
			);
			?>
		</ol><!-- .comment-list -->

		<?php
		the_comments_navigation();

		if ( ! comments_open() ) :
			?>
			<p class="no-comments"><?php esc_html_e( 'Comments are closed.', 'plantsmag-premium' ); ?></p>
			<?php
		endif;

	endif; // Check for have_comments().

	comment_form( array(
		'title_reply_before' => '<h2 id="reply-title" class="comment-reply-title">',
		'title_reply_after'  => '</h2>',
		'class_form'         => 'comment-form',
		'class_submit'       => 'btn btn-primary submit',
		'comment_field'      => '<p class="comment-form-comment"><label for="comment">' . _x( 'Comment', 'noun', 'plantsmag-premium' ) . '</label><textarea id="comment" name="comment" class="pm-textarea" cols="45" rows="8" required="required"></textarea></p>',
		'fields'             => array(
			'author' => '<p class="comment-form-author"><label for="author">' . __( 'Name', 'plantsmag-premium' ) . ( $req ? ' <span class="required">*</span>' : '' ) . '</label><input id="author" name="author" type="text" class="pm-input" value="' . esc_attr( $commenter['comment_author'] ) . '" size="30" ' . ( $req ? 'required="required"' : '' ) . ' /></p>',
			'email'  => '<p class="comment-form-email"><label for="email">' . __( 'Email', 'plantsmag-premium' ) . ( $req ? ' <span class="required">*</span>' : '' ) . '</label><input id="email" name="email" type="email" class="pm-input" value="' . esc_attr(  $commenter['comment_author_email'] ) . '" size="30" ' . ( $req ? 'required="required"' : '' ) . ' /></p>',
			'url'    => '<p class="comment-form-url"><label for="url">' . __( 'Website', 'plantsmag-premium' ) . '</label><input id="url" name="url" type="url" class="pm-input" value="' . esc_attr( $commenter['comment_author_url'] ) . '" size="30" /></p>',
		)
	) );
	?>

</div><!-- #comments -->
