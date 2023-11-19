class Status:
    GOOD = 'good'
    DOWN = 'down'
    UNKNOWN = 'unknown-device'
    BROKEN = 'broken'
    MISCONFIGURED = 'misconfigured'

STATUSES = \
    [Status.GOOD] * 20 + \
    [Status.DOWN] * 2 + \
    [Status.UNKNOWN] * 5 + \
    [Status.BROKEN, Status.MISCONFIGURED]

COLORS = {
    Status.GOOD: '#72fa93',
    Status.DOWN: '#e45f2b',
    Status.UNKNOWN: '#f6c445',
    Status.BROKEN: '#e39af0',
    Status.MISCONFIGURED: '#9ac1f0',
}
