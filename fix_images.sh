#!/bin/bash
cd /home/u284669846/domains/plantsmag.com/public_html

echo "Finding posts without images..."
rm -f /tmp/missing_thumbs.txt

wp post list --post_type=post --fields=ID,post_title --format=csv > /tmp/all_posts.csv
tail -n +2 /tmp/all_posts.csv | while IFS=, read -r ID TITLE; do
    # Remove quotes
    ID=$(echo "$ID" | tr -d '"')
    TITLE=$(echo "$TITLE" | tr -d '"')
    
    # Check if has thumbnail
    THUMB=$(wp post meta get "$ID" _thumbnail_id 2>/dev/null)
    if [ -z "$THUMB" ]; then
        echo "Processing Post ID: $ID - Title: $TITLE"
        
        # URL encode title using python3
        ENCODED_TITLE=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))" "$TITLE")
        PROMPT="${ENCODED_TITLE}%20professional%20nature%20plant%20green%20minimal%20--no%20text%20watermark%20logo"
        
        IMAGE_URL="https://image.pollinations.ai/prompt/${PROMPT}?width=1200&height=630&model=flux&seed=$RANDOM&nologo=true"
        
        MAX_RETRIES=2
        RETRY_COUNT=0
        SUCCESS=0
        
        while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
            echo "Downloading from $IMAGE_URL"
            curl -m 30 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36" -L -s "$IMAGE_URL" -o "/tmp/img_${ID}.jpg"
            
            # Check if file is a valid image and greater than 10KB
            FILE_SIZE=$(stat -c%s "/tmp/img_${ID}.jpg" 2>/dev/null || stat -f%z "/tmp/img_${ID}.jpg" 2>/dev/null || echo 0)
            if [ "$FILE_SIZE" -gt 10000 ] && file "/tmp/img_${ID}.jpg" | grep -qiE "image data|JPEG|PNG|WebP"; then
                echo "Importing to media library..."
                wp media import "/tmp/img_${ID}.jpg" --post_id="$ID" --featured_image --title="$TITLE"
                SUCCESS=1
                break
            else
                echo "Invalid or small image downloaded ($FILE_SIZE bytes). Retrying..."
                sleep 5
                RETRY_COUNT=$((RETRY_COUNT+1))
            fi
        done
        
        if [ $SUCCESS -eq 0 ]; then
            echo "Failed to generate image for Post ID: $ID. Skipping."
        fi
        
        rm -f "/tmp/img_${ID}.jpg"
        echo "Sleeping 5s to avoid rate limit..."
        sleep 5
    fi
done

wp cache flush
wp litespeed-purge all
echo "Done!"
