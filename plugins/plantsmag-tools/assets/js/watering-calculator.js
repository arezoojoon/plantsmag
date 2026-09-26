document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('pm-watering-form');
    const container = document.querySelector('.pm-app-container');
    const closeBtn = document.getElementById('pm-close-sheet');
    const overlay = document.getElementById('pm-overlay');
    const resultSheet = document.getElementById('pm-result-sheet');
    
    // Result elements
    const daysResult = document.getElementById('pm-days-result');
    const messageResult = document.getElementById('pm-result-message');
    const affiliateLink = document.getElementById('pm-affiliate-link');
    const affiliateDesc = document.getElementById('pm-affiliate-desc');

    // Plant Database
    const baseDays = {
        'succulent': 14,
        'tropical': 8,
        'fern': 5,
        'herb': 4,
        'snake': 21,
        'pothos': 9,
        'ficus': 10
    };

    const plantNames = {
        'succulent': 'Succulent / Cactus',
        'tropical': 'Monstera / Philodendron',
        'fern': 'Fern / Calathea',
        'herb': 'Indoor Herb',
        'snake': 'Snake Plant',
        'pothos': 'Pothos / Ivy',
        'ficus': 'Ficus / Rubber Tree'
    };

    if(!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get values
        const plant = document.getElementById('plant-type').value;
        const pot = document.querySelector('input[name="pot-type"]:checked')?.value;
        const light = document.querySelector('input[name="light-level"]:checked')?.value;
        
        if(!plant || !pot || !light) return;

        // Calculate Days
        let days = baseDays[plant] || 7;
        
        // Modifiers
        if (pot === 'terracotta') days *= 0.8;
        if (light === 'low') days *= 1.3;
        else if (light === 'bright') days *= 0.8;
        
        days = Math.max(1, Math.round(days)); // Min 1 day

        // Update UI
        daysResult.textContent = days;
        messageResult.textContent = `Water your ${plantNames[plant]} every ${days} days. Check the top 2 inches of soil before watering.`;

        // Dynamic Real Affiliate Links
        if (['succulent', 'snake'].includes(plant)) {
            // Needs dry soil, moisture meter is best
            affiliateLink.href = 'https://www.amazon.com/dp/B07R4Z4G95?tag=plantsmag-20'; // Example XLUX Soil Moisture Meter
            affiliateLink.textContent = 'Get a Soil Moisture Sensor ➔';
            affiliateDesc.textContent = 'Prevent root rot by checking deep moisture levels before watering.';
        } else if (['fern', 'herb', 'tropical'].includes(plant)) {
            // Loves moisture, self-watering is best
            affiliateLink.href = 'https://www.amazon.com/dp/B085VPT5T6?tag=plantsmag-20'; // Example Self Watering Pot
            affiliateLink.textContent = 'Get a Self-Watering Pot ➔';
            affiliateDesc.textContent = 'Keep the soil perfectly moist without daily watering.';
        } else {
            // General
            affiliateLink.href = 'https://www.amazon.com/dp/B07R4Z4G95?tag=plantsmag-20';
            affiliateLink.textContent = 'Get a Smart Moisture Meter ➔';
            affiliateDesc.textContent = 'Take the guesswork out of your watering schedule.';
        }

        // Show Bottom Sheet
        if (resultSheet) resultSheet.classList.add('active');
        if (overlay) overlay.classList.add('active');
        
        if (navigator.vibrate) navigator.vibrate(50);
    });

    const closeSheet = () => {
        if (resultSheet) resultSheet.classList.remove('active');
        if (overlay) overlay.classList.remove('active');
    };

    if (closeBtn) closeBtn.addEventListener('click', closeSheet);
    if (overlay) overlay.addEventListener('click', closeSheet);
    
    // Drag down to close logic
    let startY;
    if (resultSheet) {
        resultSheet.addEventListener('touchstart', (e) => {
            startY = e.touches[0].clientY;
        }, {passive: true});
        
        resultSheet.addEventListener('touchmove', (e) => {
            const y = e.touches[0].clientY;
            if (y - startY > 60) {
                closeSheet();
            }
        }, {passive: true});
    }
});
