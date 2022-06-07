import os
import pandas as pd
from matplotlib import pyplot as plt

print(*[filename.split('.')[0] for filename in os.listdir('./opinions')], sep='\n')

product_id = input('Please enter product id: ')

opinions = pd.read_json(f'opinions/{product_id}.json')

opinions_count = len(opinions)
pros_count = opinions['pros'].map(bool).sum()
cons_count = opinions['cons'].map(bool).sum()
average_score = opinions['score'].mean().round(2)

stars_recommendation = pd.crosstab(opinions['score'], opinions['rcmd'], dropna=False).sort_index().reindex([1, 2, 3, 4, 5])
# print(stars_recommendation)

recommendations = opinions['rcmd'].value_counts(dropna=False).sort_index().reindex([False, True, None])

# print(opinions_count)
# print(type(recommendations))
# print(recommendations)

if not os.path.isdir('opinions/'):
    os.mkdir('opinions/')

recommendations.plot.pie(
    label = '',
    title = 'Recommendations: ' + product_id,
    labels = ['Not recommend', 'Recommend', 'No opinion'],
    colors = ['crimson', 'forestgreen', 'grey'],
    autopct = lambda p: '{:.1f}%'.format(p) if p > 0 else ''
)

plt.savefig(f'plots/{product_id}_rcmd.png', dpi = 500)

stars_recommendation.plot.bar(
    label = '',
    title = 'Stars: ' + product_id,
    ylabel = 'Number of scores',
    xlabel = 'Score',
)

plt.savefig(f'plots/{product_id}_stars.png', dpi = 500)
plt.close()
