<?php
require_once('wp-load.php');
if ( class_exists( 'LiteSpeed\Purge' ) ) {
    LiteSpeed\Purge::purge_all();
    echo "LiteSpeed cache purged successfully.";
} else {
    echo "LiteSpeed not active.";
}
?>
