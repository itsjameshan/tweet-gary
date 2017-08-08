queue()
    .defer(d3.json, "/data")
    .await(makeGraphs);

function makeGraphs(error, recordsJson) {
	
	//Clean data
	var records = recordsJson;
	var dateFormat = d3.time.format("%Y-%m-%d %H:%M:%S");
	
	records.forEach(function(d) {
		d["timestamp"] = dateFormat.parse(d["timestamp"]);
		d["timestamp"].setMinutes(0);
		d["timestamp"].setSeconds(0);
		d["longitude"] = +d["longitude"];
		d["latitude"] = +d["latitude"];
	});

	//Create a Crossfilter instance
	var ndx = crossfilter(records);

	//Define Dimensions
	var dateDim = ndx.dimension(function(d) { return d["timestamp"]; });
	var genderDim = ndx.dimension(function(d) { return d["gender"]; });
	var ageSegmentDim = ndx.dimension(function(d) { return d["age_segment"]; });
	var phoneBrandDim = ndx.dimension(function(d) { return d["phone_brand_en"]; });
	var locationdDim = ndx.dimension(function(d) { return d["location"]; });
	var allDim = ndx.dimension(function(d) {return d;});


	//Group Data
	var numRecordsByDate = dateDim.group();
	var genderGroup = genderDim.group();
	var ageSegmentGroup = ageSegmentDim.group();
	var phoneBrandGroup = phoneBrandDim.group();
	var locationGroup = locationdDim.group();
	var all = ndx.groupAll();


	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["timestamp"];
	var maxDate = dateDim.top(1)[0]["timestamp"];


    //Charts
    var numberRecordsND = dc.numberDisplay("#number-records-nd");
	var timeChart = dc.barChart("#time-chart");
	var genderChart = dc.rowChart("#gender-row-chart");
	var ageSegmentChart = dc.rowChart("#age-segment-row-chart");
	var phoneBrandChart = dc.rowChart("#phone-brand-row-chart");
	var locationChart = dc.rowChart("#location-row-chart");



	numberRecordsND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(all);


	timeChart
		.width(650)
		.height(140)
		.margins({top: 10, right: 50, bottom: 20, left: 20})
		.dimension(dateDim)
		.group(numRecordsByDate)
		.transitionDuration(500)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.elasticY(true)
		.colors(['#ff9b54'])
		.yAxis().ticks(4);

	genderChart
        .width(300)
        .height(100)
        .dimension(genderDim)
        .group(genderGroup)
        .ordering(function(d) { return -d.value })
        .colors(['#ff9b54'])
        .elasticX(true)
        .xAxis().ticks(4);

	ageSegmentChart
		.width(300)
		.height(150)
        .dimension(ageSegmentDim)
        .group(ageSegmentGroup)
        .colors(['#ff9b54'])
        .elasticX(true)
        .labelOffsetY(10)
        .xAxis().ticks(4);

	phoneBrandChart
		.width(650)
		.height(310)
        .dimension(phoneBrandDim)
        .group(phoneBrandGroup)
        .ordering(function(d) { return -d.value })
        .colors(['#ff9b54'])
        .elasticX(true)
        .xAxis().ticks(4);

    locationChart
    	.width(200)
		.height(510)
        .dimension(locationdDim)
        .group(locationGroup)
        .ordering(function(d) { return -d.value })
        .colors(['#ff9b54'])
        .elasticX(true)
        .labelOffsetY(10)
        .xAxis().ticks(4);

    var map = L.map('map');

	var drawMap = function(){

	    //map.setView([39.8283, -98.5795], 3);
	    map.setView([40.752500, -74.0010], 4);
		mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
		L.tileLayer(
			'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
				attribution: '&copy; ' + mapLink + ' Contributors',
				maxZoom: 15,
			}).addTo(map);

		//HeatMap
		var geoData = [];
		_.each(allDim.top(Infinity), function (d) {
			geoData.push([d["latitude"], d["longitude"], d["text"],d['timestamp']]);
	      });
	    console.log(geoData);
//		var heat = L.heatLayer(geoData,{
//			radius: 10,
//			blur: 20,
//			maxZoom: 1,
//		}).addTo(map);

       var markers = L.markerClusterGroup();
       for (var i = 0; i < geoData.length; i++) {
            var a = geoData[i];
            var title = a[2];
            var created = a[3];
            var marker = L.marker(new L.LatLng(a[0], a[1]), { title: title });
            marker.bindPopup(title+''+created);
            markers.addLayer(marker);
       }

       map.addLayer(markers);

	};

	//Draw Map
	drawMap();

	//Update the heatmap if any dc chart get filtered
	dcCharts = [timeChart, genderChart, ageSegmentChart, phoneBrandChart, locationChart];

	_.each(dcCharts, function (dcChart) {
		dcChart.on("filtered", function (chart, filter) {
			map.eachLayer(function (layer) {
				map.removeLayer(layer)
			}); 
			drawMap();
		});
	});

	dc.renderAll();

};