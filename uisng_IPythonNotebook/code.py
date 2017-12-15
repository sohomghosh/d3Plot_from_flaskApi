#Reference: https://www.kaggle.com/arthurtok/ghastly-network-and-d3-js-force-directed-graphs
json_data = {"node" : [{"id": "id_1234", "group": 1},  {"id": "id_5467", "group": 2}] }

stopwords = {
"nodes": [
 {"id": "Edgar Allen Poe", "group": 1},
 {"id": "HP Lovecraft", "group": 2},
 {"id": "Mary Shelley", "group": 3},
 {"id": "and"	, "group": 1},
 {"id": "is"	, "group": 1},
 {"id": "it"	, "group": 1},
 {"id": "an"	, "group": 1},
 {"id": "as"	, "group": 1},
 {"id": "at"	, "group": 1},
 {"id": "have"	, "group": 1},
 {"id": "in"	, "group": 1},
 {"id": "from"	, "group": 1},
 {"id": "for"	, "group": 1},
 {"id": "no"	, "group": 1},
 {"id": "had"	, "group": 1}
],
"links": [
 {"source": "Edgar Allen Poe", "target": "and"	, "value": 1},
 {"source": "Edgar Allen Poe", "target": "is"	, "value": 1},
 {"source": "Edgar Allen Poe", "target": "it"	, "value": 1},
 {"source": "Edgar Allen Poe", "target": "an"	, "value": 1},
 {"source": "Edgar Allen Poe", "target": "as"	, "value": 1},
 {"source": "Edgar Allen Poe", "target": "at"	, "value": 1},
 {"source": "Edgar Allen Poe", "target": "have"	, "value": 1},
 {"source": "Edgar Allen Poe", "target": "in"	, "value": 1},	
 {"source": "Edgar Allen Poe", "target": "from"	, "value": 1},
 {"source": "Edgar Allen Poe", "target": "for"	, "value": 1},
 {"source": "Edgar Allen Poe", "target": "no"	, "value": 1},
 {"source": "Edgar Allen Poe", "target": "had"	, "value": 1},
 {"source": "Edgar Allen Poe", "target": "to"	, "value": 1},
 {"source": "Edgar Allen Poe", "target": "which", "value": 1},
 {"source": "Edgar Allen Poe", "target": "was"	, "value": 1}
 ]
 }
 
with open('stopwords.json', 'w') as outfile:  
    json.dump(stopwords, outfile)
    
html_string = """
<!DOCTYPE html>
<meta charset="utf-8">
<style>

.links line {
  stroke: #999;
  stroke-opacity: 0.6;
}

.nodes circle {
  stroke: #fff;
  stroke-width: 3px;
}

text {
  font-family: sans-serif;
  font-size: 12px;
}

</style>
<svg width="960" height="500"></svg>
"""


js_string="""
 require.config({
    paths: {
        d3: "https://d3js.org/d3.v4.min"
     }
 });

  require(["d3"], function(d3) {

  var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var color = d3.scaleOrdinal(d3.schemeCategory20);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().distance(170).strength(0.5).id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width/2 , height/2 ));

d3.json("stopwords.json", function(error, graph) {
  if (error) throw error;

  var link = svg.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

  var node = svg.append("g")
      .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter().append("g")
    
  var circles = node.append("circle")
      .attr("r", 8)
      .attr("fill", function(d) { return color(d.group); })
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

  var lables = node.append("text")
      .text(function(d) {
        return d.id;
      })
      .attr('x', 6)
      .attr('y', 3);

  node.append("title")
      .text(function(d) { return d.id; });

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(graph.links);

  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";
        })
  }
});

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.9).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}  
    
  });
 """

h = IPython.display.display(HTML(html_string))
j = IPython.display.Javascript(js_string)
IPython.display.display_javascript(j)
