import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

class ULMW():
    def __init__(self, settings):
        self.head_start = settings.head_start
        self.r1 = settings.r1
        self.r2 = settings.r2
        self.r3 = settings.r3
        self.rack_length = settings.rack_length
        self.ULMWDia = settings.ULMWDia
        self.ULMWPerimeter = settings.ULMWPerimeter
        self.fig = settings.fig
        self.ax = settings.ax

        self.endPerimeter = np.pi * self.ULMWDia / 2
        self.gearArmCenterDistance = self.r1 + self.r2
        self.gear1Perimenter = np.pi * self.r1*2
        self.gear2Perimenter = np.pi * self.r2*2
        self.gear3Perimenter = np.pi * self.r3*2     
        
        if self.ax is not None:
            self.centerLine, = self.ax.plot([], [], f"{settings.colours[0]}--")
            self.side_right, = self.ax.plot([], [], f"{settings.colours[0]}-")
            self.side_left, = self.ax.plot([], [], f"{settings.colours[0]}-")
            self.semi_circle_top, = self.ax.plot([], [], f"{settings.colours[0]}-")
            self.semi_circle_bottom, = self.ax.plot([], [], f"{settings.colours[0]}-")
            self.gear_arm_line, = self.ax.plot([], [], f"{settings.colours[1]}-")  # Line representing gear arm

            self.gear1, = self.ax.plot([], [], f"{settings.colours[2]}-")
            self.gear2, = self.ax.plot([], [], f"{settings.colours[0]}-")
            self.gear3, = self.ax.plot([], [], f"{settings.colours[3]}-")

        

        self.checkPoints = [
            self.rack_length / 2,  # Quadrant 1
            self.rack_length / 2 + self.endPerimeter,  # Quadrant -1
            self.rack_length / 2 + self.endPerimeter + self.rack_length / 2,  # Quadrant 2
            self.rack_length / 2 + self.endPerimeter + self.rack_length,  # Quadrant 3
            self.rack_length / 2 + self.endPerimeter + self.rack_length + self.endPerimeter,  # Quadrant -2
            self.rack_length / 2 + self.endPerimeter + self.rack_length + self.endPerimeter + self.rack_length / 2  # Quadrant 4
        ]

        
        self.theta1 = self.theta2 = self.theta3 = 0

    def create_gear(self, r, num_teeth=20):
        theta = np.linspace(0, 2 * np.pi, num_teeth, endpoint=False)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return x, y

    def setPosition(self, position):
        position+=self.head_start
        # Calculate the quadrant and remaining position
        gear1Rem=position %(self.gear1Perimenter)
        self.theta1 = -360* gear1Rem/self.gear1Perimenter

        gear2Rem=position %(self.gear2Perimenter)
        self.theta2 = 360* gear2Rem/self.gear2Perimenter

        gear3Rem=position %(self.gear3Perimenter)
        self.theta3 = 360* gear3Rem/self.gear3Perimenter

        remPosition = position % self.ULMWPerimeter
        position = remPosition
        for i, point in enumerate(self.checkPoints):
            if remPosition < point:
                rackQuadrant = i
                break

        armAngle = 0  # degrees

        if rackQuadrant == 0:  # [0]
            rackAssemblyCenterPosition = -position  # a negative value
        elif rackQuadrant == 1:  # [1] # Dwell
            armAngle = 180 - 180 * (self.checkPoints[1] - position) / (self.checkPoints[1] - self.checkPoints[0])
            rackAssemblyCenterPosition = -(self.rack_length / 2)  # negative value
        elif rackQuadrant == 2:  # [2]
            armAngle = 180
            rackAssemblyCenterPosition = -(self.checkPoints[2] - position)  # negative value
        elif rackQuadrant == 3:  # [0]
            armAngle = 180
            rackAssemblyCenterPosition = (self.rack_length / 2) - (self.checkPoints[3] - position)  # +ve value
        elif rackQuadrant == 4:  # Dwell
            armAngle = 360 - 180 * (self.checkPoints[4] - position) / (self.checkPoints[4] - self.checkPoints[3])
            rackAssemblyCenterPosition = self.rack_length / 2
        else:  # rackQuadrant == 5
            rackAssemblyCenterPosition = self.checkPoints[5] - position  # +ve value

        return rackAssemblyCenterPosition, armAngle
    
    def armAnglePoints(self):
        arm_angles = []
        for position in range(int(self.ULMWPerimeter)):
            _, arm_angle = self.setPosition(position)
            if arm_angle > 180:
                arm_angle = 180 - (arm_angle-180)
            arm_angles.append(arm_angle)
        return arm_angles

    def plot_arm_angles(self):
        import matplotlib.pyplot as plt

        arm_angles = self.armAnglePoints()
        positions = range(int(self.ULMWPerimeter))

        plt.figure(figsize=(12, 6))
        plt.plot(positions, arm_angles)
        plt.title('Arm Angle vs Position')
        plt.xlabel('Position')
        plt.ylabel('Arm Angle (degrees)')
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_multiple_arm_angles(instances, labels=None, save=None):
        # plt.figure(figsize=(12, 6))
        
        for i, instance in enumerate(instances):
            arm_angles = instance.armAnglePoints()
            positions = range(int(instance.ULMWPerimeter))
            
            label = labels[i] if labels and i < len(labels) else f'Instance {i+1}'
            plt.plot(positions, arm_angles, label=label)
        
        plt.suptitle('Arm Location(angle)', fontsize=14)
        plt.title(f"r_ULMW={instances[0].ULMWDia/2}, length={instances[0].rack_length}", fontsize=10)
        plt.xlabel('Arm Distance')
        plt.ylabel('Arm Angle (degrees)')
        plt.grid(True)
        plt.legend()
        
        if save:
            plt.savefig(save)
        plt.show()
    
    @staticmethod
    def plot_dynamic_arm_angles(num_instances, ULMWRadius, rack_length, labels=None, save=None):
        instances = []
        r1 = r2 = r3 = ULMWRadius
        
        # Create instances
        for i in range(num_instances):
            settings = Settings(rack_length, r1, r2, r3, None, None, numULMWs=num_instances, num=i)
            instance = ULMW(settings)
            instances.append(instance)

        # Plot
        plt.figure(figsize=(12, 6))
        
        for i, instance in enumerate(instances):
            arm_angles = instance.armAnglePoints()
            positions = range(int(instance.ULMWPerimeter))
            
            label = labels[i] if labels and i < len(labels) else f'Instance {i+1}'
            plt.plot(positions, arm_angles, label=label)
        
        plt.suptitle('Arm Location (angle)', fontsize=14)
        plt.title(f"r_ULMW={ULMWRadius}, rack_length={rack_length}", fontsize=10)
        plt.xlabel('Arm Distance')
        plt.ylabel('Arm Angle (degrees)')
        plt.grid(True)
        plt.legend()
        
        if save:
            plt.savefig(save)
        plt.show()
    
    @staticmethod
    def plot_dynamic_arm_angles1(num_instances, ULMWRadius, rack_length, labels=None, zero_threshold=0.1,save=None):
        instances = []
        r1 = r2 = r3 = ULMWRadius
        
        # Create instances
        for i in range(num_instances):
            settings = Settings(rack_length, r1, r2, r3, None, None, numULMWs=num_instances, num=i)
            instance = ULMW(settings)
            instances.append(instance)

        # Collect data
        all_arm_angles = []
        for instance in instances:
            arm_angles = instance.armAnglePoints()
            all_arm_angles.append(arm_angles)

        # Convert to numpy array for easier manipulation
        all_arm_angles = np.array(all_arm_angles)

        # Count instances with arm angle close to 0 for each position
        zero_count = np.sum(np.abs(all_arm_angles) < zero_threshold, axis=0)

        # Plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        
        # Plot arm angles
        for i, arm_angles in enumerate(all_arm_angles):
            positions = range(int(instances[0].ULMWPerimeter))
            label = labels[i] if labels and i < len(labels) else f'Instance {i+1}'
            ax1.plot(positions, arm_angles, label=label)
        
        ax1.set_ylabel('Arm Angle (degrees)')
        ax1.grid(True)
        ax1.legend()

        # Plot count of instances with arm angle = 0
        ax2.plot(positions, zero_count, color='red', linewidth=2)
        ax2.set_xlabel('Arm Distance')
        ax2.set_ylabel('Count of Instances\nwith Arm Angle ≈ 0')
        ax2.grid(True)

        plt.suptitle('Arm Location Analysis', fontsize=14)
        plt.title(f"r_ULMW={ULMWRadius}, rack_length={rack_length}", fontsize=10)
        plt.tight_layout()
        if save:
            plt.savefig(save)
        plt.show()

    def init_plot(self):
        # Initialize the plot limits and labels
        self.ax.set_xlim(-2 * self.ULMWDia, 2 * self.ULMWDia)
        self.ax.set_ylim(-30, 30)
        plt.title("Position Animation")
        plt.xlabel('Position')
        plt.ylabel('Y-axis')
        plt.grid(True)
        return self.centerLine, self.side_right, self.side_left, self.semi_circle_top, self.semi_circle_bottom, self.gear_arm_line, self.gear1, self.gear2, self.gear3

    def create_semi_circle(self, offset_y, direction=1):
        radius = self.ULMWDia / 2
        theta = np.linspace(0, np.pi * direction, 100)
        x = radius * np.cos(theta)
        y = radius * np.sin(theta) + offset_y
        return x, y

    def update_plot(self, position):
        # Update the vertical line position
        rackAssemblyCenterPosition, armAngle = self.setPosition(position)
        self.centerLine.set_data([0, 0], [rackAssemblyCenterPosition - self.rack_length / 2,
                                          rackAssemblyCenterPosition + self.rack_length / 2])
        self.side_right.set_data([self.ULMWDia / 2, self.ULMWDia / 2], [rackAssemblyCenterPosition - self.rack_length / 2,
                                                                        rackAssemblyCenterPosition + self.rack_length / 2])
        self.side_left.set_data([-self.ULMWDia / 2, -self.ULMWDia / 2], [rackAssemblyCenterPosition - self.rack_length / 2,
                                                                         rackAssemblyCenterPosition + self.rack_length / 2])

        x_top, y_top = self.create_semi_circle(rackAssemblyCenterPosition + self.rack_length / 2)
        x_bottom, y_bottom = self.create_semi_circle(rackAssemblyCenterPosition - self.rack_length / 2, -1)

        self.semi_circle_top.set_data(x_top, y_top)
        self.semi_circle_bottom.set_data(x_bottom, y_bottom)

        # Calculate the end coordinates of the gear arm line
        end_x = self.gearArmCenterDistance * np.cos(np.radians(armAngle))
        end_y = self.gearArmCenterDistance * np.sin(np.radians(armAngle))
        self.gear_arm_line.set_data([0, end_x], [0, end_y])

        x1, y1 = self.create_gear(self.r1)
        x2, y2 = self.create_gear(self.r2)
        x3, y3 = self.create_gear(self.r3)

        theta1 = np.radians(self.theta1)
        theta2 = np.radians(self.theta2)
        theta3 = np.radians(self.theta3)
        # if armAngle not in [0, 180]:
        theta3 += np.radians(armAngle)
        theta2 = theta3

        # Apply rotations
        x1r = x1 * np.cos(theta1) - y1 * np.sin(theta1)
        y1r = x1 * np.sin(theta1) + y1 * np.cos(theta1)

        x2r = x2 * np.cos(theta2) - y2 * np.sin(theta2)
        y2r = x2 * np.sin(theta2) + y2 * np.cos(theta2)

        x3r = x3 * np.cos(theta3) - y3 * np.sin(theta3)
        y3r = x3 * np.sin(theta3) + y3 * np.cos(theta3)

        # Update data for the gears
        self.gear1.set_data(x1r, y1r)
        self.gear2.set_data(x2r + end_x, y2r + end_y)
        self.gear3.set_data(x3r + end_x, y3r + end_y)

        return self.centerLine, self.side_right, self.side_left, self.semi_circle_top, self.semi_circle_bottom, self.gear_arm_line, self.gear1, self.gear2, self.gear3

    def animatePosition(self):
        # Create animation
        frames_forward = np.arange(0, 101)  # Forward frames from 0 to 100
        frames_backward = np.arange(100, -1,-1)  # Backward frames from 100 to 0
        # Concatenate the forward and backward frames
        frames = np.concatenate((frames_forward, frames_backward))
        anim = FuncAnimation(self.fig, self.update_plot, frames=frames,
                             init_func=self.init_plot, blit=True)
        plt.show()

    @staticmethod
    def dMax(working_length, rack_length, num_sets): # maximum ULMW Diameter
        dMax = (working_length * num_sets - 2 * rack_length)/np.pi
        return dMax
    
    @staticmethod
    def lMin(working_length, d, num_sets): # minimum rack_length
        rack_length = (working_length * num_sets - np.pi *d)/2
        return rack_length


# Define a sample Settings class
class Settings:
    def __init__(self, rack_length, r1, r2, r3, fig, ax, head_start=0, numULMWs=1, num=0):
        self.rack_length = rack_length
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        
        self.fig = fig
        self.ax = ax

        self.ULMWDia = (r1 + r2 - r3) * 2
        self.ULMWPerimeter = 2 * rack_length + np.pi * self.ULMWDia
        #head_start
        self.head_start = head_start
        if numULMWs > 1:
            self.head_start = (num/numULMWs)*self.ULMWPerimeter

        if ax is not None:
            ax.set_xlim(-2 * self.ULMWDia, 2 * self.ULMWDia)
            len = 2*self.rack_length+self.ULMWDia
            ax.set_ylim(-len/2, len/2)

        # Define list of colors using single-character codes
        colours = [
            ['k', 'r', 'g', 'b'],  # Set 1
            ['c', 'm', 'y', 'k'],  # Set 2
            ['m', 'y', 'b', 'g'],  # Set 3
            ['r', 'g', 'b', 'c'],  # Set 4
            ['y', 'b', 'g', 'k'],  # Set 5
            ['k', 'c', 'r', 'm'],  # Set 6
            ['g', 'y', 'c', 'b'],  # Set 7
            ['b', 'k', 'y', 'r'],  # Set 8
            ['m', 'c', 'k', 'g'],  # Set 9
            ['r', 'y', 'm', 'b']   # Set 10
        ]
        
        # Assign colors based on num
        # self.colours = colours[int(num % len(colours))]
        self.colours = colours[num % 10] # problem with len(colours)

