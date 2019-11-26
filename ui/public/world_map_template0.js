var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var earthquakes = d3.map();

var regions = {};

var projection = d3.geoCylindricalStereographic().scale(120).translate([420, 230]),
//var projection = d3.Eckert3().scale(100).translate([420, 230]),
    path = d3.geoPath().projection(projection);

var promises = [
  d3.json("countries-110m.json")
]

Promise.all(promises).then(ready)

function ready([world]) {

  var g = svg.append("g")
      .attr("class", "key")
      .attr("transform", "translate(680,200)");

  svg.append("path")
    .datum(topojson.mesh(world, world.objects.countries, function(a, b) { return a !== b; }))
      .attr("class", "country-borders")
      .attr("d", path);

  svg.append("path")
    .datum(topojson.mesh(world, world.objects.land))
      .attr("class", "country-borders")
      .attr("d", path);

}
