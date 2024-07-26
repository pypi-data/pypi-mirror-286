from functools import wraps
from flask import jsonify, request
from .rate_limiter import RateLimiter
import math

def rate_limited(limit, period, max_wait_time):
    if not isinstance(limit, int) or not isinstance(period, int) or not isinstance(max_wait_time, int):
        raise TypeError("All arguments to rate_limited decorator must be integers.")

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            limiter = RateLimiter.get_instance()
            limiter.limit = limit
            limiter.period = period
            limiter.max_wait_time = max_wait_time

            ip = request.headers.get('X-Real-Ip') or \
                 request.headers.get('X-Forwarded-For') or \
                 request.headers.get('Forwarded', '').split(';')[0].strip().split('=')[1] or \
                 request.remote_addr

            if limiter and limiter.is_rate_limited(ip):
                time_left = limiter.get_remaining_wait_time(ip)
                return jsonify({'error': 'Rate limit exceeded', 'message': f'Please wait {math.ceil(time_left)} seconds before trying again'}), 429

            return view_func(*args, **kwargs)
        return _wrapped_view
    return decorator

class CovidsLimiter:
    def __init__(self, limit=100, period=60, max_wait_time=60):
        self.limit = limit
        self.period = period
        self.max_wait_time = max_wait_time
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        limiter = RateLimiter.get_instance()
        limiter.limit = self.limit
        limiter.period = self.period
        limiter.max_wait_time = self.max_wait_time

        @app.before_request
        def global_rate_limit():
            ip = request.headers.get('X-Real-Ip') or \
                 request.headers.get('X-Forwarded-For') or \
                 request.headers.get('Forwarded', '').split(';')[0].strip().split('=')[1] or \
                 request.remote_addr

            if limiter.is_rate_limited(ip):
                time_left = limiter.get_remaining_wait_time(ip)
                return jsonify({'error': 'Rate limit exceeded', 'message': f'Please wait {math.ceil(time_left)} seconds before trying again'}), 429
