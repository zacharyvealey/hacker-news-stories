import requests
from operator import itemgetter
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

# Make an API call and store the response.
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print("Status code:", r.status_code)

# Process information about each submission.
submission_ids = r.json()
titles, submission_dicts = [], []
rank = list(range(1,31))

for submission_id in submission_ids[:31]:
    # Make a separate API call for each submission.
    url = ('https://hacker-news.firebaseio.com/v0/item/' +
            str(submission_id) + '.json')
    submission_r = requests.get(url)
    print(submission_r.status_code)
    response_dict = submission_r.json()

    #titles.append(response_dict['title'])
    submission_dict = {
        'value': response_dict.get('descendants', 0),
        'label': response_dict['title'],
        'xlink': 'http://news.ycombinator.com/item?id=' + str(submission_id),
        }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key = itemgetter('value'),
                            reverse = True)

# Make visualization.
my_style = LS('#333366', base_style=LCS)
my_style.title_font_size = 24
my_style.label_font_size = 14
my_style.major_label_font_size = 18

my_config = pygal.Config()
#my_config.x_label_rotation = 45
my_config.show_legend = False
#my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000

chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Top 30 Hacker News Articles Ordered by Comments\n(Scroll Over Bar for Title and Link)'
#chart.x_labels = titles
chart.x_labels = rank

chart.add('', submission_dicts)
chart.render_to_file('hacker_news_stories.svg')
