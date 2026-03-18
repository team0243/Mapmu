import folium
from folium.plugins import MarkerCluster, Search, LocateControl

# -------------------------------
# 1️⃣ สร้าง Map
# -------------------------------
m = folium.Map(
    location=[16.442786, 102.826613],
    zoom_start=13,
    tiles='CartoDB positron'
)

# -------------------------------
# 2️⃣ CSS Popup (🔥 Mobile Friendly)
# -------------------------------
custom_css = """
<style>
.leaflet-popup-content-wrapper {
    border-radius: 14px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}

/* ✅ ขยาย font มือถือ */
.leaflet-popup-content {
    font-size: 16px;
}

/* ✅ ปุ่มกดง่ายขึ้น */
.leaflet-popup-content a {
    padding: 8px 10px;
    display: inline-block;
}

/* ✅ Popup ไม่ล้นจอ */
.leaflet-popup-content-wrapper {
    max-width: 280px;
}
</style>
"""
m.get_root().html.add_child(folium.Element(custom_css))

# -------------------------------
# 3️⃣ ICON
# -------------------------------
icon_dict = {
    "โชคลาภ": "https://raw.githubusercontent.com/team0243/map_test/refs/heads/main/pin.png",
    "ความรัก": "https://raw.githubusercontent.com/team0243/map_test/refs/heads/main/pin.png",
    "การงาน": "https://raw.githubusercontent.com/team0243/map_test/refs/heads/main/pin.png",
    "บุญบารมี": "https://raw.githubusercontent.com/team0243/map_test/refs/heads/main/pin.png",
    "พญานาค": "https://raw.githubusercontent.com/team0243/map_test/refs/heads/main/pin.png"
}

def get_icon(luck_type):
    return icon_dict.get(luck_type, icon_dict["บุญบารมี"])

# -------------------------------
# 4️⃣ Layer Filter
# -------------------------------
layers = {
    "โชคลาภ 💰": MarkerCluster(name="โชคลาภ 💰").add_to(m),
    "ความรัก ❤️": MarkerCluster(name="ความรัก ❤️").add_to(m),
    "การงาน 💼": MarkerCluster(name="การงาน 💼").add_to(m),
    "บุญบารมี 🙏": MarkerCluster(name="บุญบารมี 🙏").add_to(m),
    "พญานาค 🐉": MarkerCluster(name="พญานาค 🐉").add_to(m),
}

# -------------------------------
# 5️⃣ Loop Marker
# -------------------------------
for index, row in df.iterrows():

    icon_url = get_icon(row['luck_type'])

    if row['province'] == "ขอนแก่น":
        icon_size = (50, 50)
        icon_anchor = (25, 50)
    else:
        icon_size = (35, 35)
        icon_anchor = (17, 35)

    popup_html = f"""
    <div style="width:260px;font-family:Prompt,Arial">
        <img src="{row['image']}"
             style="width:100%;height:150px;object-fit:cover;border-radius:10px">

        <div style="margin-top:6px;color:#777;font-size:13px">{row['province']}</div>
        <div style="font-size:18px;font-weight:bold;color:#222">{row['name']}</div>

        <div style="margin:6px 0">
            <span style="background:#ffe9b3;padding:3px 8px;border-radius:6px;font-size:12px;color:#9c6b00">
                เด่นเรื่อง {row['luck_type']}
            </span>
            <span style="background:#e8f2ff;padding:3px 8px;border-radius:6px;font-size:12px;color:#0057b8">
                {row['type']}
            </span>
        </div>

        <div style="font-size:14px;color:#444">{row['description']}</div>

        <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">

            <a href="{row['web_project_path']}" target="_blank"
               style="text-decoration:none;background:#ff6a00;color:white;
               padding:8px 12px;border-radius:6px;font-size:14px">
               ดูเพิ่มเติม
            </a>

            <a href="https://www.google.com/maps?q={row['lat']},{row['lng']}"
               target="_blank"
               style="text-decoration:none;background:#1d4ed8;color:white;
               padding:8px 12px;border-radius:6px;font-size:14px">
               📍 นำทาง
            </a>

        </div>
    </div>
    """

    marker = folium.Marker(
        location=[row['lat'], row['lng']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=row['name'],
        icon=folium.features.CustomIcon(
            icon_url,
            icon_size=icon_size,
            icon_anchor=icon_anchor
        )
    )

    # Layer mapping
    if row['luck_type'] == "โชคลาภ":
        marker.add_to(layers["โชคลาภ 💰"])
    elif row['luck_type'] == "ความรัก":
        marker.add_to(layers["ความรัก ❤️"])
    elif row['luck_type'] == "การงาน":
        marker.add_to(layers["การงาน 💼"])
    elif row['luck_type'] == "บุญบารมี":
        marker.add_to(layers["บุญบารมี 🙏"])
    elif row['luck_type'] == "พญานาค":
        marker.add_to(layers["พญานาค 🐉"])
    else:
        marker.add_to(layers["บุญบารมี 🙏"])

# -------------------------------
# 6️⃣ Search
# -------------------------------
features = []

for index, row in df.iterrows():
    features.append({
        "type": "Feature",
        "properties": {"name": str(row["name"])},
        "geometry": {
            "type": "Point",
            "coordinates": [row["lng"], row["lat"]],
        },
    })

geojson = folium.GeoJson(
    {"type": "FeatureCollection", "features": features},
    name="SearchLayer",
    marker=folium.CircleMarker(radius=0, opacity=0, fill_opacity=0)
).add_to(m)

Search(
    layer=geojson,
    search_label='name',
    placeholder='🔍 ค้นหาวัด...',
    collapsed=False,
    position='topleft'
).add_to(m)

# -------------------------------
# 7️⃣ GPS
# -------------------------------
LocateControl(position='topleft').add_to(m)

# -------------------------------
# 8️⃣ Layer Control
# -------------------------------
folium.LayerControl(position='topright', collapsed=False).add_to(m)

# -------------------------------
# 9️⃣ Legend
# -------------------------------
legend_html = """
<div style="
position: fixed;
bottom: 20px; left: 10px;
width: 140px;
background: white;
padding: 8px;
border-radius: 10px;
box-shadow: 0 0 10px rgba(0,0,0,0.2);
font-size:12px;
z-index:9999;
">
<b>สายมู</b><br><br>
💰 โชคลาภ<br>
❤️ ความรัก<br>
💼 การงาน<br>
🙏 บุญบารมี<br>
🐉 พญานาค
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))
