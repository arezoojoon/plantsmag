/**
 * PlantsMag — Disease Finder v2.0
 * Soft Gate Lead Magnet + Affiliate Routing + Viral Share
 */
jQuery(document).ready(function($) {
    const uploadArea    = $('#pm-upload-area');
    const fileInput     = $('#pm-disease-image');
    const previewImg    = $('#pm-preview-img');
    const uploadContent = $('.pm-upload-content');
    const analyzeBtn    = $('#pm-analyze-btn');
    const container     = $('.pm-disease-app');
    const closeBtn      = $('#pm-close-disease');

    let currentImageBase64 = null;
    let currentDiagData    = null;

    // ── Affiliate product map ─────────────────────────────────
    const AFFILIATE_DB = {
        'fungal':       { icon: '🍄', name: 'Bonide Copper Fungicide', price: '$14.99', asin: 'B00BS3NT4Q' },
        'spider mite':  { icon: '🕷️', name: 'Neem Oil Spray (Organic)', price: '$12.99', asin: 'B07M7KPPPN' },
        'root rot':     { icon: '🌊', name: 'Hydrogen Peroxide 3%',     price: '$9.99',  asin: 'B00ILNHA6G' },
        'overwater':    { icon: '💧', name: 'XLUX Soil Moisture Meter', price: '$11.99', asin: 'B07KBKXZL1' },
        'nutrient':     { icon: '🧪', name: 'Miracle-Gro Liquid Fertilizer', price: '$13.49', asin: 'B00BIO560G' },
        'scale':        { icon: '🪲', name: 'Insecticidal Soap Spray',  price: '$8.99',  asin: 'B00B4VE6H8' },
        'powdery':      { icon: '⬜', name: 'Garden Safe Fungicide',    price: '$10.99', asin: 'B0001YVDE0' },
        'default':      { icon: '💡', name: 'Spider Farmer LED Grow Light', price: '$109', asin: 'B07RHB8P5C' },
    };
    // Secondary always shown
    const MOISTURE_METER = { icon: '📡', name: 'XLUX Soil Moisture Meter', price: '$11.99', asin: 'B07KBKXZL1' };

    // ── Danger levels ────────────────────────────────────────
    const DANGER_MAP = {
        low:      { pct: 22, cls: 'danger-low',      badge: 'badge-low',      emoji: '🟢', label: 'Low Risk',      text: 'Your plant is stressed but recoverable.' },
        medium:   { pct: 50, cls: 'danger-medium',   badge: 'badge-medium',   emoji: '🟡', label: 'Medium Risk',   text: 'Act within 3-5 days to prevent spread.' },
        high:     { pct: 78, cls: 'danger-high',     badge: 'badge-high',     emoji: '🔴', label: 'High Risk',     text: 'Immediate treatment needed — days matter.' },
        critical: { pct: 96, cls: 'danger-critical', badge: 'badge-critical', emoji: '🚨', label: 'Critical!',     text: 'Your plant may die without urgent intervention.' },
    };

    // ── Trigger file input ────────────────────────────────────
    uploadArea.on('click', function() { fileInput.trigger('click'); });

    fileInput.on('change', function(e) {
        const file = e.target.files[0];
        if (!file || !file.type.match('image.*')) return;

        const reader = new FileReader();
        reader.onload = function(event) {
            const img = new Image();
            img.onload = function() {
                const canvas = document.createElement('canvas');
                let w = img.width, h = img.height;
                const MAX = 800;
                if (w > h) { if (w > MAX) { h = h * MAX / w; w = MAX; } }
                else       { if (h > MAX) { w = w * MAX / h; h = MAX; } }
                canvas.width = w; canvas.height = h;
                canvas.getContext('2d').drawImage(img, 0, 0, w, h);
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

    // ── Analyze ───────────────────────────────────────────────
    analyzeBtn.on('click', function() {
        if (!currentImageBase64) return;
        container.addClass('is-loading');

        $.ajax({
            url:  pmDiseaseObj.ajaxUrl,
            type: 'POST',
            data: {
                action:       'pm_analyze_disease',
                nonce:        pmDiseaseObj.nonce,
                image_base64: currentImageBase64
            },
            success: function(response) {
                container.removeClass('is-loading');
                if (response.success && response.data) {
                    currentDiagData = response.data;
                    showResult(response.data);
                } else {
                    alert('Error: ' + (response.data?.message || 'Could not analyze image.'));
                }
            },
            error: function() {
                container.removeClass('is-loading');
                alert('Server connection failed. Please try again.');
            }
        });
    });

    // ── Show Result with Soft Gate ────────────────────────────
    function showResult(data) {
        const diagnosis  = data.diagnosis  || 'Unknown Condition';
        const severity   = (data.severity  || 'medium').toLowerCase();
        const explanation = data.explanation || '';

        // Set basic info
        $('#pm-diag-title').text(diagnosis);
        $('#pm-diag-text').text(explanation);

        // Danger gauge
        renderDangerGauge(severity, diagnosis);

        // Affiliate products
        renderProducts(diagnosis);

        // Show result panel (with treatment locked)
        container.addClass('show-result');
        if (navigator.vibrate) navigator.vibrate(50);

        // Check if email already captured
        const savedEmail = localStorage.getItem('pm_lead_email');
        if (savedEmail) {
            unlockTreatment(data, savedEmail, false);
        } else {
            // Lock treatment + show gate after 1.5s
            setTimeout(function() { openSoftGate(data); }, 1500);
        }

        // WhatsApp / Pinterest share
        renderShareButtons(diagnosis, severity);
    }

    // ── Danger Gauge Renderer ─────────────────────────────────
    function renderDangerGauge(severity, diseaseName) {
        const d = DANGER_MAP[severity] || DANGER_MAP.medium;
        const gaugeHtml = `
        <div class="pm-danger-gauge">
            <div class="pm-danger-label">Threat Level — ${diseaseName}</div>
            <div class="pm-danger-track">
                <div class="pm-danger-fill ${d.cls}" data-pct="${d.pct}" style="width:0%"></div>
            </div>
            <div class="pm-danger-levels">
                <span>Low</span><span>Medium</span><span>High</span><span>Critical</span>
            </div>
            <div class="pm-danger-badge ${d.badge}">${d.emoji} ${d.label}</div>
            <p style="font-size:0.8rem;color:rgba(255,255,255,0.45);margin:6px 0 0;">${d.text}</p>
        </div>`;
        $('#pm-danger-gauge-wrap').html(gaugeHtml);
        // Animate fill
        setTimeout(function() {
            $('.pm-danger-fill').css('width', d.pct + '%');
        }, 100);
    }

    // ── Product Renderer ──────────────────────────────────────
    function renderProducts(diagnosis) {
        const diag = diagnosis.toLowerCase();
        let primary = AFFILIATE_DB.default;

        for (const [key, val] of Object.entries(AFFILIATE_DB)) {
            if (diag.includes(key)) { primary = val; break; }
        }

        const makeCard = (p, tag) => `
        <a href="https://www.amazon.com/dp/${p.asin}?tag=${tag}"
           target="_blank" rel="nofollow noopener" class="pm-product-card">
            <div class="pm-product-icon">${p.icon}</div>
            <div class="pm-product-info">
                <div class="pm-product-name">${p.name}</div>
                <div class="pm-product-price">${p.price} on Amazon →</div>
            </div>
            <svg class="pm-product-arrow" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>`;

        const html = `
        <div class="pm-affiliate-panel">
            <div class="pm-affiliate-panel-title">🛒 Recommended Products</div>
            ${makeCard(primary,       'plantsmag-20')}
            ${makeCard(MOISTURE_METER, 'plantsmag-20')}
        </div>`;

        $('#pm-affiliate-wrap').html(html);
    }

    // ── Soft Gate Modal ───────────────────────────────────────
    function openSoftGate(data) {
        const severity  = (data.severity || 'medium').toLowerCase();
        const diagnosis = data.diagnosis || 'plant disease';
        const d = DANGER_MAP[severity] || DANGER_MAP.medium;

        const modalHtml = `
        <div class="pm-softgate-overlay" id="pm-softgate">
            <div class="pm-softgate-modal">
                <div class="pm-sg-icon">🌿</div>
                <h2 class="pm-sg-headline">
                    Your plant has<br>
                    <span>${diagnosis}</span>
                </h2>
                <p class="pm-sg-subtext">
                    We found a <strong style="color:${severity === 'high' || severity === 'critical' ? '#f87171' : '#fbbf24'}">${d.label}</strong> issue.
                    Get your free personalized treatment roadmap + product recommendations sent directly to your email.
                </p>
                <ul class="pm-sg-benefits">
                    <li><span class="sg-check">✓</span> Step-by-step 7-day treatment plan</li>
                    <li><span class="sg-check">✓</span> Exact products that fix ${diagnosis}</li>
                    <li><span class="sg-check">✓</span> Prevention guide to stop recurrence</li>
                </ul>
                <form class="pm-sg-form" id="pm-sg-lead-form">
                    <div class="pm-sg-input-wrap">
                        <svg width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                            <polyline points="22,6 12,13 2,6"/>
                        </svg>
                        <input type="email" class="pm-sg-email-input" id="pm-sg-email"
                               placeholder="Your email address..." required>
                    </div>
                    <button type="submit" class="pm-sg-submit-btn" id="pm-sg-btn">
                        <div class="btn-spinner"></div>
                        <span class="btn-text">📧 Email Me Free Treatment Plan →</span>
                    </button>
                </form>
                <div class="pm-sg-skip">
                    <a href="#" id="pm-sg-skip-link">Skip — show basic info only</a>
                </div>
                <p class="pm-sg-privacy">🔒 No spam. One email. Unsubscribe anytime.</p>
            </div>
        </div>`;

        $('body').append(modalHtml);
        requestAnimationFrame(function() {
            $('#pm-softgate').addClass('active');
        });

        // Submit form
        $('#pm-sg-lead-form').on('submit', function(e) {
            e.preventDefault();
            const email = $('#pm-sg-email').val().trim();
            if (!email) return;
            submitLead(email, data);
        });

        // Skip
        $('#pm-sg-skip-link').on('click', function(e) {
            e.preventDefault();
            closeSoftGate();
            unlockTreatment(data, null, true);
        });
    }

    function closeSoftGate() {
        $('#pm-softgate').removeClass('active');
        setTimeout(function() { $('#pm-softgate').remove(); }, 350);
    }

    // ── Submit Lead to n8n Webhook ────────────────────────────
    function submitLead(email, data) {
        const btn = $('#pm-sg-btn');
        btn.addClass('loading');

        const payload = {
            email:             email,
            lead_type:         'disease',
            disease_name:      data.diagnosis     || 'Unknown',
            plant_name:        data.plant_name     || 'Your Plant',
            severity:          data.severity       || 'medium',
            treatment_keyword: data.treatment_keyword || 'plant care',
            asin:              getAsinForDisease(data.diagnosis || ''),
            explanation:       data.explanation    || ''
        };

        $.ajax({
            url:         'https://plantsmag.com/wp-json/pm/v1/capture-lead',
            type:        'POST',
            contentType: 'application/json',
            data:        JSON.stringify(payload),
            timeout:     12000,
            success: function() {
                localStorage.setItem('pm_lead_email', email);
                showSuccessState(email);
                setTimeout(function() {
                    closeSoftGate();
                    unlockTreatment(data, email, false);
                }, 2000);
            },
            error: function() {
                // Even on error, still unlock — lead was captured locally
                localStorage.setItem('pm_lead_email', email);
                closeSoftGate();
                unlockTreatment(data, email, false);
            }
        });
    }

    function showSuccessState(email) {
        const form = $('#pm-sg-lead-form');
        form.hide();
        form.parent().append(`
            <div class="pm-sg-success visible">
                <div class="pm-sg-success-icon">✅</div>
                <h3>Check your inbox!</h3>
                <p>Your personalized treatment plan is on its way to<br><strong style="color:#4ade80">${email}</strong></p>
            </div>`);
    }

    // ── Unlock Treatment ──────────────────────────────────────
    function unlockTreatment(data, email, skipped) {
        const treatmentHtml = `
        <div class="pm-treatment-roadmap">
            <h4 style="color:#4ade80;margin-bottom:12px;font-size:1rem;">
                ${skipped ? '📋 Basic Treatment Info' : '🗺️ Your Personalized Treatment Roadmap'}
            </h4>
            <div style="color:rgba(255,255,255,0.7);font-size:0.9rem;line-height:1.7;">
                ${data.treatment_desc || data.treatment || 'Apply appropriate treatment according to the disease identified.'}
            </div>
            ${!skipped ? `
            <div style="margin-top:16px;padding:12px;background:rgba(34,197,94,0.08);border-radius:10px;border-left:3px solid #22c55e;">
                <p style="font-size:0.82rem;color:#4ade80;font-weight:600;margin-bottom:4px;">💌 Full plan sent to ${email}</p>
                <p style="font-size:0.78rem;color:rgba(255,255,255,0.45);">Check your email for a 7-day recovery plan with exact product quantities.</p>
            </div>` : ''}
        </div>`;
        $('#pm-treatment-wrap').html(treatmentHtml);
        $('.pm-treatment-locked').addClass('unlocked');
    }

    // ── Share Buttons ─────────────────────────────────────────
    function renderShareButtons(diagnosis, severity) {
        const url     = encodeURIComponent('https://plantsmag.com/plant-disease-finder/');
        const text    = encodeURIComponent(`My plant has ${diagnosis}! I used PlantsMag free AI diagnosis tool 🌿`);
        const waLink  = `https://wa.me/?text=${text}%20${url}`;
        const pinLink = `https://pinterest.com/pin/create/button/?url=${url}&description=${text}`;

        const html = `
        <div class="pm-share-panel" id="pm-share-panel">
            <a href="${waLink}" target="_blank" class="pm-share-btn pm-share-whatsapp">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
                WhatsApp
            </a>
            <a href="${pinLink}" target="_blank" class="pm-share-btn pm-share-pinterest">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.373 0 0 5.373 0 12c0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738a.36.36 0 0 1 .083.345l-.333 1.36c-.053.22-.174.267-.402.161-1.499-.698-2.436-2.889-2.436-4.649 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.632-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0z"/></svg>
                Pinterest
            </a>
            <button class="pm-share-btn pm-share-copy" id="pm-copy-link">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                Copy Link
            </button>
        </div>
        <p class="pm-share-label">Share your result and help other plant parents 🌱</p>`;

        $('#pm-share-wrap').html(html);

        $('#pm-copy-link').on('click', function() {
            navigator.clipboard.writeText('https://plantsmag.com/plant-disease-finder/').then(function() {
                $('#pm-copy-link').html('<svg width="16" height="16" fill="none" stroke="#4ade80" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Copied!').css('color', '#4ade80');
                setTimeout(function() {
                    $('#pm-copy-link').html('<svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg> Copy Link').css('color', '');
                }, 2000);
            });
        });
    }

    // ── Helper: get ASIN for disease ──────────────────────────
    function getAsinForDisease(diagnosis) {
        const d = diagnosis.toLowerCase();
        for (const [key, val] of Object.entries(AFFILIATE_DB)) {
            if (d.includes(key)) return val.asin;
        }
        return AFFILIATE_DB.default.asin;
    }

    // ── Close / Reset ─────────────────────────────────────────
    const closeSheet = () => container.removeClass('show-result');

    closeBtn.on('click', function() {
        closeSheet();
        previewImg.hide().attr('src', '');
        uploadContent.show();
        uploadArea.removeClass('has-image');
        analyzeBtn.prop('disabled', true);
        currentImageBase64 = null;
        fileInput.val('');
        currentDiagData = null;
    });

    $('#pm-overlay-disease').on('click', closeSheet);

    let startY;
    const sheetContent = document.getElementById('pm-disease-result');
    if (sheetContent) {
        sheetContent.addEventListener('touchstart', e => { startY = e.touches[0].clientY; }, { passive: true });
        sheetContent.addEventListener('touchmove',  e => { if (e.touches[0].clientY - startY > 50) closeSheet(); }, { passive: true });
    }
});
