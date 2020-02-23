'use strict';

let io = new IO();
let container = document.getElementById('circle-container');

var max = 0;
var min = 0;
var column_color = null;

resize();
window.onresize = resize;

load_settings().then(settings => {
    let default_settings = {
        'circle': {
            'transition': {'size': '.5s', 'color': '.5s'},
            'column_color': 'lf/hf'
        }
    };
    settings = merge(default_settings, settings);
    column_color = settings.circle.column_color;
    set_css_var('--size-transition', settings.circle.transition.size);
    set_css_var('--color-transition', settings.circle.transition.color);
});

io.on('connect', () => {
    console.log('connected');
    io.subscribe('rr_interval');
    io.subscribe('cardiac_features');

});


io.on('rr_interval', (data) => {
    let row = data[Object.keys(data)[Object.keys(data).length - 1]]; // Last row
    let column = Object.keys(row)[0]; // First column
    let value = row[column]; // Value
    value = Math.tanh(value); // Ensure value between 0 and 1
    value = 1 - value; // circle radius should decrease when interval increase (ie. when BPM decrease)
    let px = (value * (max - min) + min) + 'px'; // Transform to pixels
    set_css_var('--circle-width', px); // Set the width
    set_css_var('--circle-height', px); // Set the height

    // Display BPM value in table
    let bpm = 60 / value;
    document.getElementById('bpm').innerHTML = bpm.toFixed(0) + ' bpm';
});

io.on('cardiac_features', (data) => {
    let row = data[Object.keys(data)[Object.keys(data).length - 1]]; // Last row

    for (let column in row) {
        // Display feature value in table
        document.getElementById(column).innerHTML = row[column].toFixed(2);
    }
    // Set circle color from the chosen feature
    let value = row[column_color]; // Value between 0 and 1
    // circle.style.backgroundColor = color_gradient(value * 100)
    set_css_var('--circle-opacity', .7);
    set_css_var('--circle-color', color_gradient(value))
});


Number.prototype.between = function (a, b, inclusive = true) {
    let min = Math.min.apply(Math, [a, b]),
        max = Math.max.apply(Math, [a, b]);
    return inclusive ? this >= min && this <= max : this > min && this < max;
};

let _gradientColors =
    [[.0, .15, "#ff3030"],
        [.15, .30, "#ff5d4b"],
        [.30, .45, "#ff8a4b"],
        [.45, .60, "#ffc04b"],
        [.60, .75, "#ffe74b"],
        [.75, .90, "#9aff26"],
        [.90, 1.1, "#02ff8a"],
    ];

/**
 * Return color gradient
 *
 * @param {number}  x variable in [0, 1]
 */
function color_gradient(x) {
    let color = null;
    _gradientColors.forEach(function (_gradientInterval) {
        if (x.between(_gradientInterval[0], _gradientInterval[1])) {
            color = _gradientInterval[2]
        }
    });
    return color
}

/**
 * Set a CSS variable
 *
 * @param {string} name: variable name in css
 * @param {string|number} value
 */
function set_css_var(name, value) {
    document.documentElement.style.setProperty(name, value);
}

/**
 * Estimate min/max of circle giveb container size
 */
function resize() {
    let width = container.clientWidth;
    let height = container.clientHeight;
    max = width < height ? width : height;
    min = max / 4;
}
