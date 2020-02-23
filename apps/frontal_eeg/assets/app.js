'use strict';

let io = new IO();

load_settings().then(settings => {
//    In case some settings should be loaded from the graph's config
});

io.on('connect', () => {
    console.log('connected');
    io.subscribe('eeg_relative_powers');
    io.subscribe('eeg_absolute_powers');
    io.subscribe('blink');

});

io.on('eeg_relative_powers', (data) => {
    // Get last row of data
    let keys = Object.keys(data);
    let row = data[keys[keys.length - 1]];
    // Set value
    for (let column in row) {
        let band = column.split('_')[1];
        document.getElementById(band + '_relative').innerHTML = row[column].toFixed(2);
    }
});

io.on('eeg_absolute_powers', (data) => {
    // Get last row of data
    let keys = Object.keys(data);
    let row = data[keys[keys.length - 1]];
    // Set value
    for (let column in row) {
        let band = column.split('_')[1];
        document.getElementById(band + '_absolute').innerHTML = row[column].toFixed(2);
    }
});

io.on('blink', (data) => {
    // Get last row of data
    let keys = Object.keys(data);
    let row = data[keys[keys.length - 1]];
    // Set value
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
