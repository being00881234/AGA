import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.animation import FuncAnimation

def free_fall_simulation():
    # Parameters
    num_particles = 50        # Number of particles
    tube_width = 50.0         # Width of the tube in cm
    tube_height = 25.0        # Height of the tube in cm
    particle_radius = 0.9     # Radius of particles in cm
    gravity = 981.0           # Acceleration due to gravity (cm/s^2)
    start_time = 2.0          # Time to start free fall (seconds)
    simulation_time = 10.0    # Total simulation time (seconds)
    dt = 0.05                 # Time step (seconds)
    restitution = 0.8         # Coefficient of restitution for bouncing
    drag_coefficient = 0.5    # Approximate drag coefficient (dimensionless)
    air_density = 0.0012      # Air density in g/cm³ (approximate near sea level)
    mass_aga = 500.0          # Approximate mass of the AGA in grams
    frontal_area = 50.0       # Approximate cross-sectional area in cm²
    
    # Initialize particle positions
    particles_x = np.random.uniform(particle_radius, tube_width - particle_radius, num_particles)
    particles_y = np.random.uniform(particle_radius + 1, tube_height / 4, num_particles)
    
    # Give them a small initial random motion before free fall
    particles_vx = np.random.uniform(-5, 5, num_particles)  # Small horizontal motion
    particles_vy = np.random.uniform(-5, 5, num_particles)  # Small bouncing motion

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_xlim(0, tube_width)
    ax.set_ylim(0, tube_height)
    ax.set_aspect('equal')
   # ax.set_title('Free Fall Simulation in Cylindrical Tube (Side View)')
   # ax.set_xlabel('Width (cm)')
   # ax.set_ylabel('Height (cm)')

    # Draw the tube
    tube = Rectangle((0, 0), tube_width, tube_height, edgecolor='black', facecolor='none', linewidth=2)
    ax.add_patch(tube)

    # Initialize particles
    particle_circles = [Circle((particles_x[i], particles_y[i]), particle_radius, 
                               facecolor='blue', edgecolor='blue') for i in range(num_particles)]
    
    for circle in particle_circles:
        ax.add_patch(circle)

    # Status text
    status_text = ax.text(tube_width / 2, tube_height - 5, '', ha='center', fontsize=12)

    # Time variable
    current_time = 0.0
    is_free_fall = False
    velocity_chamber = 0.0  # Initial velocity of the chamber

    # Function to calculate effective gravity inside chamber
    def compute_geff(velocity):
        drag_force = 0.5 * air_density * drag_coefficient * frontal_area * velocity**2
        a_chamber = drag_force / mass_aga  # Acceleration due to drag
        g_eff = gravity - a_chamber  # Effective gravity inside the chamber
        return max(g_eff, 0)  # Ensure g_eff doesn't go negative

    # Function to update the animation
    def update(frame):
        nonlocal current_time, is_free_fall, velocity_chamber

        # Check if free fall should start
        if current_time >= start_time and not is_free_fall:
            is_free_fall = True
            print(f"Free fall started at t = {current_time:.2f} seconds")

        # Compute effective gravity
        g_eff = compute_geff(velocity_chamber)

        # Update status text (Combine everything into a single text update)
        status_message = (
            f"Time: {current_time:.2f} s\n"
            #f"Gravity: {gravity} cm/s²\n"
            #f"Coefficient of Restitution: {restitution}\n"
            f"Effective Gravity (g_eff): {g_eff:.2f} cm/s²\n"
            f"Free Fall: {'Active' if is_free_fall else 'Waiting'}"
        )
        status_text.set_text(status_message)

        # Apply gravity if free fall has started
        if is_free_fall:
            velocity_chamber += gravity * dt  # Increase chamber velocity due to gravity
            particles_vy[:] += gravity * dt  

        # Update positions
        particles_x[:] += particles_vx[:] * dt
        particles_y[:] -= particles_vy[:] * dt  

        # Handle collisions with tube walls
        left_collision = particles_x < particle_radius
        right_collision = particles_x > tube_width - particle_radius

        particles_vx[left_collision] *= -restitution
        particles_x[left_collision] = particle_radius

        particles_vx[right_collision] *= -restitution
        particles_x[right_collision] = tube_width - particle_radius

        # Handle collisions with the bottom
        bottom_collision = particles_y < particle_radius
        particles_vy[bottom_collision] *= -restitution
        particles_y[bottom_collision] = particle_radius

        # Update particle positions in the animation
        for i in range(num_particles):
            particle_circles[i].center = (particles_x[i], particles_y[i])

        # Increment time
        current_time += dt

        # Stop animation if simulation time is exceeded
        if current_time > simulation_time:
            anim.event_source.stop()
            print(f"Simulation completed at t = {current_time:.2f} seconds")

        return particle_circles + [status_text]

    # Create animation
    frames = int(simulation_time / dt)
    anim = FuncAnimation(fig, update, frames=frames, interval=20, repeat=False)

    plt.show()

if __name__ == "__main__":
    free_fall_simulation()
