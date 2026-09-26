<?php
require_once( dirname(__FILE__) . '/wp-load.php' );
if ( function_exists( 'litespeed_purge_all' ) ) {
    litespeed_purge_all();
    echo "LiteSpeed Cache Purged\n";
} elseif ( class_exists( 'LiteSpeed_Cache_API' ) ) {
    LiteSpeed_Cache_API::purge_all();
    echo "LiteSpeed Cache API Purged\n";
} else {
    echo "No LiteSpeed installed.\n";
}
wp_cache_flush();
echo "Object cache flushed.\n";
?>
