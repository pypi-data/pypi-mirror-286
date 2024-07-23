from desimpy.des import Event, EventScheduler, stop_at_max_time_factory

# Define the car process
def car(env: EventScheduler):
    while True:
        # Print the start parking time
        print(f'Start parking at {env.current_time}')
        
        # Schedule the next event to be after parking_duration
        parking_duration = 5
        next_event_time = env.current_time + parking_duration
        yield Event(next_event_time, lambda ctx: None, {})

        # Print the start driving time
        print(f'Start driving at {env.current_time}')
        
        # Schedule the next event to be after trip_duration
        trip_duration = 2
        next_event_time = env.current_time + trip_duration
        yield Event(next_event_time, lambda ctx: None, {})

# Initialize the event scheduler
scheduler = EventScheduler()

# Schedule the car process to start at time 0
scheduler.schedule(Event(0, lambda ctx: car(scheduler), {}))

# Define the stop condition
stop_condition = stop_at_max_time_factory(scheduler, 15)

# Run the simulation
scheduler.run(stop_condition)

