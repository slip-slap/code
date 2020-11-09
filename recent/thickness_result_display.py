import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import thickness_result as result

##################################
problem = 'fitness(length)'


x_coordinate = result.result_times
fig, ax1_1= plt.subplots(1, 1)
color = 'tab:red'
color= 'k'

"""
ax1_1.set_xlabel('generation (s)', fontsize=18)
ax1_1.set_ylabel(problem, color=color,fontsize=18)
ax1_1.set_ylim([0,120])
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

ax1_1.set_xlabel('generation (s)', fontsize=18)
ax1_1.set_ylabel("first angle", color=color,fontsize=18)
ax1_1.set_ylim([-100,100])
ax1_1.plot(x_coordinate, result.result_angle1, color=color, linestyle="--")
ax1_1.tick_params(axis='y', labelcolor=color)

custom_lines_fitness = [lines.Line2D([0],[0],color='black',linestyle="--" ),
                        lines.Line2D([0],[0],color='black', linestyle="-")]

ax1_1.legend(custom_lines_fitness,['first angle','second angle'],loc='best', 
        fontsize=13,)

ax1_2 = ax1_1.twinx()  # instantiate a second axes that shares the same x-axis

ax1_2.set_ylabel('second angle', color="black",fontsize=18)  # we already handled the x-label with ax1
ax1_2.set_ylim([-100,100])
ax1_2.plot(x_coordinate, result.result_angle2, color='black', linestyle="-") 
ax1_2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped

plt.rcParams.update({'font.size': 18})


plt.show()
