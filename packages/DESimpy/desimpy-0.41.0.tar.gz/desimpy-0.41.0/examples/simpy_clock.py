from desimpy.des import EventScheduler, Event

def timeout(e, t, a):
    e.schedule(Event(e.current_time + t, action=a))

def clock(env, name, tick) -> None:
    """Clock simulation process."""

    def action() -> None:
        """Schedule next tick of the clock."""
        print(name, env.current_time)
        timeout(env, tick, action)
        # env.schedule(Event(env.current_time + tick, action))

    env.schedule(Event(env.current_time, action))


# Setting up the simulation environment
env = EventScheduler()

# Scheduling the 'fast' and 'slow' clocks
clock(env, "fast", 0.5)
clock(env, "slow", 1)

# Running the simulation until time 2
env.run_until_max_time(2)
