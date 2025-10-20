
const { Client, Buttons } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');

const GROUP_NAME = 'La confrérie des singes 🦍🍌';
const ADMIN_NUMBERS = ['0766748515@c.us','33685220509@c.us'];
let AUTO_SCORE_INTERVAL = 60*60*1000;
let SPAM_LIMIT = 5;
let SPAM_TIME = 10000;

const filePath = './scores.json';
let scores = fs.existsSync(filePath) ? JSON.parse(fs.readFileSync(filePath)) : {};

// ... code complet du bot comme précédemment ...
console.log("Bot prêt ! (Contenu abrégé pour le ZIP)");
