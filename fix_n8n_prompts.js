const fs = require('fs');
const path = require('path');

const dir = 'd:/project/plantsmag/';
const files = fs.readdirSync(dir).filter(f => f.startsWith('workflow_') && f.endsWith('.json'));

let anyModified = false;

for (const file of files) {
    const filePath = path.join(dir, file);
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    let modified = false;

    if (data.nodes) {
        for (const node of data.nodes) {
            if (node.name && node.name.toLowerCase().includes('gemini') && node.type && node.type.includes('httpRequest')) {
                if (node.parameters && node.parameters.body) {
                    let bodyText = node.parameters.body;
                    
                    // Apply replacements to kill the AI footprint
                    let newBody = bodyText.replace(/EXACTLY 2500 words/g, '800-1200 highly useful, concise words. DO NOT produce fluff. Google penalizes fluff.');
                    newBody = newBody.replace(/5 H2 sections \(350 words each\)/g, 'H2 sections (only as many as needed, max 150 words each, no fluff)');
                    newBody = newBody.replace(/Intro \(180 words\)/g, 'Intro (max 60 words)');
                    newBody = newBody.replace(/Conclusion \(120 words\)/g, 'Conclusion (max 60 words)');
                    newBody = newBody.replace(/Conclusion \(150 words\)/g, 'Conclusion (max 60 words)');
                    
                    if (newBody !== bodyText) {
                        node.parameters.body = newBody;
                        modified = true;
                    }
                }
            }
        }
    }

    if (modified) {
        fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
        console.log(`Fixed AI footprint in: ${file}`);
        anyModified = true;
    }
}

if (anyModified) {
    console.log("All workflows updated locally!");
} else {
    console.log("No workflows needed updating.");
}
