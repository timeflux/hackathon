'use strict';

let io = new IO();

load_settings().then(settings => {
//    In case some settings should be loaded from the graph's config
});

// subscribe to useful streams on new connection
io.on('connect', () => {
    console.log('connected');
    io.subscribe('eeg_relative_powers');
    io.subscribe('eeg_absolute_powers');
    io.subscribe('blink');
});

// Prepare elements from DOM
const columns = ['delta', 'theta', 'alpha', 'beta', 'gamma']; // columns of EMG activation bursts
let _td_relative_features = {};
let _td_absolute_features = {};
columns.forEach(function (column) {
    _td_relative_features[column] = document.getElementById(column + '_relative');
    _td_absolute_features[column] = document.getElementById(column + '_absolute');
});

// Display relative powers in table
io.on('eeg_relative_powers', (data) => {
    // Get last row of data
    let keys = Object.keys(data);
    let row = data[keys[keys.length - 1]];
    // Set value
    for (let column in row) {
        let band = column.split('_')[1];
        _td_relative_features[band].innerHTML = row[column].toFixed(2);
    }
});

// Display absolute powers in table
io.on('eeg_absolute_powers', (data) => {
    // Get last row of data
    let keys = Object.keys(data);
    let row = data[keys[keys.length - 1]];
    // Set value
    for (let column in row) {
        let band = column.split('_')[1];
        _td_absolute_features[band].innerHTML = row[column].toFixed(2);
    }
});

// Mimic blink
io.on('blink', (data) => {
    let keys = Object.keys(data);
    let row = data[keys[keys.length - 1]]; // Get last row of data
    let lens_top = 25 + 25 * row[Object.keys(row)[0]];
    set_css_var("--lens-top", lens_top.toString() + '%')
});

/**
 * Set a CSS variable
 *
 * @param {string} variable name
 * @param {string|number} value
 */
function set_css_var(name, value) {
    document.documentElement.style.setProperty(name, value);
}
