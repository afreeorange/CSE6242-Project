/* Creates a chart of the size of the corresponding html element.
   Parameters:
        elemName: Corresponding html element id or class where the chart
                  will appear
        params: Chart parameters.  This parent class only uses the margin
                within the params dictionary to set the margins of the chart
                additional parameters can be used within the children classes
    This class was originally copied from:
*/
class Graphic {
  /* Constructor of the Generic Graphic Class
  */
  constructor(elemName, params={}) {

    // Store the name of the element to attach the SVG
    this.elemName = elemName;
    // Create the SVG reference
    this.svg = d3.select(elemName).append('svg');
    // Create the margins
    this.margin = params.margin || {
      top: 0,
      bottom: 0,
      left: 0,
      right: 0,
    }

    // Create the chart element offset by the margins
    this.chart = this.svg.append('g')
      .attr('class', 'chart')
      .attr('transform', `translate(${this.margin.left}, ${this.margin.top})`);
  }

  /* Return the html element of the SVG using jQuery
  */
  get element() {
      return $(this.elemName);
  }

  /* Initializes the SVG
  */
  init() {
      // Draw the SVG
      this.resize();
      // Redraw the SVG when the window is resized using jQuery
      $(window).resize(() => {
          this.resize();
      })
  }

  /* Draws the graphic -- overridden by subclass
  */
  draw() {

  }

  /* Resize the SVG and redraw it as the window size changes
  */
  resize() {
    // Set the SVG width and height to the size of the div
    this.svgWidth = this.element.width();
    this.svgHeight = this.element.height();
    // Set the width and the height of the chart
    this.width = this.svgWidth - this.margin.left - this.margin.right;
    this.height = this.svgHeight - this.margin.top - this.margin.bottom;
    // Update the SVG width and height
    this.svg
      .attr('width', this.svgWidth)
      .attr('height', this.svgHeight);
    // Update the chart width and height
    this.chart
      .attr('width', this.width)
      .attr('height', this.height);

    // Draw the SVG
    this.draw();
  }

  /* Create a new element group
  */
  newGroup(name, parent=undefined) {
    if (parent === undefined) {
      this.chart.selectAll(`.${name}`).remove();
      this[name] = this.chart.append('g').classed(name, true);
    } else {
      parent.selectAll(`.${name}`).remove();
      parent[name] = parent.append('g').classed(name, true);
    }
  }

  /* Draw the error message if any parameters are missing
  */
  showErrors() {

      // Create the error message group
      this.newGroup('errors');

      this.errors
        // Move to the center of the chart
        .attr('transform',
              `translate(${this.width / 2}, ${this.height / 2})`)
        .append('text')
          .text('Missing required parameters.')
          .attr('text-anchor', 'middle')
          .style('font', '12px sans-serif');
  }
}
