from desimpy.des import EventScheduler, Event, stop_at_max_time_factory

def clock(env, name, tick) -> None:
    """Clock simulation process."""

    def action() -> None:
        """Schedule next tick of the clock."""
        print(name, env.current_time)
        env.schedule_timeout(delay=tick, action=action)

    env.schedule_timeout(delay=0, action=action)


# Setting up the simulation environment
env = EventScheduler()

# Scheduling the 'fast' and 'slow' clocks
clock(env, "fast", 0.5)
clock(env, "slow", 1)

# Running the simulation until time 2
print(env.run_until_max_time(2))
