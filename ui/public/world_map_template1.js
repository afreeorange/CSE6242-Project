var promises = [
  d3.json("countries-50m.json"),
  d3.json("http://localhost:8000/wsi")
]

Promise.all(promises).then(ready)

function ready([world, dataset]) {

  // Create the bar chart
  const map = new WorldMap(
    '#map',
    {
      margin: {
        top: 50,
        bottom: 70,
        left: 10,
        right: 10,
      },
      dataSet: dataset.data,
      topo: world
    }
  )
}
