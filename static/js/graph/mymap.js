//choropleth
var width = 900, height = 500;

var divNode = d3.select('#map').node();

var projection = d3.geo.mercator()
								.scale(5300)
								.translate([width / 2, height / 2])
								.center([83.985593872070313, 28.465876770019531]);

var path = d3.geo.path().projection(projection);

var svg = d3.select("#map").append("svg").attr("width", width).attr("height", height);

d3.json("https://raw.githubusercontent.com/aayushrijal/Nepal-district-topojson/master/nepal-districts.topojson", function(error, ok) {
	var counties = topojson.feature(ok, ok.objects.districts);

    var data = [{'district':'Kathmandu','value':'32'},
                    {'district':'Kavre','value':'14'}];

//    var bardata = [['Kathmandu',32], ['Kavre',13]];
//    console.log(bardata)
//    d3.csv.parse(bardata, function(data) {

//    d3.csv("https://raw.githubusercontent.com/aayushrijal/Nepal-district-topojson/master/district.csv",function(data){
        console.log(data)
        var valueById = {};
        data.forEach(function(d){
            valueById[d.district] = d.value;
            console.log(d.district)
            console.log(d.value)
//        });
	//counties
    	svg.append("g")
            .attr("class", "county")
            .selectAll("path")
            .data(counties.features)
            .enter()
            .append("path")
            .attr("d", path)
            .style("fill", function(d) {
                if(valueById[d.properties.DISTRICT]){
                    return "#000";
                    // return color(valueById[d.properties.DISTRICT]);
                }
    		return "#ccc";
    	});

        var radius = d3.scale.sqrt()
            .domain([0, 1e6])
            .range([0, 20]);

        svg.selectAll("circle")
            .data(counties.features)
            .enter()
            .append("svg:circle")
            .attr("transform", function(d) { return "translate(" + path.centroid(d) + ")"; })
            .attr("r", function(d) {
                if (valueById[d.properties.DISTRICT]) {
                    // return valueById[d.properties.DISTRICT];
                    return radius(valueById[d.properties.DISTRICT])*150;
                }
             })
             .attr("fill","#FC8D59")
             .attr("opacity","0.6")
			 .on("mousemove", function(d){
                       var absoluteMousePos = d3.mouse(divNode);
                       d3.select("#tooltip")
                           .style("left", absoluteMousePos[0]+ 10 + "px")
                           .style("top", absoluteMousePos[1]+ 15 + "px")
                           .select("#value")
                           .attr("class","font")
                           .html(function(){
							   return "<strong>"+ d.properties.DISTRICT +"</strong> " + "<br>" +"Organization Count: <strong>" + valueById[d.properties.DISTRICT] + "</strong> ";
						   });

                       d3.select("#tooltip").classed("hidden", false);
                   })
                   .on("mouseout",function(){
                       d3.select("#tooltip").classed("hidden", true);
                   });

    	//county borders
    	svg.append("path").datum(topojson.mesh(ok, ok.objects.districts, function(a, b) {
    		return a !== b;
    	})).attr("class", "county-border").attr("d", path);
    });
});
