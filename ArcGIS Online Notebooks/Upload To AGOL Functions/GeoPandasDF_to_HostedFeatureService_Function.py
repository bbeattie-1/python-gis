def gdfToFeatureService(gdf, title):
    cleaned_title = title.replace(" ", "_")
    gdf.to_file(f"/arcgis/{cleaned_title}.geojson", driver='GeoJSON', engine='fiona', crs='4326')
    display(Markdown("### 🛠️ GDFToHostedFeatureService Function Running: *(Created By Ben Beattie)*"))

    with tqdm(total=100, desc="Starting GDFToHostedTable", bar_format='{desc}{bar}') as pbar:
        search_results = gis.content.search(f'title: "{cleaned_title}" type: "GeoJson"')
        if search_results == []:
            geojson_AGOL_item = gis.content.add(item_properties={'title': f'{cleaned_title}', 'type': 'GeoJson', 'spatialReference': '4326'}, data=f'/arcgis/{cleaned_title}.geojson')
            pbar.set_description("Uploading GeoJSON To AGOL")
            pbar.update(50) 
            sleep(1)

            fs_AGOL_item = geojson_AGOL_item.publish()
            pbar.set_description("Publishing GeoJSON As Hosted Feature Service")
            pbar.update(100)
            sleep(0.5)

            display(Markdown(f"✅***{cleaned_title}** has been published with item ID: {fs_AGOL_item.id}*"))

        elif len(search_results) > 0:
            pbar.set_description("Feature Service Already Exists")
            sleep(0.5)
            pbar.update(33.33)
            pbar.set_description("Seaching For Feature Service")
            search_results = gis.content.search(f'title: "{cleaned_title}" type: "Feature Service"')
            
            if search_results:
                sleep(0.5)
                pbar.update(66.66)
                pbar.set_description("Feature Service Found")
                sleep(0.5)
                pbar.set_description("Overwriting Feature Service")
                fs_AGOL_item = search_results[0]
                flc = FeatureLayerCollection.fromitem(fs_AGOL_item)
                flc.manager.overwrite(f'/arcgis/{cleaned_title}.geojson')

                display(Markdown(f"✅ ***{fs_AGOL_item.title}** has been updated...*"))
                pbar.update(100)
            else:
                print("Could not find or create existing feature service.")
            pbar.close()