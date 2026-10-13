from kloppy import wyscout

dataset = wyscout.load_open_data(match_id="2499841", event_types=["shot"])
print(dataset.to_df("event_id", "event_type", "team", "coordinates_*").head())