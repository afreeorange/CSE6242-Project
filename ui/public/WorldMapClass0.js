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


  /* Clear all paths
  */
  clearPaths() {
    this.chart.selectAll("path").remove();
    this.svg.selectAll("rect").remove();
    this.svg.selectAll("timelabels").remove();
  }

  /* Draws ocean for zooming
  */
  drawOcean() {
    this.map.append("rect")
      .attr('transform',
            `translate(${-this.margin.left}, ${-this.margin.top / 4})`)
      .attr("width", this.svgWidth)
      .attr("height", this.svgHeight)
      .attr("fill", "#FFFFFF")
  }

  /* Draws country borders
  */
  drawCountryBorders() {

    this.map.append("path")
      .datum(topojson.mesh(this.topo, this.topo.objects.countries, function(a, b) { return a !== b; }))
        .attr("class", "country-borders")
        .attr("d", this.mapPath);

    this.map.append("path")
      .datum(topojson.mesh(this.topo, this.topo.objects.land))
        .attr("class", "country-borders")
        .attr("d", this.mapPath);

  }

  /* Draws country borders
  */
  fillCountryValues() {

    var color = d3.scaleLog()
    .domain([0.001, 2, 1000])
    .range(['blue', '#ddd', 'red']);

    var wsi = d3.map(this.data);

    // Create the tooltip
    var tip = d3.tip()
      .attr("class", "d3-tip")
      .offset([20,20])
      .html(function(d) {
        var name = d.properties.name;
        var val = wsi.get(name);
        return "Country: " + name +
               "<br>WSI: " + val;
      });
    this.svg.call(tip);


    // Draw the states and their earthquake rates
    this.map.append("g")
        .attr("class", "countries")
      .selectAll("path")
      .data(topojson.feature(this.topo, this.topo.objects.countries).features)
      .enter()
        .append("path")
        .attr("fill", function(d) {
          var col = color(wsi.get(d.properties.name));
          console.log();
          if(col == d3.rgb(0,0,0))
            col = "#AAA";
          return col;
        })
        .attr("d", this.mapPath)
        .on("mouseover", tip.show)
        .on("mouseout", tip.hide);

  }

  /* Draw the error message if any parameters are missing
  */
  showErrors() {

      // Initialize the error message group
      this.newGroup('errors', 'chart');

      this.errors
          .append('text')
          // Move to the center of the chart
          .attr('transform',
                `translate(${this.width / 2}, ${this.height / 2})`)
          .text('Missing required parameters.')
          .attr('text-anchor', 'middle')
          .style('font', '12px sans-serif');
  }

  /* Draw the complete chart
  */
  draw() {

      // draw the error message
      if (this.missingParams)
          this.showErrors();
      else {
          this.setMapProjection();
          this.clearPaths();
          this.drawOcean();
          this.fillCountryValues();
          this.drawCountryBorders();
      }
  }
}
