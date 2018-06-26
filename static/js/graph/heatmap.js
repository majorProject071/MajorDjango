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
    var data = {{ newdata|safe }};
        console.log(data)
        var valueById = {};
        var districtById = {};
        var countById = {};
        var injuryById = {};
        data.forEach(function(d){
            valueById[d.location] = d.value;
            districtById[d.location] = d.location;
            countById[d.location] = d.count;
            injuryById[d.location] = d.injury;
            console.log(d.value)
            console.log(d.count)
    	svg.append("g")
            .attr("class", "country")
            .selectAll("path")
            .data(counties.features)
            .enter()
            .append("path")
            .attr("d", path)
            .on("mouseover", function(d) {
            if(valueById[d.properties.DISTRICT]){
                 d3.select(this.parentNode).append("text")
              .attr("x", "250") // margin
              .attr("y", "450") // vertical-align
              .attr("class", "mylabel")//adding a label class
              .text(function() {
                var data = "District:"+districtById[d.properties.DISTRICT]+ ".";
                var stats = "Death:"+ "" +valueById[d.properties.DISTRICT]+"\n"+"Injury:"+ "" +injuryById[d.properties.DISTRICT];
                datas = data + stats
                return (datas);
              }
              );
	        }})
	        .on("mouseout",function() {
            d3.selectAll(".mylabel").remove()
          })
            .style("fill", function(d) {
                if(countById[d.properties.DISTRICT]>=5){
                    return "red";
                    // return color(valueById[d.properties.DISTRICT]);
                }
                else if(countById[d.properties.DISTRICT]>2 && countById[d.properties.DISTRICT]<5){
                    return "yellow";
                }
                else if(countById[d.properties.DISTRICT]<=2){
                    return "blue";
                }
    		return "#ccc";
    	});
    	//county borders
    	svg.append("path").datum(topojson.mesh(ok, ok.objects.districts, function(a, b) {
    		return a !== b;
    	})).attr("class", "county-border").attr("d", path);
    });
});