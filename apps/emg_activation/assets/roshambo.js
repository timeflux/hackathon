'use strict';

class Roshambo {

    /**
     * Initialize the Oddball experiment
     *
     * @param {IO} io - Timeflux IO instance
     */
    constructor(io, options = {}) {

        this.io = io;

        // Overwrite default options with given options
        let default_options = {
                'calibration_rounds': 2,
                'fixation_duration': 2000,
                'trial_duration': 7000,
                'highlight_duration': 1500,
                'ids': ['rock', 'paper', 'scissors', 'rest']
            }
        ;
        this.options = merge(default_options, options);

        // Initialize
        // this._init();

        // Get HTML elements for faster access
        this._cells = {};
        for (let id in this.options.targets) {
            this._cells[id] = document.getElementById(id);
        }
    }

    /**
     * Calibration
     */
    async calibrate() {
        this.io.event('calibration_starts');
        // this.io.event('calibration-baseline_starts');
        // await sleep(this.options.calibration.baseline_duration);
        // this.io.event('calibration-baseline_stops');
        let ids = this.options.ids;
        for (let i = 0; i < this.options.calibration_rounds; i++) {
            this._shuffle(ids);
            for (const id of ids) {
                let meta = {'id': id};
                document.getElementById('fixation_cross').classList.toggle('show');
                await sleep(this.options.fixation_duration);
                this.io.event('trial_starts', meta);
                // show image
                document.getElementById('fixation_cross').classList.toggle('show');
                document.getElementById(id).classList.toggle('show');
                await sleep(this.options.trial_duration);
                // hide image
                this.io.event('trial_stops', meta);
                // stop showing
                document.getElementById(id).classList.toggle('show');
            }
        }
        this.io.event('calibration_stops');
    }

    /**
     * Prediction
     */
    async classify() {
        this.io.event('classify_starts');
        let meta = {'id': null};
        await sleep(this.options.fixation_duration);
        this.io.event('trial_starts', meta);
        // hide all choices

        // show image question
        document.getElementById('question').classList.toggle('show');

        await sleep(this.options.trial_duration);
        // hide image
        this.io.event('trial_stops', meta);
        // listen to prediction
        // todo
        // hide question and show predicted image
        document.getElementById('question').classList.toggle('show');
        // send event prediction stops
        this.io.event('classify_stops');
    }

    /**
     * Shuffle an array
     *
     * This is done in-place. Make a copy first with .slice(0) if you don't want to
     * modify the original array.
     *
     * @param {array} array
     *
     * @see:https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle#The_modern_algorithm
     */
    _shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }
    _init(){
        var elements = document.getElementsByClassName('choice');
        for (var i = 0; i < elements.length; i++) {
            elements[i].classList.remove('show');
            }
    }

}

