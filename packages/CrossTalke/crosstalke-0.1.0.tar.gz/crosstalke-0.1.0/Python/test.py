
import CrossTalkeP
from CrossTalkeP import *
from plot import *
import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data from pickle file
with open("output/LR_data.pkl", "rb") as f:
    data = pickle.load(f)


graph_ctr = data["graphs"]["EXP_x_CTR"]
colors_ctr = data["colors"]
coords_ctr =  data["coords"]
pg = data["rankings"]["EXP_x_CTR"]["Pagerank"]




plot_cci(graph=graph_ctr,
         colors=colors_ctr,
         plt_name='Control',
         coords=coords_ctr,
         emax= None,
         leg= False,
         low= 0,
         high= 0, 
         ignore_alpha= False,
         log= False,
         efactor= 6,
         vfactor= 0.03, 
         pg= pg
         )


# # Analysis on the Gene-Cell Interaction Level

rankings_table_ctr = data['rankings']['CTR_ggi'].sort_values(by='Pagerank', ascending=False).head(10)
rankings_table_ctr['signal'] = ['negative' if x < 0 else 'positive' for x in rankings_table_ctr['Pagerank']]
rankings_table_exp = data['rankings']['EXP_ggi'].sort_values(by='Pagerank', ascending=False).head(10)
rankings_table_exp['signal'] = ['negative' if x < 0 else 'positive' for x in rankings_table_exp['Pagerank']]
custom_palette = {'positive': '#ff3e3e', 'negative': '#00FFFF'}  # Orange and Blue
fig, axs = plt.subplots(1, 2, figsize=(15, 8))

# Plot for CTR_ggi
sns.barplot(ax=axs[0], x='Pagerank', y='nodes', data=rankings_table_ctr, hue='signal', dodge=False, palette=custom_palette)
axs[0].set_title("Top Listener in Control Condition")
axs[0].set_xlabel('Pagerank')
axs[0].set_ylabel('Nodes')

# Set x-axis tick intervals for CTR_ggi
ctr_max = rankings_table_ctr['Pagerank'].max()
ctr_min = rankings_table_ctr['Pagerank'].min()
ctr_ticks = np.linspace(ctr_min, ctr_max, num=3)  # Adjust 'num' for more/less intervals
axs[0].set_xticks(ctr_ticks)
axs[0].set_xticklabels([f'{tick:.2f}' for tick in ctr_ticks])

# Plot for EXP_ggi
sns.barplot(ax=axs[1], x='Pagerank', y='nodes', data=rankings_table_exp, hue='signal', dodge=False, palette=custom_palette)
axs[1].set_title("Top Listener in Disease Condition")
axs[1].set_xlabel('Pagerank')
axs[1].set_ylabel('')

# Set x-axis tick intervals for EXP_ggi
exp_max = rankings_table_exp['Pagerank'].max()
exp_min = rankings_table_exp['Pagerank'].min()
exp_ticks = np.linspace(exp_min, exp_max, num=3)  # Adjust 'num' for more/less intervals
axs[1].set_xticks(exp_ticks)
axs[1].set_xticklabels([f'{tick:.2f}' for tick in exp_ticks])

axs[0].grid(True, linestyle='--', linewidth=0.5)
axs[1].grid(True, linestyle='--', linewidth=0.5)
axs[0].set_axisbelow(True)
axs[1].set_axisbelow(True)
handles, labels = axs[0].get_legend_handles_labels()
plt.tight_layout()
plt.show()


# # Compared Coondition Results

custom_palette = {'positive': '#00FFFF', 'negative':'#ff3e3e'}  # Orange and Blue

# Iterate through the rankings and plot
for key in data['rankings']:
    if '_x_' in key and 'ggi' not in key:
        rankings_table = data['rankings'][key]
        rankings_table = rankings_table.sort_values(by='Pagerank')
        rankings_table['signal'] = ['negative' if x < 0 else 'positive' for x in rankings_table['Pagerank']]

        # Plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Pagerank', y='nodes', data=rankings_table, hue='signal', dodge=False, palette=custom_palette)
        plt.title(f"Ranking for {key}")
        plt.xlabel('Pagerank')
        plt.ylabel('Nodes')

        # Set x-axis tick intervals
        max_val = rankings_table['Pagerank'].max()
        min_val = rankings_table['Pagerank'].min()
        ticks = np.linspace(min_val, max_val, num=5)  # Adjust 'num' for more/less intervals
        plt.xticks(ticks, [f'{tick:.2f}' for tick in ticks])

        # Invert y-axis to have highest values at the top
        plt.gca().invert_yaxis()

        # Show the legend only once
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles, labels, loc='lower right')

        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.gca().set_axisbelow(True)
        # Adjust layout and show plot
        plt.tight_layout()
        plt.show()
        


for key in data['rankings']:
    if '_x_' in key and 'ggi' not in key:
        rankings_table = data['rankings'][key]
        rankings_table = rankings_table.sort_values(by='Influencer')
        rankings_table['signal'] = ['negative' if x < 0 else 'positive' for x in rankings_table['Influencer']]

        plt.figure(figsize=(10, 6))
        sns.barplot(x='Influencer', y='nodes', data=rankings_table, hue= 'signal', dodge= False, palette = custom_palette)
        

        plt.title(key)
        plt.xlabel('Influencer')
        plt.ylabel('Nodes')

        # Set x-axis tick intervals
        max_val = rankings_table['Influencer'].max()
        min_val = rankings_table['Influencer'].min()
        ticks = np.linspace(min_val, max_val, num=5)  # Adjust 'num' for more/less intervals
        plt.xticks(ticks, [f'{tick:.2f}' for tick in ticks])

        # Invert y-axis to have highest values at the top
        plt.gca().invert_yaxis()

        # Show the legend only once
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles, labels, loc='lower right')

        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.gca().set_axisbelow(True)
        # Adjust layout and show plot
        plt.tight_layout()
        plt.show()



# Iterate through the rankings and plot
for key in data['rankings']:
    if '_x_' in key and 'ggi' in key:
        rankings_table = data['rankings'][key]
        rankings_table = rankings_table.loc[rankings_table['Pagerank'].abs().nlargest(20).index]
        rankings_table = rankings_table.sort_values(by='Pagerank')
        rankings_table['signal'] = ['negative' if x < 0 else 'positive' for x in rankings_table['Pagerank']]

        # Plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Pagerank', y='nodes', data=rankings_table, hue='signal', dodge=False, palette=custom_palette)
        plt.title(f"Ranking for {key}")
        plt.xlabel('Pagerank')
        plt.ylabel('Nodes')

        # Set x-axis tick intervals
        max_val = rankings_table['Pagerank'].max()
        min_val = rankings_table['Pagerank'].min()
        ticks = np.linspace(min_val, max_val, num=5)  # Adjust 'num' for more/less intervals
        plt.xticks(ticks, [f'{tick:.2f}' for tick in ticks])

        # Invert y-axis to have highest values at the top
        plt.gca().invert_yaxis()

        # Show the legend only once
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles, labels, loc='lower right')

        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.gca().set_axisbelow(True)
        # Adjust layout and show plot
        plt.tight_layout()
        plt.show()

plot_pca_LR_comparative(
    lrobj_tblPCA = data,
    pca_table = "EXP_x_CTR_ggi",
    dims = (1, 2),
    ret = True,
    ggi = True
)
