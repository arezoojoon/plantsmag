jQuery(document).ready(function($) {
    const uploadArea = $('#pm-upload-area');
    const fileInput = $('#pm-disease-image');
    const previewImg = $('#pm-preview-img');
    const uploadContent = $('#pm-upload-content');
    const analyzeBtn = $('#pm-analyze-btn');
    const container = $('.pm-disease-app');
    const closeBtn = $('#pm-close-disease');
    const resultSheet = $('#pm-disease-result');
    const overlay = $('#pm-overlay-disease');
    const loadingOverlay = $('#pm-ai-loading');
    
    let currentImageBase64 = null;

    uploadArea.on('click', function(e) {
        if(e.target.id !== 'pm-disease-image') {
            fileInput.trigger('click');
        }
    });

    fileInput.on('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;

        if (!file.type.match('image.*')) {
            alert('Please select an image file (JPEG or PNG).');
            return;
        }

        const reader = new FileReader();
        reader.onload = function(event) {
            const img = new Image();
            img.onload = function() {
                const canvas = document.createElement('canvas');
                const MAX_WIDTH = 600;
                const MAX_HEIGHT = 600;
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
                
                currentImageBase64 = canvas.toDataURL('image/jpeg', 0.8);
                
                previewImg.attr('src', currentImageBase64).show();
                uploadContent.hide();
                uploadArea.addClass('has-image');
                analyzeBtn.prop('disabled', false);
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    });

    analyzeBtn.on('click', function() {
        if (!currentImageBase64) return;

        loadingOverlay.addClass('active');
        
        fetch(pmDiseaseObj.apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-WP-Nonce': pmDiseaseObj.nonce
            },
            body: JSON.stringify({
                image_base64: currentImageBase64
            })
        })
        .then(res => {
            if (!res.ok) {
                return res.json().then(err => { throw err; });
            }
            return res.json();
        })
        .then(data => {
            loadingOverlay.removeClass('active');
            showResult(data);
        })
        .catch(err => {
            loadingOverlay.removeClass('active');
            alert('Error: ' + (err.message || 'Server connection failed. Please check your internet connection.'));
        });
    });

    function showResult(data) {
        $('#pm-diag-title').text(data.diagnosis || 'Unknown Condition');
        $('#pm-diag-text').text(data.explanation || 'We could not figure out what is wrong.');
        
        const keyword = data.treatment_keyword || 'plant care';
        $('#pm-treatment-text').text(data.treatment_desc || 'General maintenance required.');
        
        // Map common keywords to specific high-converting Amazon ASINs, else fallback to search
        let affLink = 'https://www.amazon.com/s?k=' + encodeURIComponent(keyword + ' for plants') + '&tag=plantsmag-20';
        
        const keywordLower = keyword.toLowerCase();
        if (keywordLower.includes('neem')) {
            affLink = 'https://www.amazon.com/dp/B004QAWGIO?tag=plantsmag-20'; // Example Neem Oil
        } else if (keywordLower.includes('copper') || keywordLower.includes('fungicide')) {
            affLink = 'https://www.amazon.com/dp/B000RUJZS6?tag=plantsmag-20'; // Example Copper Fungicide
        } else if (keywordLower.includes('sticky') || keywordLower.includes('trap')) {
            affLink = 'https://www.amazon.com/dp/B07XLM4NWV?tag=plantsmag-20'; // Example Yellow Sticky Traps
        } else if (keywordLower.includes('fertilizer') || keywordLower.includes('food')) {
            affLink = 'https://www.amazon.com/dp/B000OV8WTM?tag=plantsmag-20'; // Example Liquid Plant Food
        }
        
        $('#pm-treatment-link')
            .attr('href', affLink)
            .text('Buy ' + keyword + ' ➔');

        resultSheet.addClass('active');
        overlay.addClass('active');
        if (navigator.vibrate) navigator.vibrate(50);
    }

    const closeSheet = () => {
        resultSheet.removeClass('active');
        overlay.removeClass('active');
    };

    closeBtn.on('click', function() {
        closeSheet();
        previewImg.hide().attr('src', '');
        uploadContent.show();
        uploadArea.removeClass('has-image');
        analyzeBtn.prop('disabled', true);
        currentImageBase64 = null;
        fileInput.val('');
    });
    
    overlay.on('click', closeSheet);
    
    // Bottom sheet drag close logic
    let startY;
    const sheetDOM = document.getElementById('pm-disease-result');
    if(sheetDOM) {
        sheetDOM.addEventListener('touchstart', (e) => {
            startY = e.touches[0].clientY;
        }, {passive: true});
        
        sheetDOM.addEventListener('touchmove', (e) => {
            const y = e.touches[0].clientY;
            if (y - startY > 60) closeSheet();
        }, {passive: true});
    }
});
