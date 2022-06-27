// https://github.com/KyrneDev/OSM-LocationPicker
var latlng=[]
$.getJSON('./Website/speechbase.json', function(data) {
    var kinhdo=data.Kinh
    var vido=data.Vi
    var diachi=data.DiaChi
    for (var i=0;i<Object.keys(kinhdo).length;i++)
    {
        var listKinhVi=[]
        listKinhVi.push(kinhdo[i])
        listKinhVi.push(vido[i])
        latlng.push(listKinhVi)
    }

    var mapObj = null;
    var defaultCoord = [10.829350955398068, 106.67269408108423]; // coord mặc định, 9 giữa HCMC
    var zoomLevel = 13;
    var mapConfig = {
        attributionControl: false, // để ko hiện watermark nữa, nếu bị liên hệ đòi thì open 
        center: defaultCoord, // vị trí map mặc định hiện tại
        zoom: zoomLevel, // level zoom
    };
    window.onload = function() {
        // init map
        mapObj = L.map('sethPhatMap', mapConfig);
        
        // add tile để map có thể hoạt động, xài free từ OSM
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(mapObj);

        var myIcon = L.icon({
            iconUrl: 'outdoor.png',
            // iconSize: [67, 95],
            iconAnchor: [22, 30],
            // popupAnchor: [-3, -76],
        });
        for (var i=0;i<latlng.length;i++)
        {
            if (i==latlng.length-1)
            {
                // var marker = L.marker([latlng[0][0],latlng[0][1]],{icon: myIcon}).addTo(mapObj);
                // marker.bindPopup(i+". "+diachi[i]).openPopup()
                break
            }
            if (i==0)
            {
                var marker = L.marker([latlng[i][0],latlng[i][1]],{icon: myIcon}).addTo(mapObj);
                marker.bindPopup(i+". "+diachi[i]).openPopup()
            }
            else
            {
                var marker = L.marker([latlng[i][0],latlng[i][1]]).addTo(mapObj);
                marker.bindPopup(i+". "+diachi[i]).openPopup()
            }
        }
        var poly= L.polyline(latlng,{color: 'red'}).addTo(mapObj)

        x=L.Control.geocoder().addTo(mapObj);
        console.log(x)
    }	
});