var map, heatmap;

      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 12,
          center: {lat: 27.7172, lng: 85.3240},
          mapTypeId: 'roadmap'
        });

        heatmap = new google.maps.visualization.HeatmapLayer({
          data: getPoints(),
          map: map
        });
      }


      // Heatmap data: 500 Points
       function getPoints() {
            return [
            {% for lat in latitude %}
            new google.maps.LatLng{{lat}},
            {% endfor %}
            ];

      }