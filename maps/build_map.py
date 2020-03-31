import folium

lat, lon = 48.8632543, 2.3488009
MapBox_API_key='pk.eyJ1IjoiZGFuY291IiwiYSI6ImNqdTJnM2c3djA1Z2U0M2p0NjFrcWFoaHcifQ.iJs_v4La7rOEbJS0NAnOdA'

# Stamen Terrain, Stamen Toner, Mapbox Bright, and Mapbox Control Room

waypoints = [   (48.863714, 2.348976),
                (48.864139, 2.348002),
                (48.865508, 2.342985)
            ]   


m = folium.Map(location=[lat, lon], 
                zoom_start=14,
                max_zoom=20,
                tiles='Stamen Toner',
                )

folium.Marker(
    location=waypoints[0],
    popup='Métro Etienne Marcel',
    icon=folium.Icon()
).add_to(m)

folium.Marker(
    location=[48.864139, 2.348002],
    popup='Tour Jean Sans Peur',
    icon=folium.Icon()
).add_to(m)

folium.Marker(
    location=[48.865508, 2.342985],
    popup='immeuble donnant sur trois rues',
    icon=folium.Icon()
).add_to(m)


# print(m)
# print(dir(m))
m.save('sentier.html')