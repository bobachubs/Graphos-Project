Graphos


Graphos is a general purpose data visualizer that allows the user to input a csv file (or choose from the predefined data streams) and display the data through different graphical/visual options (scatter, bar, histogram, grouped bar chart animation).


[how to run the project] 


The user should run the main file, app.py. The rest of the 12 python source files are in the appropriate relative locations.

There is 1 folder called [images] which contains all the image assets.

There is 1 csv file called [nba_stats.csv] which contains the data needed to run the built-in sample NBA dataset.

Graphos supports visualizing live-streamed Twitter data, but the user must supply their own Twitter developer keys or the application page will display a warning. To keep the creator’s keys safe, the application reads the keys in as environment variables as documented in the twitter_word_count.py source file.


[Libraries]


This project uses Tweepy, Wordcloud, and numpy as external modules. Tweepy is a client for the Twitter APIs and Graphos uses it for real-time streaming of tweets. The Wordcloud module is used to generate images of word clouds to visualize trending Twitter hashtags. Numpy is used to create a mask to shape the word cloud. All these modules can be installed using pip - the python package installer. Installing Wordcloud using pip requires gcc, which is part of macOS command line tools.


The other external modules, such as PIL, are assumed to be part of cmu_graphics.py.


[Shortcut commands]


The application uses the space key to start and pause animated visualizations.
- Bar Chart Groups
- Twitter Word Clouds