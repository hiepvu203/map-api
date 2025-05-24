from flask import Flask, render_template_string, request
import folium
from geopy.geocoders import Nominatim

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Bản đồ địa điểm</title>
    <meta charset="utf-8">
</head>
<body>
    <h2>Nhập tên địa điểm để xem bản đồ</h2>
    <form method="post">
        <input type="text" name="location_name" placeholder="Nhập địa điểm" required>
        <button type="submit">Tìm kiếm</button>
    </form>
    {% if map_html %}
        <h3>Kết quả cho: {{ location_name }}</h3>
        {{ map_html|safe }}
    {% elif error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    map_html = None
    error = None
    location_name = ""
    if request.method == "POST":
        location_name = request.form["location_name"]
        geolocator = Nominatim(user_agent="geoapi")
        location = geolocator.geocode(location_name)
        if location:
            latitude = location.latitude
            longitude = location.longitude
            m = folium.Map(location=[latitude, longitude], zoom_start=12)
            folium.Marker([latitude, longitude], popup=location_name).add_to(m)
            map_html = m._repr_html_()
        else:
            error = f"Không tìm thấy địa điểm '{location_name}'."
    return render_template_string(HTML_TEMPLATE, map_html=map_html, error=error, location_name=location_name)

if __name__ == "__main__":
    app.run(debug=True)