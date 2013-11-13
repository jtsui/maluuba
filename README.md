i256 - information extraction assignment
Jeff Tsui
Shubham Goel

Repository:
https://github.com/jtsui/maluuba

What We Did:
For this assignment, we chose suggestion 2 in the information extraction option to explore the Maluuba API, create an extensive test set, and evaluate its precision and recall. 

Maluuba has two API's: the interpret API and the normalize API as outlined on their developer page http://dev.maluuba.com/. We chose to focus on the interpret API which accepts unstructured text and interprets information about them in the following format: category, action, and entities. The category tag is one of Maluuba's supported categories and the action is a more specific type of each category. For example, the category BUSINESS has actions of BUSINESS_SEARCH and BUSINESS_RESERVATION. The entities cover a broader range of text surrounding the action. For example, the text "remind me about my dentist appointment tomorrow at 2" gets tomorrow's date based on the time of the request, and appends the time. We chose to focus on evaluating the category and action labels of maluuba since the entities are more free form and would be difficult to evaluate. Creating a test set with exactly tagged entities in Maluuba's output format would be extremely time intensive so we decided to remove this from the scope of this project.

Next we created an extensive test set covering all of Maluuba's 22 categories and 69 actions. The breakdown of the number of samples for each (category, action) pair is given in the output. Maluuba clearly specifies the interpret API works best on short (<10 word) sentences so we set out to create a test set of phrases common to the mobile space that fit into each category and action. Our complete test set of 300 sentences can be found in test_all.csv.

Finally we wrote code to call the Maluuba API and tag each sentence. We compute statistics on the false negative, false positive, true negative, and true positive rates as well as recall and precision for each action and each category. More detail on the code is in the next section.

Code:
The code has two main functions as seen in main: tag() and evaluate(). 

Tag() takes strings of input and output file names as argugments. The input file is the test set that we developed in the format of a csv with headers sentence, category, and action. Tag() iterates through each row in the csv and calls the maluuba API to get the interpreted action and category. We create a results list that takes the original row in each input file and appends the actual labels that we get from the Maluuba API. The results are written to a output csv.

Evaluate takes the filename of the resulting csv output from tag() which has headers sentence, category, retrieved category, action, retrieved action. It creates slices of the results in the form of (actual tag, retrieved tag) and passes it to the get_precision_recall() function which outputs the false negative, false positive, true negative, and true positive rates as well as recall and precision. Evalute() prints the statistics for all slices of individual and aggregate categories and actions. The result of evalute() is copied below.

Division of work:
We met in person once and split up the work pretty evenly.
Jeff - Wrote final evaluation code, explored the API, added test cases
Shubham - Created most of the test cases, wrote initial evaluation code, explored the API

Evaluation results:
The recall is always 100% because Maluuba's API always return category KNOWLEDGE when it is unable to label it with a more specific category. The results below show the output of running evaluate() in our code. It shows the breakdown of false negative, false positive, true negative, and true positive rates as well as recall and precision for each action and each category.

Summary for 300 samples
-----------------------
                              tp	fp	fn	tn	recall	precision	samples
ALARM                         1.00	0.00	0.00	0.00	1.00	1.000000	6
APPLICATION                   0.81	0.19	0.00	0.00	1.00	0.809524	21
BUSINESS                      0.89	0.11	0.00	0.00	1.00	0.891304	46
CALENDAR                      1.00	0.00	0.00	0.00	1.00	1.000000	5
CALL                          0.97	0.03	0.00	0.00	1.00	0.970588	34
CONTACT                       0.92	0.08	0.00	0.00	1.00	0.916667	12
EMAIL                         1.00	0.00	0.00	0.00	1.00	1.000000	2
ENTERTAINMENT                 1.00	0.00	0.00	0.00	1.00	1.000000	5
HELP                          1.00	0.00	0.00	0.00	1.00	1.000000	2
KNOWLEDGE                     0.78	0.22	0.00	0.00	1.00	0.777778	18
MUSIC                         0.94	0.06	0.00	0.00	1.00	0.941176	17
NAVIGATION                    0.82	0.18	0.00	0.00	1.00	0.823529	17
REMINDER                      1.00	0.00	0.00	0.00	1.00	1.000000	2
SEARCH                        1.00	0.00	0.00	0.00	1.00	1.000000	8
SOCIAL                        0.77	0.23	0.00	0.00	1.00	0.767442	43
SPORTS                        0.48	0.52	0.00	0.00	1.00	0.478261	23
STOPWATCH                     1.00	0.00	0.00	0.00	1.00	1.000000	3
TEXT                          1.00	0.00	0.00	0.00	1.00	1.000000	9
TIMER                         1.00	0.00	0.00	0.00	1.00	1.000000	4
TRANSIT                       1.00	0.00	0.00	0.00	1.00	1.000000	3
TRAVEL                        0.75	0.25	0.00	0.00	1.00	0.750000	16
WEATHER                       1.00	0.00	0.00	0.00	1.00	1.000000	4
---------------------------------------------------------------
category overall              0.85	0.15	0.00	0.00	1.00	0.850000

ALARM_CANCEL                  1.00	0.00	0.00	0.00	1.00	1.000000	1
ALARM_CANCEL_ALL_ALARMS       1.00	0.00	0.00	0.00	1.00	1.000000	1
ALARM_MODIFY                  1.00	0.00	0.00	0.00	1.00	1.000000	1
ALARM_SEARCH                  1.00	0.00	0.00	0.00	1.00	1.000000	1
ALARM_SET                     1.00	0.00	0.00	0.00	1.00	1.000000	1
ALARM_SET_RECURRING           1.00	0.00	0.00	0.00	1.00	1.000000	1
APPLICATION_LAUNCH            0.76	0.24	0.00	0.00	1.00	0.761905	21
BUSINESS_RESERVATION          0.75	0.25	0.00	0.00	1.00	0.750000	12
BUSINESS_SEARCH               0.94	0.06	0.00	0.00	1.00	0.941176	34
CALENDAR_AVAILABILITY         1.00	0.00	0.00	0.00	1.00	1.000000	1
CALENDAR_CREATE_EVENT         1.00	0.00	0.00	0.00	1.00	1.000000	1
CALENDAR_MODIFY_EVENT         1.00	0.00	0.00	0.00	1.00	1.000000	1
CALENDAR_REMOVE_EVENT         1.00	0.00	0.00	0.00	1.00	1.000000	1
CALENDAR_SEARCH               1.00	0.00	0.00	0.00	1.00	1.000000	1
CALL_ACCEPT_INCOMING          1.00	0.00	0.00	0.00	1.00	1.000000	4
CALL_CHECK_MISSED             1.00	0.00	0.00	0.00	1.00	1.000000	10
CALL_DIAL                     0.94	0.06	0.00	0.00	1.00	0.937500	16
CALL_RESPOND_MISSED           1.00	0.00	0.00	0.00	1.00	1.000000	4
CONTACT_ADD                   1.00	0.00	0.00	0.00	1.00	1.000000	6
CONTACT_SEARCH                0.80	0.20	0.00	0.00	1.00	0.800000	5
CONTACT_SET_ALIAS             1.00	0.00	0.00	0.00	1.00	1.000000	1
EMAIL_DISPLAY                 1.00	0.00	0.00	0.00	1.00	1.000000	1
EMAIL_SEND                    1.00	0.00	0.00	0.00	1.00	1.000000	1
ENTERTAINMENT_AMBIGUOUS       1.00	0.00	0.00	0.00	1.00	1.000000	1
ENTERTAINMENT_EVENT           1.00	0.00	0.00	0.00	1.00	1.000000	2
ENTERTAINMENT_MOVIE           1.00	0.00	0.00	0.00	1.00	1.000000	2
HELP_HELP                     1.00	0.00	0.00	0.00	1.00	1.000000	2
KNOWLEDGE_SEARCH              0.78	0.22	0.00	0.00	1.00	0.777778	18
MUSIC_PAUSE                   1.00	0.00	0.00	0.00	1.00	1.000000	1
MUSIC_PLAY                    0.94	0.06	0.00	0.00	1.00	0.937500	16
NAVIGATION_DIRECTIONS         0.91	0.09	0.00	0.00	1.00	0.909091	11
NAVIGATION_WHERE_AM_I         0.67	0.33	0.00	0.00	1.00	0.666667	6
REMINDER_SEARCH               1.00	0.00	0.00	0.00	1.00	1.000000	1
REMINDER_SET                  1.00	0.00	0.00	0.00	1.00	1.000000	1
SEARCH_AMAZON                 1.00	0.00	0.00	0.00	1.00	1.000000	2
SEARCH_BING                   1.00	0.00	0.00	0.00	1.00	1.000000	1
SEARCH_DEFAULT                1.00	0.00	0.00	0.00	1.00	1.000000	1
SEARCH_EBAY                   1.00	0.00	0.00	0.00	1.00	1.000000	1
SEARCH_GOOGLE                 1.00	0.00	0.00	0.00	1.00	1.000000	1
SEARCH_RECIPES                1.00	0.00	0.00	0.00	1.00	1.000000	1
SEARCH_WIKIPEDIA              1.00	0.00	0.00	0.00	1.00	1.000000	1
SOCIAL_FACEBOOK_SEND_MESSAGE  1.00	0.00	0.00	0.00	1.00	1.000000	5
SOCIAL_FACEBOOK_SHOW_NEWSFEED 0.59	0.41	0.00	0.00	1.00	0.588235	17
SOCIAL_FACEBOOK_SHOW_PHOTOS   0.60	0.40	0.00	0.00	1.00	0.600000	5
SOCIAL_FACEBOOK_SHOW_WALL     1.00	0.00	0.00	0.00	1.00	1.000000	2
SOCIAL_FACEBOOK_WRITE_ON_WALL 1.00	0.00	0.00	0.00	1.00	1.000000	2
SOCIAL_FOURSQUARE_CHECK_IN    1.00	0.00	0.00	0.00	1.00	1.000000	2
SOCIAL_FOURSQUARE_SHOW_CHECKINS0.50	0.50	0.00	0.00	1.00	0.500000	2
SOCIAL_TWITTER_SHOW_FOLLOWER  1.00	0.00	0.00	0.00	1.00	1.000000	3
SOCIAL_TWITTER_SHOW_TRENDING  0.50	0.50	0.00	0.00	1.00	0.500000	2
SOCIAL_TWITTER_TWEET          1.00	0.00	0.00	0.00	1.00	1.000000	3
SPORTS_MISC                   0.48	0.52	0.00	0.00	1.00	0.478261	23
STOPWATCH_DISPLAY             1.00	0.00	0.00	0.00	1.00	1.000000	1
STOPWATCH_START               1.00	0.00	0.00	0.00	1.00	1.000000	1
STOPWATCH_STOP                1.00	0.00	0.00	0.00	1.00	1.000000	1
TEXT_DISPLAY                  1.00	0.00	0.00	0.00	1.00	1.000000	1
TEXT_SEND                     1.00	0.00	0.00	0.00	1.00	1.000000	8
TIMER_CANCEL                  1.00	0.00	0.00	0.00	1.00	1.000000	1
TIMER_DISPLAY                 1.00	0.00	0.00	0.00	1.00	1.000000	1
TIMER_PAUSE                   1.00	0.00	0.00	0.00	1.00	1.000000	1
TIMER_START                   1.00	0.00	0.00	0.00	1.00	1.000000	1
TRANSIT_NEARBY_STOPS          1.00	0.00	0.00	0.00	1.00	1.000000	1
TRANSIT_NEXT_BUS              1.00	0.00	0.00	0.00	1.00	1.000000	1
TRANSIT_SCHEDULE              1.00	0.00	0.00	0.00	1.00	1.000000	1
TRAVEL_FLIGHT                 0.75	0.25	0.00	0.00	1.00	0.750000	16
WEATHER_DETAILS               1.00	0.00	0.00	0.00	1.00	1.000000	1
WEATHER_STATUS                1.00	0.00	0.00	0.00	1.00	1.000000	1
WEATHER_SUNRISE               1.00	0.00	0.00	0.00	1.00	1.000000	1
WEATHER_SUNSET                1.00	0.00	0.00	0.00	1.00	1.000000	1
---------------------------------------------------------------
action overall                0.84	0.16	0.00	0.00	1.00	0.843333
