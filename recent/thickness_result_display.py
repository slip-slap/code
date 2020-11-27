import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import thickness_three_angle_result as result

##################################
problem = 'fitness(length)'


x_coordinate = result.result_times
fig, ax1_1= plt.subplots(1, 1)
color = 'tab:red'
color= 'k'

"""
ax1_1.set_xlabel('generation (s)', fontsize=18)
ax1_1.set_ylabel(problem, color=color,fontsize=18)
ax1_1.set_ylim([0,150])
ax1_1.plot(x_coordinate, result.result_fitness, color=color)
ax1_1.tick_params(axis='y', labelcolor=color)

custom_lines_fitness = [lines.Line2D([0],[0],color='black',linestyle="-" ),
                        lines.Line2D([0],[0],color='black', linestyle="--")]

ax1_1.legend(custom_lines_fitness,['fitness','strength ratio'],loc='best', 
        fontsize=13,)

ax1_2 = ax1_1.twinx()  # instantiate a second axes that shares the same x-axis

ax1_2.set_ylabel('strength ratio(SR)', color="black",fontsize=18)  # we already handled the x-label with ax1
ax1_2.set_ylim([0,1.5])
ax1_2.plot(x_coordinate, result.result_strength_ratio, color='black', linestyle="--") 
ax1_2.tick_params(axis='y', labelcolor=color)

"""
#############################
ax1_1.set_xlabel('generation (s)', fontsize=18)
ax1_1.set_ylabel("angle", color=color,fontsize=18)
ax1_1.set_ylim([-90,90])
ax1_1.plot(x_coordinate, result.result_angle0, color=color, marker="D", markevery=21)
ax1_1.plot(x_coordinate, result.result_angle1, color=color, marker="d", markevery=30)
ax1_1.plot(x_coordinate, result.result_angle2, color=color, marker="s", markevery=35)
ax1_1.tick_params(axis='y', labelcolor=color)

custom_lines_fitness = [lines.Line2D([0],[0],color='black', marker="D", markevery=21),
                        lines.Line2D([0],[0],color='black', marker="d", markevery=30),
                        lines.Line2D([0],[0],color='black', marker="s", markevery=35)]

ax1_1.legend(custom_lines_fitness,['first angle','second angle', 'third angle'],loc='best', 
        fontsize=13,)
############################
"""
ax1_1.set_xlabel('generation (s)', fontsize=18)
ax1_1.set_ylabel("number of angle", color=color,fontsize=18)
ax1_1.set_ylim([0,100])
ax1_1.plot(x_coordinate, result.result_number0, color=color, marker="D", markevery=21)
ax1_1.plot(x_coordinate, result.result_number1, color=color, marker="d", markevery=30)
ax1_1.plot(x_coordinate, result.result_number2, color=color, marker="s", markevery=35)
ax1_1.tick_params(axis='y', labelcolor=color)

custom_lines_fitness = [lines.Line2D([0],[0],color='black', marker="D", markevery=21),
                        lines.Line2D([0],[0],color='black', marker="d", markevery=30),
                        lines.Line2D([0],[0],color='black', marker="s", markevery=35)]

ax1_1.legend(custom_lines_fitness,['number of first angle','number of second angle', 'number of third angle'],loc='best', 
        fontsize=13,)
"""
#############################
"""
"""
############################



########################################
""" dedicated for two angles
ax1_1.set_xlabel('generation (s)', fontsize=18)
ax1_1.set_ylabel("first angle", color=color,fontsize=18)
ax1_1.set_ylim([-100,100])
ax1_1.plot(x_coordinate, result.result_angle0, color=color, linestyle="--")
ax1_1.tick_params(axis='y', labelcolor=color)
custom_lines_fitness = [lines.Line2D([0],[0],color='black',linestyle="--" ),
                        lines.Line2D([0],[0],color='black', linestyle="-")]
ax1_1.legend(custom_lines_fitness,['first angle','second angle'],loc='best', 
        fontsize=13,)
ax1_2 = ax1_1.twinx()  # instantiate a second axes that shares the same x-axis
ax1_2.set_ylabel('second angle', color="black",fontsize=18)  # we already handled the x-label with ax1
ax1_2.set_ylim([-100,100])
ax1_2.plot(x_coordinate, result.result_angle1, color='black', linestyle="-") 
ax1_2.tick_params(axis='y', labelcolor=color)
"""
####################################

########################################
""" dedicated for two angles
ax1_1.set_xlabel('generation (s)', fontsize=18)
ax1_1.set_ylabel("number of first angle", color=color,fontsize=18)
ax1_1.set_ylim([0,100])
ax1_1.plot(x_coordinate, result.result_number0, color=color, linestyle="--")
ax1_1.tick_params(axis='y', labelcolor=color)
custom_lines_fitness = [lines.Line2D([0],[0],color='black',linestyle="--" ),
                        lines.Line2D([0],[0],color='black', linestyle="-")]
ax1_1.legend(custom_lines_fitness,['number of first angle','number of second angle'],loc='best', 
        fontsize=13,)
ax1_2 = ax1_1.twinx()  # instantiate a second axes that shares the same x-axis
ax1_2.set_ylabel('number of second angle', color="black",fontsize=18)  # we already handled the x-label with ax1
ax1_2.set_ylim([0,100])
ax1_2.plot(x_coordinate, result.result_number1, color='black', linestyle="-") 
ax1_2.tick_params(axis='y', labelcolor=color)
"""
####################################
fig.tight_layout()  # otherwise the right y-label is slightly clipped

plt.rcParams.update({'font.size': 18})


plt.show()
