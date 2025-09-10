import base64

import cv2

from distributed_event_factory.provider.activity.activity_provider import ActivityProvider

class ImageActivityProvider(ActivityProvider):
    def __init__(self, activity):
        self.dependencies = dict()
        self.activity = activity

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def get_activity(self):
        img = cv2.imread(f"/home/hre/Repo/scalablemine/EventFactoryConfigs/Images/images/{self.activity}.jpg")
        _, buffer = cv2.imencode('.jpg', img)
        return base64.b64encode(buffer)