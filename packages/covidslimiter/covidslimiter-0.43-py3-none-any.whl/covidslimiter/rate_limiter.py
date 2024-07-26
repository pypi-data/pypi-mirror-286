from datetime import datetime, timedelta

class RateLimiter:
    _instance = None
    _params = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RateLimiter, cls).__new__(cls)
            cls._params = {'limit': kwargs.get('limit', 100), 'period': kwargs.get('period', 60), 'max_wait_time': kwargs.get('max_wait_time', 5)}
        return cls._instance

    @classmethod
    def get_instance(cls, limit=None, period=None, max_wait_time=None):
        if not cls._instance:
            cls._instance = cls()
            for attr_name, param_value in cls._params.items():
                setattr(cls._instance, attr_name, param_value)

            cls._instance.request_counts = {}
            cls._instance.request_timestamps = {}
            cls._instance.rate_limit_hit_count = {}
            cls._instance.wait_start_times = {}
        return cls._instance

    def is_rate_limited(self, ip):
        now = datetime.utcnow()

        self.request_counts[ip] = self.request_counts.get(ip, 0) + 1
        if not ip in self.wait_start_times:
            self.wait_start_times[ip] = now
        else:
            self.wait_start_times[ip] = self.wait_start_times.get(ip, now)

        self.rate_limit_hit_count[ip] = self.rate_limit_hit_count.get(ip, 0)

        if ip not in self.request_timestamps:
            self.request_timestamps[ip] = []
            self.request_timestamps[ip].append(now)

        self.clear_old_entries(now)

        try:
            if self.request_counts[ip] >= self.limit:
                if ip in self.rate_limit_hit_count:
                    self.rate_limit_hit_count[ip] += 1
                else:
                    self.rate_limit_hit_count[ip] = 1
                if self.has_wait_time_passed(ip):
                    return False
                return True
            else:
                return False
        except KeyError:
            return True

    def clear_old_entries(self, current_time):
        MAX_ENTRY_AGE = timedelta(minutes=2)
        ips_to_clear = set()

        for ip, timestamps in self.request_timestamps.items():
            timestamps.sort(reverse=True)
            new_timestamps = [ts for ts in timestamps if current_time - ts <= MAX_ENTRY_AGE]

            if len(new_timestamps) < len(timestamps):
                self.request_timestamps[ip] = new_timestamps
                if not new_timestamps:
                    ips_to_clear.add(ip)
                else:
                    print(new_timestamps)

        if ips_to_clear:
            for ip in ips_to_clear:
                del self.request_timestamps[ip]
                del self.request_counts[ip]
                del self.rate_limit_hit_count[ip]
                del self.wait_start_times[ip]

    def has_wait_time_passed(self, ip):
        now = datetime.utcnow()

        if ip in self.wait_start_times:
            wait_start = self.wait_start_times[ip]
        else:
            wait_start = now

        if wait_start is None:
            self.wait_start_times[ip] = now
            return True

        wait_duration = now - wait_start
        total_wait_duration = min(self.rate_limit_hit_count[ip], self.max_wait_time)

        if wait_duration.total_seconds() < total_wait_duration:
            return False

        self.wait_start_times[ip] = None
        self.request_counts[ip] = 0
        self.rate_limit_hit_count[ip] = 0
        return True

    def get_remaining_wait_time(self, ip):
        now = datetime.utcnow()
        if ip in self.wait_start_times:
            wait_start = self.wait_start_times[ip]
        else:
            wait_start = now

        if wait_start is None:
            return 0

        if ip in self.rate_limit_hit_count:
            hit_count = self.rate_limit_hit_count[ip]
        else:
            hit_count = self.rate_limit_hit_count.get(ip, 1)
        total_wait_duration = min(hit_count, self.max_wait_time)

        effective_wait_end = wait_start + timedelta(seconds=total_wait_duration)
        remaining_wait = max(0, (effective_wait_end - now).total_seconds())

        return remaining_wait
