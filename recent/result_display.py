import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
#import selection_method_comparsion_result as result
import seed_test as result

##################################
problem = 'fitness(problem I)'


x_coordinate = list(np.arange(1,102,1))
fig, ax1 = plt.subplots()
color = 'tab:red'
color= 'k'
ax1.set_xlabel('generation (s)', fontsize=18)

ax1.set_ylabel(problem, color=color,fontsize=18)
ax1.set_ylim([0,10])
ax1.plot(x_coordinate, result.original_fitness_, color=color, marker='D', markevery=10)
ax1.plot(x_coordinate, result.improved_fitness_, color=color, marker='h', markevery=9)
ax1.tick_params(axis='y', labelcolor=color)

custom_lines_fitness = [lines.Line2D([0],[0],color='black', marker='D'),
                        lines.Line2D([0],[0],color='black', marker='h')]
ax1.legend(custom_lines_fitness,['fitness of Basic GA','fitness of Improved GA'],loc='right', 
        bbox_to_anchor=[1,0.1],fontsize=13,)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'k'
ax2.set_ylabel('strength ratio(SR)', color=color,fontsize=18)  # we already handled the x-label with ax1
ax2.set_ylim([0,3])
ax2.plot(x_coordinate, result.original_strength_ratio_, color=color, marker='D',
        markevery=10,linestyle=':')
ax2.plot(x_coordinate, result.improved_strength_ratio_, color=color, marker='h',
        markevery=9,linestyle=':')
ax2.tick_params(axis='y', labelcolor=color)


custom_lines = [lines.Line2D([0],[0],color='black', marker='D',linestyle=':'),
                lines.Line2D([0],[0],color='black', marker='h',linestyle=':')]
fig.tight_layout()  # otherwise the right y-label is slightly clipped

plt.annotate("Load:      $N_x= N_y=1e6$ N \nMaterial: GR",xy=(25,2.5),fontsize=13)
plt.legend(custom_lines,['SR of Basic GA','SR of Improved GA'],loc="lower right",
                        bbox_to_anchor=[0.93,0.45], fontsize=13)
plt.rcParams.update({'font.size': 18})

plt.show()
