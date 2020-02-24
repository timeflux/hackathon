'use strict';


let io = new IO();
let roshambo = null;
let options = {};
const calibrate_button = document.getElementById('calibrate');
const start_button = document.getElementById('start');

let gaugeOptions = {
    lines: 1,
    angle: 0,
    lineWidth: 0.2,
    pointer: {
        legth: 0.9,
        strokeWidth: 0,
        color: '#ccc'
    },
    limitMax: 'false',
    percentColors:
        [[0.0, "#ffe74b"],
        [0.20, "#ffc04b"],
        [0.40, "#ff8a4b"],
        [0.60, "#ff5d4b"],
        [0.80, "#ff3030"]],
    strokeColor: '#E0E0E0',
    generateGradient: true
};

let target = document.getElementById('gauge');
let gauge = new Gauge(target).setOptions(gaugeOptions);

gauge.maxValue = 1;

load_settings().then(settings => {
    options = settings.roshambo;
    calibrate_button.addEventListener('click', calibrate);
    start_button.addEventListener('click', classify);
});


async function calibrate() {
    calibrate_button.classList.toggle('disabled');
    calibrate_button.disabled = true;
    roshambo = new Roshambo(io, options);
    await roshambo.calibrate();
    calibrate_button.disabled = false;
    start_button.disabled = false;
}

async function classify() {
    roshambo._init();
    // start_button.classList.toggle('disabled');
    await roshambo.classify();
    start_button.disabled = false
}

io.subscribe('events');
io.on('events', (data, meta) => {
    for (let timestamp in data) {
        try {
            if (data[timestamp]['label'] == 'predict') {
                data = JSON.parse(data[timestamp].data);
                document.getElementById(data.result).classList.toggle('show');
            }
        } catch (e) {
        }
    }
});

io.subscribe('emg_burst');
io.on('emg_burst', (data) => {
    let avg_activation = 0;
    let row = data[Object.keys(data)[Object.keys(data).length - 1]]; // Last row
    let n_columns = Object.keys(row).length;
    for (let column in row) {
        // Display feature value in table
        let value = row[column];
        document.getElementById(column).innerHTML = (value * 100).toFixed() + "%";
        avg_activation = avg_activation + value
    }
    gauge.set(avg_activation / n_columns);
});
