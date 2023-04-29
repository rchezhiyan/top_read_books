'use strict';

fetch('/author_books.json')
    .then((response) => response.json())
    .then((responseJson) => {

        const data = responseJson
        console.log(data)

        const margin = {top: 20, right:100, bottom:40, left:200}
        const width = 760 - margin.left - margin.right
        const height = 500 - margin.top -margin.bottom

        const svg = d3.select('#bar-chart')
            .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
            .append("g")
                .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");
        
        const x = d3.scaleLinear()
            .domain([d3.min(data, function (d) {
            return d.bookcount;
            }), d3.max(data, function (d) {
            return d.bookcount;
            })])
            .range([0, width]);

        svg.append("g")
            .attr("transform", "translate(0, "+ height + ")")
            .call(d3.axisBottom(x))
            .selectAll("text")
                .attr("transform", "translate(-10,0)")
                .style("test-anchor","end");
        

        const y = d3.scaleBand()
            .range([0,height])
            .domain(data.map(function(d) { return d.name; }))
            .padding(.1);
        
        svg.append("g")
            .call(d3.axisLeft(y))

        svg 
          .selectAll('rect')
          .data(data)
          .enter()
          .append('rect')
            .attr('x', 0)
            .attr('y', function(d) { return y(d.name)} )
            .attr('width', function(d){return d.bookcount*5})
            .attr('height', y.bandwidth()/2)
            .attr('fill', function(d,idx) { return d3.hsl(idx * 30, 1.0, 0.8)})
    });