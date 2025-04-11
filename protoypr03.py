import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.animation import FuncAnimation

def free_fall_simulation():
    # Parameters
    num_particles = 50
    tube_width = 50.0
    tube_height = 25.0
    particle_radius = 0.9
    gravity = 981.0
    start_time = 2.0
    simulation_time = 200.0
    dt = 0.05
    restitution = 0.8
    drag_coefficient = 0.5
    air_density = 0.0012
    mass_aga = 500.0
    frontal_area = 50.0
    
    # Initialize particle positions and velocities
    particles_x = np.random.uniform(particle_radius, tube_width - particle_radius, num_particles)
    particles_y = np.random.uniform(particle_radius + 1, tube_height / 4, num_particles)
    particles_vx = np.random.uniform(-5, 5, num_particles)
    particles_vy = np.random.uniform(-5, 5, num_particles)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_xlim(0, tube_width)
    ax.set_ylim(0, tube_height)
    ax.set_aspect('equal')

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

    # Simulation variables
    current_time = 0.0
    is_free_fall = False
    velocity_chamber = 0.0

    def update(frame):
        nonlocal current_time, is_free_fall, velocity_chamber

        # Check if free fall starts
        if current_time >= start_time and not is_free_fall:
            is_free_fall = True
            print(f"Free fall started at t = {current_time:.2f} seconds")

        # Compute effective gravity
        if is_free_fall:
            drag_force = 0.5 * air_density * drag_coefficient * frontal_area * velocity_chamber**2
            a_chamber = gravity - drag_force / mass_aga
            g_eff = drag_force / mass_aga
            velocity_chamber += a_chamber * dt
        else:
            g_eff = gravity
            velocity_chamber = 0.0

        # Update status text
        status_message = (
            f"Time: {current_time:.2f} s\n"
            f"Effective Gravity (g_eff): {g_eff:.2f} cm/s²\n"
            f"Free Fall: {'Active' if is_free_fall else 'Waiting'}"
        )
        status_text.set_text(status_message)

        # Update particle velocities (positive vy is downward)
        particles_vy[:] += g_eff * dt

        # Update positions
        particles_x[:] += particles_vx[:] * dt
        particles_y[:] -= particles_vy[:] * dt

        # Handle collisions with walls
        left_collision = particles_x < particle_radius
        right_collision = particles_x > tube_width - particle_radius
        particles_vx[left_collision] *= -restitution
        particles_x[left_collision] = particle_radius
        particles_vx[right_collision] *= -restitution
        particles_x[right_collision] = tube_width - particle_radius

        # Handle collisions with bottom
        bottom_collision = particles_y < particle_radius
        particles_vy[bottom_collision] *= -restitution
        particles_y[bottom_collision] = particle_radius

        # Update particle positions in animation
        for i in range(num_particles):
            particle_circles[i].center = (particles_x[i], particles_y[i])

        # Increment time
        current_time += dt

        # Stop if simulation time exceeded
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