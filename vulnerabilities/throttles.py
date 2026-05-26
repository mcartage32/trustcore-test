from rest_framework.throttling import UserRateThrottle

class SyncRateThrottle(UserRateThrottle):
    scope = "sync"

class FixedRateThrottle(UserRateThrottle):
    scope = "fixed"