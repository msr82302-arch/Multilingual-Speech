from rest_framework.throttling import UserRateThrottle


class ProcessRateThrottle(UserRateThrottle):
    scope = "process"