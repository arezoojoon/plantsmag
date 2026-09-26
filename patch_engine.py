import re

def patch_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. Update wordpress.js (status to draft)
patch_file(r'd:\project\plantsmag\engine\lib\wordpress.js', [
    ("const status = 'publish';", "const status = 'draft';")
])

# 2. Update plant-care.js (export pickTopic and remove 2024 from Prompt)
patch_file(r'd:\project\plantsmag\engine\strategies\plant-care.js', [
    ("function pickTopic()", "export function pickTopic()"),
    ("A 2024 Comparison", "A 2026 Comparison"), # just in case
])

# 3. Update comparison.js (export pickTopic)
patch_file(r'd:\project\plantsmag\engine\strategies\comparison.js', [
    ("function pickTopic()", "export function pickTopic()"),
    ("A 2024 Comparison", "A 2026 Comparison"),
    ("for 2024", "for 2026"),
])

# 4. Update trending-rss.js
patch_file(r'd:\project\plantsmag\engine\strategies\trending-rss.js', [
    ("2024", "2026")
])

# 5. Update seo-automation-cron.js
cron_js = r'd:\project\plantsmag\engine\seo-automation-cron.js'
with open(cron_js, 'r', encoding='utf-8') as f:
    cron_content = f.read()

# Disable comparison and trending-rss
cron_content = cron_content.replace("""  cron.schedule('0 15 * * *', () => {
    logger.info('[CRON] Triggered: comparison (15:00)');
    runOnce('comparison');
  });""", """  // cron.schedule('0 15 * * *', () => {
  //   logger.info('[CRON] Triggered: comparison (15:00)');
  //   runOnce('comparison');
  // });""")

cron_content = cron_content.replace("""  cron.schedule('0 21 * * *', () => {
    logger.info('[CRON] Triggered: trending-rss (21:00)');
    runOnce('trending-rss');
  });""", """  // cron.schedule('0 21 * * *', () => {
  //   logger.info('[CRON] Triggered: trending-rss (21:00)');
  //   runOnce('trending-rss');
  // });""")

# Pre-flight check
preflight_code = """
    let topicStr = '';
    if (strategyName === 'trending-rss') {
      logger.info('Fetching trending plant topics from RSS…');
      let rssFeed = [];
      try {
        rssFeed = await getTrendingPlantTopics();
        logger.info(`Fetched ${rssFeed.length} trending topics`);
      } catch (rssErr) {
        logger.warn(`RSS fetch failed, using fallback topics: ${rssErr.message}`);
      }
      topicStr = rssFeed.length > 0 ? rssFeed[0].title : 'trending plant';
      prompt = strategy.getPrompt(rssFeed);
    } else {
      topicStr = strategy.pickTopic ? strategy.pickTopic() : '';
      prompt = strategy.getPrompt();
    }

    if (topicStr) {
      logger.info(`Pre-flight checking duplicate for topic: ${topicStr}`);
      const keyword = topicStr.split(' ').slice(0, 3).join('+');
      try {
        const res = await fetch(`https://plantsmag.com/wp-json/wp/v2/posts?search=${encodeURIComponent(keyword)}&per_page=1`);
        const data = await res.json();
        if (data && data.length > 0) {
          logger.warn(`[PRE-FLIGHT] Topic already exists: ${topicStr}. Skipping generation.`);
          return;
        }
      } catch (e) {
        logger.error('Pre-flight check failed: ' + e.message);
      }
    }
    
    logger.info('Prompt generated – calling Gemini API…');
"""

# Replace the block 1 and prompt generation
old_block = """    let prompt;
    if (strategyName === 'trending-rss') {
      logger.info('Fetching trending plant topics from RSS…');
      let rssFeed = [];
      try {
        rssFeed = await getTrendingPlantTopics();
        logger.info(`Fetched ${rssFeed.length} trending topics`);
      } catch (rssErr) {
        logger.warn(`RSS fetch failed, using fallback topics: ${rssErr.message}`);
      }
      prompt = strategy.getPrompt(rssFeed);
    } else {
      prompt = strategy.getPrompt();
    }

    logger.info('Prompt generated – calling Gemini API…');"""

cron_content = cron_content.replace(old_block, preflight_code)

# Slug lock check
slug_lock_code = """
    // 2.5 Slug lock check
    logger.info(`Checking slug lock for: ${article.slug}`);
    try {
      const slugRes = await fetch(`https://plantsmag.com/wp-json/wp/v2/posts?slug=${article.slug}`);
      const slugData = await slugRes.json();
      if (slugData && slugData.length > 0) {
        logger.warn(`[SLUG LOCK] Slug already exists: ${article.slug}. Aborting publish.`);
        return;
      }
    } catch (e) { }

    // 3. Extract keywords for internal linking
"""

cron_content = cron_content.replace("// 3. Extract keywords for internal linking", slug_lock_code)

with open(cron_js, 'w', encoding='utf-8') as f:
    f.write(cron_content)

print("Engine files patched successfully!")
