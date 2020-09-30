import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import selection_method_comparsion_result as result

##################################
problem = 'fitness(problem II)'


x_coordinate = list(np.arange(1,102,1))
fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_xlabel('generation (s)', fontsize=18)

ax1.set_ylabel(problem, color=color,fontsize=18)
ax1.set_ylim([1,4])
ax1.plot(x_coordinate, result.original_fitness_, color=color, marker='D', markevery=6)
ax1.plot(x_coordinate, result.improved_fitness_, color=color, marker='h', markevery=5)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('strength ratio', color=color,fontsize=18)  # we already handled the x-label with ax1
ax2.set_ylim([1,4])
ax2.plot(x_coordinate, result.original_strength_ratio_, color=color, marker='D', markevery=6)
ax2.plot(x_coordinate, result.improved_strength_ratio_, color=color, marker='h', markevery=5)
ax2.tick_params(axis='y', labelcolor=color)


custom_lines = [lines.Line2D([0],[0],color='black', marker='D'),
                lines.Line2D([0],[0],color='black', marker='h'),
               ]

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.annotate("Load:      $N_x= N_y=N_z=1e6$ N \nMaterial: GR GL",xy=(0,3.55),fontsize=13)
plt.legend(custom_lines,['Original GA','Improved GA'],loc="upper right",fontsize=13)

plt.rcParams.update({'font.size': 18})

plt.show()
