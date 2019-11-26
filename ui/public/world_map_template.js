// Initialize the backend URL
const BASE_URL = 'http://localhost:8000';

// Initialize the global variables to hold the year,
// data, GDP rate, and Population rate
var year = 2015,
    years = [],
    data = null;
    deltaGdp = 0,
    deltaPop = 0,
    heading = null,
    map = null,
    predict = null;

var promises = [
  d3.json("countries-110m.json"),
  d3.json(`${BASE_URL}/wsi`)
];

Promise.all(promises).then(ready);

function ready([world, response]) {

  // Set the global data variable
  data = response.data;
  // Get the years from the data
  years = Object.keys(data).map(Number);
  // Set the default year
  if(years.includes(year) == false)
    year = years[0];

  document.querySelector('#gdp').value = deltaGdp;
  document.querySelector('#pop').value = deltaPop;

  // Create the World Map
  map = new WorldMap(
    '#map',
    {
      margin: {
        top: 100,
        bottom: 0,
        left: 0,
        right: 0,
      },
      data: data[year],
      topo: world
    }
  )

  // Create the Timeline
  timeline = new Timeline(
    "#titlebar",
    {
      margin: {
        top: 0,
        bottom: 30,
        left: 0,
        right: 0,
      },
      years: years,
      year: year
    }
  )

  // Listen to the form for changes
  const gdpEvent = document.querySelector('#gdp').addEventListener('click', async event => {
    event.preventDefault();
    // Set the gdp and pop values
    deltaGdp = document.querySelector('#gdp').value;
    deltaPop = document.querySelector('#pop').value;
    getPredictValues();
  });
  const popEvent = document.querySelector('#pop').addEventListener('click', async event => {
    event.preventDefault();
    // Set the gdp and pop values
    deltaGdp = document.querySelector('#gdp').value;
    deltaPop = document.querySelector('#pop').value;
    getPredictValues();
  });
}

/* Update the WSI World Map
*/
function updateData(yr) {

  // Update the year
  year = yr;

  // Update the year data of the Timeline
  timeline.year = yr;

  // Update the year data of the Map
  map.year = yr;

  // Show the default data if the user has not moved the sliders
  if(yr < 2020 || (deltaGdp == 0 && deltaPop == 0))
    map.data = data[yr];
  // Otherwise show the predicted data
  else
    map.data = predict[yr];

  // Show or hide the sliders
  if(yr > 2015)
    $('#editor').addClass('open');
  else {
    $('#editor').removeClass('open');
  }

  // Redraw the Map the the Timeline
  map.draw();
  timeline.draw();
}

/* Call the backend to get the predicted values
*/
function getPredictValues(){

  axios.get(`${BASE_URL}/predict`, {
    params: {
      year: this.year,
      gdp_delta: deltaGdp,
      population_delta: deltaPop
    }
  })
  // Set the predicted values from the response and update the map
  .then(function (response) {
    this.predict = response.data.data;
    this.updateData(this.year);
  })
  .catch(function (error) {
      console.log(error);
  });
}
