//import d3.legend from './d3.legend.js';

var w = 300, h = 400, r = 150
console.log(data)
data = JSON.parse(data)[0]["f_mixed"]
//color = d3.scale.category20c();     //builtin range of colors
//function colores_google(n) {
//  var colores_g =["#b24343","#f9bb52","#89a3c2","#e499bd","#e499bd","#bbc89c","#bbc89d"];
//  return colores_g[n];}

//piepie= JSON.parse(data)[0]["f_mixed"]


//var colorscale = d3.scale.ordinal()
//    .domain(['Residential', 'Office', 'Commercial', 'Residential&Commercial', 'Commercial&Office', 'Residential&Office',"Residential&Commercial&Office"])
//    .range(["#b24343","#f9bb52","#89a3c2","#6c4c87","#3d8677","#e499bd","#bfbfbf"]);//orange "#e499bd", green #3d8677, purple #6c4c87, grey #bfbfbf
////color = ["#9081ca","#89a3c2","#f9bb52"]
// resi, off, comm, res_com, com_off, res_off, 3tyeps
// chart for first ONE!

//
//[{"name": "Residential", "freq": 32833.68709945883, "color": "#b24343"}, {"name": "Office", "freq": 31359.608256387335, "color": "#f9bb52"}, {"name": "Commercial", "freq": 52024.76024980958, "color": "#89a3c2"}, {"name": "Mixed:RC", "freq": 18893.813638854423, "color": "#6c4c87"}, {"name": "Mixed:CO", "freq": 2236.485401068858, "color": "#3d8677"}, {"name": "Mixed:RO", "freq": 1157.8477008918603, "color": "#e499bd"}, {"name": "Mixed:COR", "freq": 14754.024532770425, "color": "#bfbfbf"}]
//var vis = d3.select("#chart-03")
//          .append("svg:svg")
//        .data([data])                   //associate our data with the document
//            .attr("width", w)           //set the width and height of our visualization (these will be attributes of the <svg> tag
//            .attr("height", h)
//        .append("svg:g")                //make a group to hold our pie chart
//            .attr("transform", "translate(" + r + "," + r + ")")    //move the center of the pie chart from 0, 0 to radius, radius
//
//    var arc = d3.svg.arc()              //this will create <path> elements for us using arc data
//        .outerRadius(r);
//
//    var pie = d3.layout.pie()           //this will create arc data for us given a list of values
//        //.value(function(d) { return d.freq; });    //we must tell it out to access the value of each element in our data array
//         .value(function(d) { return d.freq; });
//
//    var arcs = vis.selectAll("g.slice")     //this selects all <g> elements with class slice (there aren't any yet)
//        .data(pie)                          //associate the generated pie data (an array of arcs, each having startAngle, endAngle and value properties)
//        .enter()                            //this will create <g> elements for every "extra" data element that should be associated with a selection. The result is creating a <g> for every object in the data array
//            .append("svg:g")                //create a group to hold each slice (we will have a <path> and a <text> element associated with each slice)
//                .attr("class", "slice");    //allow us to style things in the slices (like text)
//
//        arcs.append("svg:path")
//                .attr("fill", function(d) { return d.data.color; } ) //set the color for each slice to be chosen from the color function defined above
//                .attr("d", arc);                                    //this creates the actual SVG path using the associated data (pie) with the arc drawing function
//
//        arcs.append("svg:text")                                     //add a label to each slice
//                .attr("transform", function(d) {                    //set the label's origin to the center of the arc
//                //we have to make sure to set these before calling arc.centroid
//                d.innerRadius = 0;
//                d.outerRadius = r;
//                return "translate(" + arc.centroid(d) + ")";        //this gives us a pair of coordinates like [50, 50]
//            })
//            .attr("text-anchor", "middle")                          //center the text on it's origin
//            .text(function(d, i) { return data[i].name; });        //get the label from our original data array

// test with legend
var width = 400,
    height = 300,
    radius = Math.min(width, height) / 3;

//var color = d3.scale.ordinal()
//    .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

var arc = d3.svg.arc()
    .outerRadius(radius - 10)
    .innerRadius(0);

var svg = d3.select("#chart-01").append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
     .data([data])
     .attr("transform", "translate(" + radius + "," + radius + ")")
   // .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

var pie = d3.layout.pie()
    .sort(null)
    .value(function(d) { return d.freq; });

var piefreq = data.map(a => a.freq);
console.log(piefreq)

var g = svg.selectAll(".arc")
      .data(pie)
      .enter().append("g")
      .attr("class", "arc");

console.log(pie(data))

  g.append("path")
      .attr("d", arc)
      .attr("data-legend", function(d) { return d.data.name; })
      .attr("data-legend-pos", function(d, i) { return i; })
      .style("fill", function(d) { return d.data.color; });
      // .style("fill", function(d) { return color(d.data.name); });

  g.append("text")
      .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
      .attr("dy", ".35em")
      .style("text-anchor", "middle");

  var padding = 40,
    legx = radius + padding,
    legend = svg.append("g")
    .attr("class", "legend")
    .attr("transform", "translate(" + legx + ", 0)")
    .style("font-size", "12px")
    .call(d3.legend);



//test for graph 02
//var vis = d3.select("#chart-03")
//          .append("svg:svg")
//        .data([data])                   //associate our data with the document
//            .attr("width", w)           //set the width and height of our visualization (these will be attributes of the <svg> tag
//            .attr("height", h)
//        .append("svg:g")                //make a group to hold our pie chart
//            .attr("transform", "translate(" + r + "," + r + ")")    //move the center of the pie chart from 0, 0 to radius, radius
//
//    var arc = d3.svg.arc()              //this will create <path> elements for us using arc data
//        .outerRadius(r);
//
//    var pie = d3.layout.pie()           //this will create arc data for us given a list of values
//        .value(function(d) { return d.freq; });    //we must tell it out to access the value of each element in our data array
//
//    var arcs = vis.selectAll("g.slice")     //this selects all <g> elements with class slice (there aren't any yet)
//        .data(pie)                          //associate the generated pie data (an array of arcs, each having startAngle, endAngle and value properties)
//        .enter()                            //this will create <g> elements for every "extra" data element that should be associated with a selection. The result is creating a <g> for every object in the data array
//            .append("svg:g")                //create a group to hold each slice (we will have a <path> and a <text> element associated with each slice)
//                .attr("class", "slice");    //allow us to style things in the slices (like text)
//
//        arcs.append("svg:path")
//                .attr("fill", function(d, i) { return colores_google(i); } ) //set the color for each slice to be chosen from the color function defined above
//                .attr("d", arc);                                    //this creates the actual SVG path using the associated data (pie) with the arc drawing function
//
//        arcs.append("svg:text")                                     //add a label to each slice
//                .enter()
//                .append("text")
//                .attr("text-anchor", "middle")
//                .attr("x", function(d) {
//                    var a = d.startAngle + (d.endAngle - d.startAngle)/2 - Math.PI/2;
//                    d.cx = Math.cos(a) * (radius - 75);
//                    return d.x = Math.cos(a) * (radius - 20);
//                })
//                .attr("y", function(d) {
//                    var a = d.startAngle + (d.endAngle - d.startAngle)/2 - Math.PI/2;
//                    d.cy = Math.sin(a) * (radius - 75);
//                    return d.y = Math.sin(a) * (radius - 20);
//                })
//                .text(function(d, i) { return data[i].name; })
//                .each(function(d) {
//                    var bbox = this.getBBox();
//                    d.sx = d.x - bbox.width/2 - 2;
//                    d.ox = d.x + bbox.width/2 + 2;
//                    d.sy = d.oy = d.y + 5;
//                });

//
//
//                .attr("transform", function(d) {                    //set the label's origin to the center of the arc
//                //we have to make sure to set these before calling arc.centroid
//                d.innerRadius = 0;
//                d.outerRadius = r;
//                return "translate(" + 0.1*arc.centroid(d) + ")";        //this gives us a pair of coordinates like [50, 50]
//            })
//            .attr("text-anchor", "middle")                          //center the text on it's origin
          //  .text(function(d, i) { return data[i].name; });        //get the label from our original data array

// D3 Another example
//
//var pienames = data.map(a => a.name);
//var piefreqs = data.map(a => a.freq);
//var piecolors = data.map(a => a.color);
//console.log(pienames,piefreqs,piecolors)
//
//var dataset = {
//  names: ["A","B","C","C","D"],
//  freqs: piefreqs,
//  colors:piecolors
//};
//
//var width = 300,
//    height = 300,
//    radius = Math.min(width, height) / 2;
//
//var color = d3.scale.category20();
//
//var pie = d3.layout.pie()
//    .sort(null);
////
//var piename = pie(dataset.names);
//var piefreq = pie(dataset.freqs)
//var piecolor  = pie(dataset.colors)
//alert(piename)
//var arc = d3.svg.arc()
//    .innerRadius(radius - 100)
//    .outerRadius(radius - 50);
//
//var svg = d3.select("#chart-01").append("svg")
//    .attr("width", width)
//    .attr("height", height)
//    .append("g")
//    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
//
//var path = svg.selectAll("path")
//    .data(piefreq)
//  .enter().append("path")
//    .attr("fill", function(d, i) { return color(i); })
//    .attr("d", arc);
//
//svg.selectAll("text").data(piename)
//    .enter()
//    .append("text")
//    .attr("text-anchor", "middle")
//    .attr("x", function(d) {
//        var a = d.startAngle + (d.endAngle - d.startAngle)/2 - Math.PI/2;
//        d.cx = Math.cos(a) * (radius - 75);
//        return d.x = Math.cos(a) * (radius - 20);
//    })
//    .attr("y", function(d) {
//        var a = d.startAngle + (d.endAngle - d.startAngle)/2 - Math.PI/2;
//        d.cy = Math.sin(a) * (radius - 75);
//        return d.y = Math.sin(a) * (radius - 20);
//    })
////    .text(function(d) { return d.value; })
//    .each(function(d) {
//        var bbox = this.getBBox();
//        d.sx = d.x - bbox.width/2 - 2;
//        d.ox = d.x + bbox.width/2 + 2;
//        d.sy = d.oy = d.y + 5;
//    });
//
//svg.append("defs").append("marker")
//    .attr("id", "circ")
//    .attr("markerWidth", 6)
//    .attr("markerHeight", 6)
//    .attr("refX", 3)
//    .attr("refY", 3)
//    .append("circle")
//    .attr("cx", 3)
//    .attr("cy", 3)
//    .attr("r", 3);
//
//svg.selectAll("path.pointer").data(piefreq).enter()
//    .append("path")
//    .attr("class", "pointer")
//    .style("fill", "none")
//    .style("stroke", "black")
//    .attr("marker-end", "url(#circ)")
//    .attr("d", function(d) {
//        if(d.cx > d.ox) {
//            return "M" + d.sx + "," + d.sy + "L" + d.ox + "," + d.oy + " " + d.cx + "," + d.cy;
//        } else {
//            return "M" + d.ox + "," + d.oy + "L" + d.sx + "," + d.sy + " " + d.cx + "," + d.cy;
//        }
//    });