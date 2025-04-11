import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.animation import FuncAnimation

def free_fall_simulation():
    # ### Simulation Parameters
    num_particles = 50         # Number of particles
    tube_width = 50.0          # Chamber width in cm
    tube_height = 25.0         # Chamber height in cm
    particle_radius = 0.9      # Particle radius in cm
    gravity = 980.0            # Gravity acceleration (cm/s²)
    start_time = 1.0           # Time when free fall begins (seconds)
    simulation_time = 10.0     # Total simulation duration (seconds)
    dt = 0.01                  # Time step (seconds)
    restitution = 0.8          # Bounce energy loss coefficient

    # ### Initialize Particle Positions and Velocities
    # Start particles near the top with small random motion
    particles_x = np.random.uniform(particle_radius, tube_width - particle_radius, num_particles)
    particles_y = np.random.uniform(tube_height - particle_radius - 5, tube_height - particle_radius, num_particles)
    particles_vx = np.random.uniform(-5, 5, num_particles)  # Small horizontal velocity
    particles_vy = np.random.uniform(-5, 5, num_particles)  # Small vertical velocity

    # ### Set Up the Plot
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_xlim(0, tube_width)
    ax.set_ylim(0, tube_height)
    ax.set_aspect('equal')

    # Draw the chamber as a rectangle
    tube = Rectangle((0, 0), tube_width, tube_height, edgecolor='black', facecolor='none', linewidth=2)
    ax.add_patch(tube)

    # Create particle circles
    particle_circles = [Circle((particles_x[i], particles_y[i]), particle_radius, 
                               facecolor='blue', edgecolor='blue') for i in range(num_particles)]
    for circle in particle_circles:
        ax.add_patch(circle)

    # Add status text
    status_text = ax.text(tube_width / 2, tube_height - 5, '', ha='center', fontsize=12)

    # ### Simulation State Variables
    current_time = 0.0
    is_free_fall = False

    # ### Animation Update Function
    def update(frame):
        nonlocal current_time, is_free_fall

        # Switch to free fall after 2 seconds
        if current_time >= start_time and not is_free_fall:
            is_free_fall = True
            print(f"Free fall started at t = {current_time:.2f} seconds")

        # Set effective gravity: normal before free fall, zero during
        g_eff = 0.0 if is_free_fall else gravity

        # Update status display
        status_message = (
            f"Time: {current_time:.2f} s\n"
            f"Effective Gravity: {g_eff:.2f} cm/s²\n"
            f"Free Fall: {'Active' if is_free_fall else 'Waiting'}"
        )
        status_text.set_text(status_message)

        # Update velocities (gravity only applies before free fall)
        if not is_free_fall:
            particles_vy[:] += g_eff * dt  # Gravity increases downward velocity

        # Update positions (y decreases as vy is positive downward)
        particles_x[:] += particles_vx[:] * dt
        particles_y[:] -= particles_vy[:] * dt

        # ### Handle Collisions with Chamber Walls
        # Left wall
        left_collision = particles_x < particle_radius
        particles_vx[left_collision] *= -restitution
        particles_x[left_collision] = particle_radius

        # Right wall
        right_collision = particles_x > tube_width - particle_radius
        particles_vx[right_collision] *= -restitution
        particles_x[right_collision] = tube_width - particle_radius

        # Bottom wall
        bottom_collision = particles_y < particle_radius
        particles_vy[bottom_collision] *= -restitution
        particles_y[bottom_collision] = particle_radius

        # Top wall
        top_collision = particles_y > tube_height - particle_radius
        particles_vy[top_collision] *= -restitution
        particles_y[top_collision] = tube_height - particle_radius

        # ### Update Particle Positions in Animation
        for i in range(num_particles):
            particle_circles[i].center = (particles_x[i], particles_y[i])

        # Increment simulation time
        current_time += dt

        # Stop simulation if time exceeds limit
        if current_time > simulation_time:
            anim.event_source.stop()
            print(f"Simulation completed at t = {current_time:.2f} seconds")

        return particle_circles + [status_text]

    # ### Run the Animation
    frames = int(simulation_time / dt)
    anim = FuncAnimation(fig, update, frames=frames, interval=20, repeat=False)
    plt.show()

# ### Execute the Simulation
if __name__ == "__main__":
    free_fall_simulation()