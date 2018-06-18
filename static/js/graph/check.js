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
                    {'district':'Kavre','value':'14'},
                    {'district':'Jhapa','value':'14'}];

////    d3.csv("https://raw.githubusercontent.com/aayushrijal/Nepal-district-topojson/master/district.csv",function(data){
//        console.log(data)
        var valueById = {};
        var districtById = {};

        data.forEach(function(d){
            valueById[d.district] = d.value;
            districtById[d.district] = d.district;
    	svg.append("g")
            .attr("class", "country")
            .selectAll("path")
            .data(counties.features)
            .enter()
            .append("path")
            .attr("d", path)

            .on("mouseover", function(d) {
                 d3.select(this.parentNode).append("text")


              .attr("x", "1000") // margin
              .attr("y", "200") // vertical-align
              .attr("class", "mylabel")//adding a label class
              .text(function() {
                return (valueById[d.properties.DISTRICT]);

              });
//                console.log(valueById[d.properties.DISTRICT])
//                console.log(districtById[d.properties.DISTRICT])
	        })
	        .on("mouseout",function() {
            d3.selectAll(".mylabel").remove()
          })

            .style("fill", function(d) {
                if(valueById[d.properties.DISTRICT]){
                    return "#000";
                    // return color(valueById[d.properties.DISTRICT]);
                }
    		return "#ccc";

    	});
//       function mouseover(d) {
//       console.log(valueById[d.properties.DISTRICT])
//            d3.select(this.parentNode).append("text")
//              .attr("transform", function() {
//                return "rotate(" + computeTextRotation(d) + ")";
//              })
//              .attr("x", function() {
//                return y(d.y);
//              })
//              .attr("dx", "6") // margin
//              .attr("dy", ".35em") // vertical-align
//              .attr("class", "mylabel")//adding a label class
//              .text(function() {
//                return d.name;
//              });
//          }
//          function mouseOut() {
//            d3.selectAll(".mylabel").remove()
//          }



    	//county borders
    	svg.append("path").datum(topojson.mesh(ok, ok.objects.districts, function(a, b) {
    		return a !== b;
    	})).attr("class", "county-border").attr("d", path);
    });
});
