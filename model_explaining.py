# For examining the dataset a BeRT model is built and used.
# A BeRT model is a Transforemer built and trained by google.
# The dataset contains 2 columns: 'data' and 'label'. The 'data' column contains the text data, while the 'label' column contains the labels for the data. The labels are binary, with 0 representing human-generated text and 1 representing AI-generated text.
# In order to classify the data an extra fully connected layer with one output is added and by using the sigmoid function on the output we get the probability of the text being human or Ai generated.
# The loss function is the BCELoss in one single class. We run the model for 20 epochs with batch size = 32.
# as we can see in the graph the model is clearly able to distinguish between human and Ai generated text.
# as the epochs go on we are able to see the overfit of the model on the training set which happens because the dataset is small.





# DATA ANALYSIS
# in order to analyze the value of datasets we used some classic techniques
# for start we used histograms to visualize the distribution of the number of words, characters, unique words, and sentences in the dataset
# we can see in the figures that there is a clear difference between the human and Ai generated text in the number of words, characters, unique words, and sentences
# when lookig into wikipedia dataset and newpaper the human generated text has wider distribution of number of words, characters, unique words and sentences than in Ai generated text
# but looking into the reddit comments dataset we can see that the Ai generated text has wider distribution of words, characters, unique words and sentences than the human generated text
# this is because the reddit comments are usually short and informal, while the wikipedia and newspaper articles are longer and more formal
# later we show n-grams of the text in the dataset. We can see that their is difference in human-generated n-grams and Ai-generated text n-grams.
# we can see that the human generated most frequent n-grams are used more than the Ai generated most frequent n-grams
# in the word cloud we can see the most frequent words in the dataset. We can see that the human generated text bigger word clouds while the Ai generated text has more diverse word clouds.



In our analysis, we utilized several classic techniques to examine and compare AI-generated and human-generated texts across different datasets. We began by visualizing the distribution of the number of words, characters, unique words, and sentences using histograms. These visualizations reveal a clear distinction between human and AI-generated texts. In the Wikipedia and newspaper datasets, human-generated texts exhibit a broader distribution in terms of the number of words, characters, unique words, and sentences compared to AI-generated texts. This indicates that human writing in these contexts tends to vary more in length and complexity. Conversely, in the Reddit comments dataset, AI-generated texts show a wider distribution than human-generated texts. This can be attributed to the informal and typically shorter nature of Reddit comments, which contrasts with the more formal and extended format of Wikipedia and newspaper articles.

Furthermore, we analyzed the most frequent n-grams (combinations of words) within the datasets. This analysis highlights significant differences between human and AI-generated n-grams. Human-generated texts tend to have n-grams that are used more frequently than those in AI-generated texts. This suggests that human writing often relies on common phrases and constructs, while AI-generated texts may exhibit a more diverse range of expressions. The n-gram analysis thus provides insights into the distinctive patterns of language use between human and AI texts.

The word clouds generated from the datasets further illustrate these differences. In word clouds, the size of a word corresponds to its frequency in the text. Human-generated texts typically result in larger word clouds, reflecting a higher repetition of certain words or phrases. On the other hand, AI-generated texts produce more diverse word clouds, indicating a broader vocabulary and varied word usage. This diversity in AI-generated word clouds underscores the algorithmic attempts to create varied and less repetitive content.

Overall, our analysis reveals that human-generated texts are more varied and nuanced, especially in formal contexts like Wikipedia and newspapers. In contrast, AI-generated texts, while potentially more diverse in vocabulary, tend to be more consistent in length and structure, particularly in informal contexts like Reddit comments. These findings highlight the intrinsic differences in content generation between humans and AI, offering valuable insights for understanding and improving AI text generation technologies.