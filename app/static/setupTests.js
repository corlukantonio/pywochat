// setupTests.js
import { JSDOM } from 'jsdom';

const jsdom = new JSDOM('<!doctype html><html><body></body></html>');
global.window = jsdom.window;
global.document = jsdom.window.document;

// Add any other global variables you need for your tests here
global.$ = require('jquery');
