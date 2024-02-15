from glintcontrol import glintcontrol

glint_control_instance = glintcontrol(datapath = '.')  # Create an instance of the glintcontrol class
result = glint_control_instance.sim_chip()  # Call the sim_chip method on the instance
