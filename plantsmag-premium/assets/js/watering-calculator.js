/**
 * PlantsMag — Smart Watering Calculator v2.0
 * Evapotranspiration Formula: W = (Kc × ET0) × Sfactor
 * Lead Gate + Affiliate Products + Viral Share
 */
document.addEventListener('DOMContentLoaded', function() {
    const form        = document.getElementById('pm-watering-form');
    const container   = document.querySelector('.pm-app-container');
    const closeBtn    = document.getElementById('pm-close-sheet');
    const overlay     = document.getElementById('pm-overlay');
    const daysResult  = document.getElementById('pm-days-result');
    const msgResult   = document.getElementById('pm-result-message');
    const affLink     = document.getElementById('pm-affiliate-link');

    // ── ET Formula Database ──────────────────────────────────
    // Kc = Crop coefficient (water demand relative to reference)
    const Kc = {
        succulent: 0.20,
        tropical:  0.80,
        fern:      1.00,
        herb:      0.90,
        snake:     0.15,
        orchid:    0.60,
        pothos:    0.70,
        monstera:  0.80,
        cactus:    0.10,
        peace:     0.85,
    };

    const plantNames = {
        succulent: 'Succulent',
        tropical:  'Tropical Plant',
        fern:      'Fern',
        herb:      'Indoor Herb',
        snake:     'Snake Plant',
        orchid:    'Orchid',
        pothos:    'Pothos',
        monstera:  'Monstera',
        cactus:    'Cactus',
        peace:     'Peace Lily',
    };

    // ET0 base (days between watering at reference temp 20°C)
    const ET0_base = 7; // reference evapotranspiration = 7 days

    // Temperature modifier → multiplies ET0 (higher temp = dries faster = fewer days)
    function getTempModifier(tempRange) {
        const map = {
            'cold':   1.40,  // 10-18°C  → dries slowly
            'mild':   1.00,  // 18-24°C  → reference
            'warm':   0.72,  // 24-30°C  → dries faster
            'hot':    0.45,  // 30-40°C  → dries much faster (Dubai summers)
        };
        return map[tempRange] || 1.00;
    }

    // Sfactor = soil/pot modifier
    const Sfactor = {
        terracotta:    0.80,  // porous → dries 20% faster
        plastic:       1.00,  // standard
        ceramic:       1.15,  // glazed → retains more
        'self-water':  2.20,  // reservoir → much longer interval
    };

    // Light modifier
    function getLightModifier(light) {
        return { low: 1.35, medium: 1.00, bright: 0.80, 'direct-sun': 0.55 }[light] || 1.0;
    }

    // ── Affiliate products ────────────────────────────────────
    const PRODUCTS = {
        succulent:  { icon: '💧', name: 'XLUX Soil Moisture Meter',        asin: 'B07KBKXZL1', price: '$11.99' },
        tropical:   { icon: '💦', name: 'LEVOIT Humidifier for Plants',    asin: 'B08L73ZT3N', price: '$79.99' },
        fern:       { icon: '🌊', name: 'LEVOIT Humidifier',               asin: 'B08L73ZT3N', price: '$79.99' },
        herb:       { icon: '🌱', name: 'Miracle-Gro All-Purpose Food',    asin: 'B00BIO560G', price: '$13.49' },
        snake:      { icon: '📡', name: 'XLUX Soil Moisture Meter',        asin: 'B07KBKXZL1', price: '$11.99' },
        orchid:     { icon: '🌸', name: 'Orchid Potting Mix Pro',          asin: 'B01MR8B8WP', price: '$19.99' },
        pothos:     { icon: '🏺', name: 'LECHUZA Self-Watering Planter',   asin: 'B07N1CLX3J', price: '$89.00' },
        monstera:   { icon: '🏺', name: 'LECHUZA Self-Watering Planter',   asin: 'B07N1CLX3J', price: '$89.00' },
        cactus:     { icon: '📡', name: 'XLUX Soil Moisture Meter',        asin: 'B07KBKXZL1', price: '$11.99' },
        peace:      { icon: '💦', name: 'Govee Smart Humidifier',          asin: 'B08W5DVPFZ', price: '$59.99' },
    };

    // ── Form Submit ───────────────────────────────────────────
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const plant    = document.getElementById('plant-type').value;
        const pot      = document.querySelector('input[name="pot-type"]:checked')?.value  || 'plastic';
        const light    = document.querySelector('input[name="light-level"]:checked')?.value || 'medium';
        const tempRange = document.querySelector('input[name="temperature-range"]:checked')?.value || 'mild';

        if (!plant) return;

        // ── ET Formula: W = (Kc × ET0) × Sfactor × TempMod × LightMod
        const kc       = Kc[plant]             || 0.70;
        const sfactor  = Sfactor[pot]          || 1.00;
        const tempMod  = getTempModifier(tempRange);
        const lightMod = getLightModifier(light);

        const rawDays = (kc * ET0_base) * sfactor * tempMod * lightMod;
        const days    = Math.max(1, Math.round(rawDays));

        // Build formula breakdown
        const formulaBreakdown = `W = (${kc} × ${ET0_base}) × ${sfactor} × ${tempMod.toFixed(2)} × ${lightMod.toFixed(2)} = ${rawDays.toFixed(1)} → ${days} days`;

        // Update UI — main result
        daysResult.textContent = days;
        msgResult.textContent  = buildMessage(plant, pot, days, plantNames[plant]);

        // ET breakdown detail
        renderETBreakdown(formulaBreakdown, plant, pot, light, tempRange, kc, sfactor, tempMod, lightMod, days);

        // Affiliate product
        renderAffiliateCard(plant, pot, days);

        // Show result
        container.classList.add('show-result');
        if (navigator.vibrate) navigator.vibrate(50);

        // Weekly plan gate
        const savedEmail = localStorage.getItem('pm_lead_email');
        if (!savedEmail) {
            setTimeout(function() { renderWeeklyGate(plant, days); }, 1200);
        } else {
            renderWeeklyPlan(plant, days, savedEmail);
        }

        // Share buttons
        renderWaterShareButtons(plantNames[plant], days);
    });

    // ── Message Builder ───────────────────────────────────────
    function buildMessage(plant, pot, days, plantName) {
        const tips = {
            terracotta: 'Terracotta pots dry quickly — check soil 2 days before scheduled watering.',
            'self-water': 'Your self-watering pot handles the rest — just refill the reservoir monthly.',
        };
        const tip = tips[pot] || 'Check the top 2 inches of soil before each watering.';
        return `Water your ${plantName} every ${days} days. ${tip}`;
    }

    // ── ET Breakdown Panel ────────────────────────────────────
    function renderETBreakdown(formula, plant, pot, light, temp, kc, sf, tm, lm, days) {
        const wrap = document.getElementById('pm-et-breakdown-wrap');
        if (!wrap) return;
        wrap.innerHTML = `
        <div class="pm-et-breakdown">
            <strong>How we calculated this:</strong>
            <code class="pm-et-formula">W = (Kc × ET₀) × Sfactor × TempMod × LightMod</code>
            <code class="pm-et-formula" style="font-size:0.75rem;color:rgba(255,255,255,0.6)">${formula}</code>
            <span style="font-size:0.8rem">
                Kc (${plantNames[plant] || plant}) = ${kc} |
                Pot factor = ${sf} |
                Temp mod = ${tm.toFixed(2)} |
                Light mod = ${lm.toFixed(2)}
            </span>
        </div>`;
    }

    // ── Affiliate Card ────────────────────────────────────────
    function renderAffiliateCard(plant, pot, days) {
        const wrap = document.getElementById('pm-affiliate-wrap');
        if (!wrap) return;

        const p = PRODUCTS[plant] || PRODUCTS.pothos;
        const tag   = 'plantsmag-20';
        const tagAE = 'plantsmag-ae-21';

        wrap.innerHTML = `
        <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.35);margin-bottom:10px;">
            Recommended for your ${plantNames[plant] || plant}
        </div>
        <a href="https://www.amazon.com/dp/${p.asin}?tag=${tag}" target="_blank" rel="nofollow noopener" class="pm-product-card">
            <div class="pm-product-icon">${p.icon}</div>
            <div class="pm-product-info">
                <div class="pm-product-name">${p.name}</div>
                <div class="pm-product-price">${p.price} — Amazon US →</div>
            </div>
            <svg class="pm-product-arrow" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
        <a href="https://www.amazon.ae/dp/${p.asin}?tag=${tagAE}" target="_blank" rel="nofollow noopener" class="pm-product-card" style="margin-top:8px;">
            <div class="pm-product-icon">🇦🇪</div>
            <div class="pm-product-info">
                <div class="pm-product-name">${p.name}</div>
                <div class="pm-product-price">Amazon UAE →</div>
            </div>
            <svg class="pm-product-arrow" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>`;
    }

    // ── Weekly Plan Gate ──────────────────────────────────────
    function renderWeeklyGate(plant, days) {
        const wrap = document.getElementById('pm-weekly-gate-wrap');
        if (!wrap) return;
        wrap.innerHTML = `
        <div class="pm-weekly-gate" id="pm-wg">
            <h4>📅 Want Your Full Weekly Care Calendar?</h4>
            <p>Get a personalized weekly watering + fertilizing schedule for your ${plantNames[plant] || plant} — free, sent to your email.</p>
            <form id="pm-water-lead-form" style="display:flex;gap:10px;max-width:380px;margin:0 auto;">
                <input type="email" id="pm-water-email" placeholder="Your email..."
                    style="flex:1;padding:11px 14px;background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.15);border-radius:10px;color:#fff;font-size:0.9rem;outline:none;font-family:inherit;">
                <button type="submit" style="padding:11px 18px;background:linear-gradient(135deg,#16a34a,#22c55e);border:none;border-radius:10px;color:#fff;font-weight:700;cursor:pointer;font-size:0.875rem;font-family:inherit;white-space:nowrap;">
                    Send Plan →
                </button>
            </form>
            <p style="font-size:0.72rem;color:rgba(255,255,255,0.25);margin-top:10px;">🔒 One email. No spam. Unsubscribe anytime.</p>
        </div>`;

        document.getElementById('pm-water-lead-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('pm-water-email').value.trim();
            if (!email) return;
            submitWaterLead(email, plant, days);
        });
    }

    function submitWaterLead(email, plant, days) {
        localStorage.setItem('pm_lead_email', email);

        fetch('https://plantsmag.com/wp-json/pm/v1/capture-lead', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email:        email,
                lead_type:    'watering',
                plant_name:   plantNames[plant] || plant,
                watering_days: days,
                asin:         (PRODUCTS[plant] || PRODUCTS.pothos).asin
            })
        }).catch(function() {});

        document.getElementById('pm-wg').innerHTML = `
        <div style="text-align:center;padding:10px 0;">
            <div style="font-size:36px;margin-bottom:10px;">✅</div>
            <h4 style="color:#4ade80;">Weekly Plan Sent!</h4>
            <p style="color:rgba(255,255,255,0.5);font-size:0.85rem;">Check ${email} for your personalized care calendar.</p>
        </div>`;

        renderWeeklyPlan(plant, days, email);
    }

    function renderWeeklyPlan(plant, days, email) {
        // Already shown inline after success
    }

    // ── Share Buttons (Watering) ──────────────────────────────
    function renderWaterShareButtons(plantName, days) {
        const wrap = document.getElementById('pm-water-share-wrap');
        if (!wrap) return;
        const url  = encodeURIComponent('https://plantsmag.com/watering-calculator/');
        const text = encodeURIComponent(`I just found out my ${plantName} needs watering every ${days} days! 💧 Free calculator at PlantsMag:`);
        wrap.innerHTML = `
        <div class="pm-share-panel">
            <a href="https://wa.me/?text=${text}%20${url}" target="_blank" class="pm-share-btn pm-share-whatsapp">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
                Share on WhatsApp
            </a>
        </div>
        <p class="pm-share-label">Help your friends keep their plants alive 🌱</p>`;
    }

    // ── Close ─────────────────────────────────────────────────
    const closeSheet = () => container.classList.remove('show-result');
    closeBtn.addEventListener('click', closeSheet);
    overlay.addEventListener('click', closeSheet);

    let startY;
    const sheet = document.querySelector('.pm-bottom-sheet');
    if (sheet) {
        sheet.addEventListener('touchstart', e => { startY = e.touches[0].clientY; }, { passive: true });
        sheet.addEventListener('touchmove',  e => { if (e.touches[0].clientY - startY > 50) closeSheet(); }, { passive: true });
    }
});
