document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('pm-watering-form');
    const container = document.querySelector('.pm-app-container');
    const closeBtn = document.getElementById('pm-close-sheet');
    const overlay = document.getElementById('pm-overlay');
    
    // Result elements
    const daysResult = document.getElementById('pm-days-result');
    const messageResult = document.getElementById('pm-result-message');
    const affiliateLink = document.getElementById('pm-affiliate-link');

    // Simple Database / Logic
    const baseDays = {
        'succulent': 14,
        'tropical': 7,
        'fern': 5,
        'herb': 3,
        'snake': 21
    };

    const plantNames = {
        'succulent': 'Succulent',
        'tropical': 'Tropical Plant',
        'fern': 'Fern',
        'herb': 'Indoor Herb',
        'snake': 'Snake Plant'
    };

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get values
        const plant = document.getElementById('plant-type').value;
        const pot = document.querySelector('input[name="pot-type"]:checked')?.value;
        const light = document.querySelector('input[name="light-level"]:checked')?.value;
        
        if(!plant || !pot || !light) return;

        // Calculate
        let days = baseDays[plant] || 7;
        
        // Pot Modifier
        if (pot === 'terracotta') {
            days = days * 0.8; // Dries 20% faster
        }
        
        // Light Modifier
        if (light === 'low') {
            days = days * 1.3; // Dries 30% slower
        } else if (light === 'bright') {
            days = days * 0.8; // Dries 20% faster
        }
        
        // Round to nearest integer
        days = Math.round(days);
        
        // Safety bounds
        if (days < 1) days = 1;

        // Update UI
        daysResult.textContent = days;
        messageResult.textContent = `Water your ${plantNames[plant]} every ${days} days. Check the top 2 inches of soil before watering.`;

        // Customize affiliate link based on plant (Example dynamic logic)
        if(plant === 'succulent' || plant === 'snake') {
            affiliateLink.href = 'https://amazon.com/dp/example-soil-moisture'; // Replace with real referral link
            affiliateLink.textContent = 'Get a Soil Moisture Sensor ➔';
        } else {
            affiliateLink.href = 'https://amazon.com/dp/example-self-watering'; // Replace with real referral link
            affiliateLink.textContent = 'Get a Self-Watering Pot ➔';
        }

        // Show Bottom Sheet (Native feel)
        container.classList.add('show-result');
        
        // Provide haptic feedback if available
        if (navigator.vibrate) {
            navigator.vibrate(50);
        }
    });

    const closeSheet = () => {
        container.classList.remove('show-result');
    };

    closeBtn.addEventListener('click', closeSheet);
    overlay.addEventListener('click', closeSheet);
    
    // Allow dragging down to close (Simple implementation)
    let startY;
    const sheetContent = document.querySelector('.pm-bottom-sheet');
    
    sheetContent.addEventListener('touchstart', (e) => {
        startY = e.touches[0].clientY;
    }, {passive: true});
    
    sheetContent.addEventListener('touchmove', (e) => {
        const y = e.touches[0].clientY;
        if (y - startY > 50) { // Dragged down 50px
            closeSheet();
        }
    }, {passive: true});
});
