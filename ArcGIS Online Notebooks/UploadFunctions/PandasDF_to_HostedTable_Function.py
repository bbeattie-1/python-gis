def dfToHostedTable(df, title):
    cleaned_title = title.replace(" ", "_")
    df_csv = df.to_csv(f'{cleaned_title}.csv')
    display(Markdown("### 🛠️ DFToHostedTable Function Running: *(Created By Ben Beattie)*"))

    with tqdm(total=100, desc="Starting DFToHostedTable", bar_format='{desc}{bar}') as pbar:
        try:
            csv_AGOL_item = gis.content.add(item_properties={'title': cleaned_title, 'type': 'CSV'}, data=f'/arcgis/{cleaned_title}.csv')
            pbar.set_description("Uploading CSV To AGOL")
            pbar.update(50) 
            sleep(1)

            table_AGOL_item = csv_AGOL_item.publish()
            pbar.set_description("Publishing CSV As Hosted Table Service")
            pbar.update(100)
            sleep(0.5)

            display(Markdown(f"✅***{cleaned_title}** has been published with item ID: {table_AGOL_item.id}*"))

        except Exception as e:
            pbar.set_description("Table Already Exists")
            sleep(0.5)
            pbar.update(33.33)
            pbar.set_description("Seaching For Table")
            search_results = gis.content.search(f'title: "{cleaned_title}" type: "Feature Service"')

            if search_results:
                sleep(0.5)
                pbar.update(66.66)
                pbar.set_description("Table Found")
                sleep(0.5)
                pbar.set_description("Overwriting Table")
                table_AGOL_item = search_results[0]
                flc = FeatureLayerCollection.fromitem(table_AGOL_item)
                flc.manager.overwrite(f'{cleaned_title}.csv')

                display(Markdown(f"✅ ***{table_AGOL_item.title}** has been updated...*"))
                pbar.update(100)
            else:
                print("Could not find or create existing table.")
            pbar.close()