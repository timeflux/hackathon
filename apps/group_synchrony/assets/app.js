'use strict';

Number.prototype.between = function (a, b, inclusive = true) {
    var min = Math.min.apply(Math, [a, b]),
        max = Math.max.apply(Math, [a, b]);
    return inclusive ? this >= min && this <= max : this > min && this < max;
};

let _percentColors =
        [[0, 20, "#ffe74b"],
        [20, 40, "#ffc04b"],
        [40, 60, "#ff8a4b"],
        [60, 80, "#ff5d4b"],
        [80, 100, "#ff3030"]];

function color_gradient(x) {
    let color = null;
    _percentColors.forEach(function (_percentColor) {
        if (x.between(_percentColor[0], _percentColor[1])) {
            color = _percentColor[2]
        }
    })
    return color
}

let value_range = [0, 1]; // todo: set in config
function valueToPoint(value, index, total) {

    value = (value - value_range[0])/(value_range[1] - value_range[0])*100;
    var x = 0
    var y = -value * 0.9
    var angle = Math.PI * 2 / total * index
    var cos = Math.cos(angle)
    var sin = Math.sin(angle)
    var tx = x * cos - y * sin + 100
    var ty = x * sin + y * cos + 100
    return {x: tx, y: ty}
}

function generatePoints(stats) {
    var total = stats.length
    return stats.map(function (stat, index) {
        var point = valueToPoint(stat, index, total)
        if (point.x == null){
            point = {}
        }
        return point.x + ',' + point.y
    }).join(' ')
}

function updateStats(stats, previous_stats) {
    return stats.map(function (stat, index) {
        if (!stat.between(value_range[0], value_range[1])) {
            stat = previous_stats[index]
        }
        return stat
    })
}

let io = new IO();

load_settings().then(settings => {
    let polygon = new Vue({
        el: '#container',
        data: function () {
            return {
                sides: 3,
                stats: [.5, .5, .5, .5],
                points: generatePoints([.5, .5, .5, .5]),
                minRadius: 50,
            }
        }

    });
    io.subscribe('vertices');
    io.on('vertices', (data) => {
        console.log(data)
        let n_rows = Object.keys(data).length;
        let row = Object.values(data[Object.keys(data)[n_rows - 1]]); // Last row
        let n_cols = Object.keys(row).length;


        polygon.$data['sides'] = n_cols;
        let previous_stats = polygon.$data['stats']
        let stats = updateStats(row, previous_stats);
        polygon.$data['stats'] = stats;
        polygon.$data['points'] = generatePoints(stats, polygon.$data['points']);
    })
    io.subscribe('color');
    io.on('color', (data) => {
        let n_rows = Object.keys(data).length;
        let row = Object.values(data[Object.keys(data)[n_rows - 1]]); // Last row

        let target = document.getElementById('elt-polygon');
        target.style.fill = color_gradient(row[0])
    })

});
