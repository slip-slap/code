import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import thickness_result as result

##################################
problem = 'fitness(length)'


x_coordinate = result.result_times
plt.rcParams["figure.figsize"] = (10,4)
fig, (ax1_1,ax2_1)= plt.subplots(1, 2)
color = 'tab:red'
color= 'k'
ax1_1.set_xlabel('generation (s)', fontsize=18)

ax1_1.set_ylabel(problem, color=color,fontsize=18)
ax1_1.set_ylim([0,120])
ax1_1.plot(x_coordinate, result.result_fitness, color=color)
ax1_1.tick_params(axis='y', labelcolor=color)

custom_lines_fitness = [lines.Line2D([0],[0],color='black' ),
                        lines.Line2D([0],[0],color='black')]

ax1_2 = ax1_1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'k'
ax1_2.set_ylabel('strength ratio(SR)', color=color,fontsize=18)  # we already handled the x-label with ax1
ax1_2.set_ylim([0,1.5])
ax1_2.plot(x_coordinate, result.result_strength_ratio, color='red') 
ax1_2.tick_params(axis='y', labelcolor=color)


custom_lines = [lines.Line2D([0],[0],color='black', marker='D',linestyle=':'),
                lines.Line2D([0],[0],color='black', marker='h',linestyle=':')]
fig.tight_layout()  # otherwise the right y-label is slightly clipped

plt.annotate("Load:      $N_x= N_y=1e6$ N ",xy=(25,2.5),fontsize=13)
plt.rcParams.update({'font.size': 18})


ax2_1.set_ylim([-90,90])
ax2_1.plot(x_coordinate, result.result_angle1)

ax2_2 = ax2_1.twinx()
ax2_2.set_ylim([-90,90])
ax2_2.plot(x_coordinate, result.result_angle2)




plt.show()
