#!/bin/bash
cd /home/u284669846/domains/plantsmag.com/public_html

echo "Deleting bad generated images..."
wp post delete 747 749 --force

echo "Importing new high-quality Google AI images..."
REMEDIES_ID=$(wp media import /tmp/plant_remedies.png --post_id=745 --title="Common plant diseases and natural remedies" --featured_image --porcelain)
echo "Plant Remedies Image ID: $REMEDIES_ID"

wp media import /tmp/bedroom_plants.png --post_id=746 --title="Top 10 air purifying plants for bedroom" --featured_image

echo "Applying Plant Remedies Image to duplicate posts..."
wp post meta update 744 _thumbnail_id $REMEDIES_ID
wp post meta update 743 _thumbnail_id $REMEDIES_ID
wp post meta update 742 _thumbnail_id $REMEDIES_ID
wp post meta update 741 _thumbnail_id $REMEDIES_ID

wp cache flush
wp litespeed-purge all

echo "Done! High-quality images deployed."
