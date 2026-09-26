jQuery(document).ready(function($) {
    const uploadArea = $('#pm-upload-area');
    const fileInput = $('#pm-disease-image');
    const previewImg = $('#pm-preview-img');
    const uploadContent = $('.pm-upload-content');
    const analyzeBtn = $('#pm-analyze-btn');
    const container = $('.pm-disease-app');
    const closeBtn = $('#pm-close-disease');
    
    let currentImageBase64 = null;

    // Trigger file input
    uploadArea.on('click', function() {
        // Prevent double trigger if clicking on the image directly
        fileInput.trigger('click');
    });

    // Handle file selection
    fileInput.on('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;

        // Ensure it's an image
        if (!file.type.match('image.*')) {
            alert('Please select an image file.');
            return;
        }

        // Needs to be reasonably sized for Gemini API. 
        // Let's do a simple client-side resize to max 800px.
        const reader = new FileReader();
        reader.onload = function(event) {
            const img = new Image();
            img.onload = function() {
                const canvas = document.createElement('canvas');
                const MAX_WIDTH = 800;
                const MAX_HEIGHT = 800;
                let width = img.width;
                let height = img.height;

                if (width > height) {
                    if (width > MAX_WIDTH) {
                        height *= MAX_WIDTH / width;
                        width = MAX_WIDTH;
                    }
                } else {
                    if (height > MAX_HEIGHT) {
                        width *= MAX_HEIGHT / height;
                        height = MAX_HEIGHT;
                    }
                }
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);
                
                // Get base64
                currentImageBase64 = canvas.toDataURL('image/jpeg', 0.8);
                
                // Update UI
                previewImg.attr('src', currentImageBase64).show();
                uploadContent.hide();
                uploadArea.addClass('has-image');
                analyzeBtn.prop('disabled', false);
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    });

    // Analyze Button logic
    analyzeBtn.on('click', function() {
        if (!currentImageBase64) return;

        container.addClass('is-loading');
        
        $.ajax({
            url: pmDiseaseObj.ajaxUrl,
            type: 'POST',
            data: {
                action: 'pm_analyze_disease',
                nonce: pmDiseaseObj.nonce,
                image_base64: currentImageBase64
            },
            success: function(response) {
                container.removeClass('is-loading');
                
                if (response.success && response.data) {
                    showResult(response.data);
                } else {
                    alert('Error: ' + (response.data.message || 'Could not analyze image.'));
                }
            },
            error: function() {
                container.removeClass('is-loading');
                alert('Server connection failed. Please try again.');
            }
        });
    });

    function showResult(data) {
        $('#pm-diag-title').text(data.diagnosis || 'Unknown Condition');
        $('#pm-diag-text').text(data.explanation || 'We could not figure out what is wrong.');
        
        const keyword = data.treatment_keyword || 'plant care';
        $('#pm-treatment-text').text(data.treatment_desc || 'General maintenance required.');
        
        // Generate dynamic affiliate link (Example logic for Amazon search)
        const affLink = 'https://www.amazon.com/s?k=' + encodeURIComponent(keyword) + '&tag=YOUR_AFFILIATE_TAG';
        
        $('#pm-treatment-link')
            .attr('href', affLink)
            .text('Buy ' + keyword + ' ➔');

        container.addClass('show-result');
        if (navigator.vibrate) navigator.vibrate(50);
    }

    const closeSheet = () => {
        container.removeClass('show-result');
    };

    closeBtn.on('click', function() {
        closeSheet();
        // Reset state for another plant
        previewImg.hide().attr('src', '');
        uploadContent.show();
        uploadArea.removeClass('has-image');
        analyzeBtn.prop('disabled', true);
        currentImageBase64 = null;
        fileInput.val('');
    });
    
    $('#pm-overlay-disease').on('click', closeSheet);
    
    // Bottom sheet drag close logic
    let startY;
    const sheetContent = document.getElementById('pm-disease-result');
    if(sheetContent) {
        sheetContent.addEventListener('touchstart', (e) => {
            startY = e.touches[0].clientY;
        }, {passive: true});
        
        sheetContent.addEventListener('touchmove', (e) => {
            const y = e.touches[0].clientY;
            if (y - startY > 50) closeSheet();
        }, {passive: true});
    }
});
