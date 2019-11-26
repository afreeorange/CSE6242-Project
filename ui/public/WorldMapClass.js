/* Creates a Choropleth World Map of the Water Stress Index.
   Parameters:
        elem: Corresponding html element id or class where the chart
                  will appear
        parameters: Chart parameters.
                margins: { top, bottom, left, right }: margins of the chart
                dataSet: the data to be displayed in the world map - required
                topo: the topographic map to use - required
*/
class WorldMap extends Graphic {
  /* Constructor of the WSI World Map
  */
  constructor(elemName, params={}) {

    // Set the Graphic class parameters
    super(elemName, params);

    // Get the full data set
    this.data = params.data || 'none';

    // Get the TopoJson Map
    this.topo = params.topo || 'none';

    // Set the error flag if any required parameters are missing
    if ( this.data == 'none' || this.topo == 'none' )
        this.missingParams = true;
    else
        this.missingParams = false;

    // Default the selected year to 2015
    this.year = 2015

    // Create the zoomable and draggable map element
    var map = this.chart.append('g')
        .classed('map', true)
        .call(d3.zoom().on("zoom", function () {
            map.attr("transform", d3.event.transform)
        }))
        .append('g');

    // Enable the map element to be called from other functions
    this.map = map;

    // Set the domain and range
    this.domain = [0.1, 2, 200];
    this.range = ['#2c7bb6', '#ffffbf', '#ca0020'];

    // Initialize the Map
    this.init();

  }


  /* Set the map projection
  */
  setMapProjection() {
    //var projection = d3.geoEquirectangular().scale((this.width/640)*100).translate([this.width/2, this.width/4]);
    var projection = d3.geoCylindricalStereographic().scale((this.width/640)*100).translate([this.width/2, this.width/4]);
    this.mapPath = d3.geoPath().projection(projection);
  }

  /* Clear all paths before redrawing
  */
  clear() {
    this.chart.selectAll("path").remove();
    this.chart.selectAll(".legend").remove();
    this.chart.selectAll(".zoomable-bg").remove();
    d3.selectAll(".tooltip").remove();
  }

  /* Draw clear background rectangle so that oceans are zoomable
  */
  drawZoomable() {
    this.map
      .append("rect")
        .attr("class", "zoomable-bg")
        .attr("width", this.svgWidth)
        .attr("height", this.svgHeight * 1.5)
        .style("opacity", 0)
  }

  /* Draws country borders
  */
  drawCountryBorders() {
    // Draw country borders
    this.map
      .append("path")
        .attr("class", "country-borders")
        .datum(topojson.mesh(this.topo, this.topo.objects.countries, function(a, b) { return a !== b; }))
        .attr("d", this.mapPath);
    // Draw land borders
    this.map
      .append("path")
        .attr("class", "country-borders")
        .datum(topojson.mesh(this.topo, this.topo.objects.land))
        .attr("d", this.mapPath);
  }

  /* Draws country borders
  */
  fillCountryValues() {

    // Create the d3 color scale
    var color = d3.scaleLinear()
    .domain(this.domain)
    .range(this.range);

    // Create the map from the wsi value to the scale
    var wsi = d3.map(this.data);

    // Create the tooltip to show the country and WSI value
    var tip = d3.select(this.elemName)
      .append("div")
      .style("opacity", 0)
      .attr("class", "tooltip")
    // Show the tooltip when the mouse is over the country
    var mouseover = function(d) {
      let wsiVal = wsi.get(d.properties.name);
      if( wsiVal == undefined )
        wsiVal = "Data Unavailable";
      tip
        .html("<center><b>" + d.properties.name + "<br>WSI:</b> " +
          wsiVal + "</center>")
        .style("opacity", 1)
    }
    // Adjust the tooltip location as the mouse moves
    var mousemove = function(d) {
      tip
        .style("left", (d3.event.pageX+20) + "px")
        .style("top", (d3.event.pageY) + "px")
    }
    // Hide the tooltip when the mouse leaves the country
    var mouseout = function(d) {
      tip
        .style("opacity", 0)
    }

    // Fill in the countries with the scaled WSI color
    this.map.append("g")
      .attr("class", "countries")
      .selectAll("path")
      .data(topojson.feature(this.topo, this.topo.objects.countries).features)
      .enter()
        .append("path")
          .attr("fill", function(d) {
            var col = color(wsi.get(d.properties.name));
            if(col == d3.rgb(0,0,0))
              col = "#AAA";
            return col;
          })
          .attr("d", this.mapPath)
          .on("mouseover", mouseover)
          .on("mousemove", mousemove)
          .on("mouseout", mouseout);

  }

  /* Draw the legend
  */
  drawLegend(){

    // Create the d3 color scale
    var color = d3.scaleLinear()
    .domain(this.domain)
    .range(this.range);

    // Create the values to add to the legend
    var scale = [0.1, 0.5, 1, 2, 10, 50, 100, 200, 300]

    // Initialize the legend group
    this.newGroup('legend');

    // Set the location
    this.legend
      .attr('transform',
            `translate(${this.width - 100}, 20)`);

    // Draw the background
    this.legend
      .append("rect")
        .attr("class", "legend-bg")
        .attr("width", 80)
        .attr("height", 220)

   // Draw the title
   this.legend
     .append("text")
       .attr("class", "legend-title")
       .attr("x", 40)
       .attr("y", 20)
       .text("WSI")

    // Draw the scale blocks
    this.legend
    .selectAll(".legend-block")
    .data(scale)
    .enter()
      .append("rect")
        .attr("class", "legend-block")
        .attr("x", 10)
        .attr("y", function(d,i) { return i*20 + 30; })
        .attr("width", function(d) { return 15; })
        .attr("height", 15)
        .attr("fill", function(d) { return color(d); });

    // Draw the labels
    this.legend
      .selectAll(".legend-label")
      .data(scale)
      .enter()
        .append("text")
          .attr("class", "legend-label")
          .attr("x", 30)
          .attr("y", function(d,i) { return i*20+43; })
          .text(function(d) {return d;});
  }



  /* Draw the complete chart
  */
  draw() {

      // Draw the error message
      if (this.missingParams)
          this.showErrors();
      // Draw the WSI World Map
      else {
          this.setMapProjection();
          this.clear();
          this.drawZoomable();
          this.fillCountryValues();
          this.drawCountryBorders();
          this.drawLegend();
      }
  }
}
