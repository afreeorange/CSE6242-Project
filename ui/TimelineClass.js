/* Creates a Choropleth World Map of the Water Stress Index.
   Parameters:
        elem: Corresponding html element id or class where the chart
                  will appear
        parameters: Chart parameters.
                margins: { top, bottom, left, right }: margins of the chart
                dataSet: the data to be displayed in the world map - required
                topo: the topographic map to use - required
*/
class Timeline extends Graphic {
  /* Constructor of the WSI World Map
   */
  constructor(elemName, params = {}) {
    // Set the Graphic class parameters
    super(elemName, params);

    // Get the full data set
    this.years = params.years || "none";

    // Default the selected year to 2015
    this.year = params.year || "none";

    // Set the error flag if any required parameters are missing
    if (this.years == "none" || this.year == "none") this.missingParams = true;
    else this.missingParams = false;

    // Initialize the Timeline
    this.init();
  }

  /* Draw timeline
   */
  drawTimeline() {
    // Create local variables so that they are accessible
    // within the function(d) calls
    var years = this.years,
      yr = this.year,
      width = this.width;

    // Create a new timeline group
    this.newGroup("timeline");

    this.timeline
      // Move to the center of the chart
      .attr("transform", `translate(0, ${this.height - 10})`);

    // Draw the line connecting the years
    this.timeline
      .selectAll("timeline-line")
      .data(years)
      .enter()
      .append("rect")
      .attr("class", function(d) {
        if (d < 2015) return "timeline-line historical";
        else return "timeline-line forecast";
      })
      .attr("x", function(d, i) {
        return (i * width) / years.length + width / (3 * years.length);
      })
      .attr("width", function(d, i) {
        if (i + 1 == years.length) return 0;
        else return width / years.length;
      })
      .attr("height", 3);

    // Draw the circles for each year
    this.timeline
      .selectAll("timeline-years")
      .data(years)
      .enter()
      .append("circle")
      .attr("class", function(d) {
        if (d == yr && d < 2020)
          return "timeline-years historical selected-year";
        else if (d < 2020) return "timeline-years historical";
        else if (d == yr) return "timeline-years forecast selected-year";
        else return "timeline-years forecast";
      })
      .attr("cx", function(d, i) {
        return (i * width) / years.length + width / (3 * years.length);
      })
      .attr("cy", 1)
      .attr("r", function(d) {
        if (d == yr) return 13;
        else return 10;
      })
      // Enlarge the year dot when the mouse is over it
      .on("mouseover", function(d, i) {
        d3.select(this)
          .transition()
          .duration(300)
          .attr("r", 13);
      })
      // Reduce the year dot when the mouse leaves it
      .on("mouseout", function(d, i) {
        var rad = 10;
        if (d == yr) rad = 13;
        d3.select(this)
          .transition()
          .duration(300)
          .attr("r", rad);
      })
      // Update the map data when the year dot is clicked
      .on("click", this.updateMapData);

    // Draw the year labels
    this.timeline
      .selectAll("time-label")
      .data(years)
      .enter()
      .append("text")
      .attr("class", function(d) {
        if (d < 2020) return "time-label historical";
        else return "time-label forecast";
      })
      .attr("x", function(d, i) {
        return (i * width) / years.length + width / (3 * years.length);
      })
      .attr("y", 30)
      .text(function(d) {
        return d;
      });

    // Draw the Historical subtitle
    this.timeline
      .append("text")
      .attr("class", "time-category historical")
      .attr("x", this.width / 6)
      .attr("y", -15)
      .text("Historical");

    // Draw the forecast subtitle
    this.timeline
      .append("text")
      .attr("class", "time-category forecast")
      .attr("x", (5 * this.width) / 6)
      .attr("y", -15)
      .text("Forecast");
  }

  // Set the year and update the data of the map
  updateMapData(d) {
    // Call the global function to update the data
    updateData(d);
  }

  /* Clear the timeline */
  clear() {
    this.chart.selectAll("timeline").remove();
  }

  /* Draw the complete chart
   */
  draw() {
    // draw the error message
    if (this.missingParams) this.showErrors();
    else this.clear();
    this.drawTimeline();
  }
}
