import axios from 'axios';
import 'dotenv/config';

const API_KEY = process.env.GEMINI_API_KEY;

async function testModel(modelName) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${API_KEY}`;
  try {
    const res = await axios.post(url, {
      contents: [{ parts: [{ text: "Hello" }] }]
    });
    console.log(`[SUCCESS] ${modelName} is working.`);
  } catch (err) {
    console.log(`[ERROR] ${modelName} failed with status:`, err.response?.status);
  }
}

async function run() {
  await testModel('gemini-2.0-flash');
  await testModel('gemini-1.5-flash');
  await testModel('gemini-1.5-pro');
}

run();
