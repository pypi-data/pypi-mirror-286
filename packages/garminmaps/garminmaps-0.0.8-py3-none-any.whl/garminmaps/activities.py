class Activity:
    def __init__(self, payload, garmin_client):
        self.id = payload["activityId"]
        self.type = payload["activityType"]["typeKey"]
        self.distance = payload["distance"]
        self.duration = payload["duration"]
        self.gpx = garmin_client.download_activity(
            self.id, garmin_client.ActivityDownloadFormat.GPX
        )
