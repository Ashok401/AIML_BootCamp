### iPhone reviews sentiment and aspect-based sentiment analysis


### This project comprises four subtasks:

### Subtask 1: Sentiment Analysis 

- Data Source: iPhone reviews from Amazon India, downloaded from Kaggle.
- Data Cleaning: Data preprocessing and cleaning.
- Deep Dive into Major Issues Reported in Phone Reviews: Analyzing and categorizing significant issues mentioned in the reviews.
- Observations:
  - The 128GB iPhone, in a blue color, sold the highest units among all iPhone models.
  - Most customers were satisfied with the camera quality but disappointed with the battery drain.

### Subtask 2: Experiment with Various AI Models 

- Experiment with different LLMs using data from “top100_wordcounts” (top 100 reviews with meaningful review comments) to determine which model yields superior results.
- Observations:
  - All LLMs performed well, but Claude Sonnet 4, created by Anthropic, outperformed the others.
  - Based on my experience with this data, Claude correctly identified the top 10 issues in the correct order.

Note: This observation was made on December 19, 2025.

### Subtask 3: Aspect-based Sentiment Analysis

- Explore the possibility of replacing expensive and slow LLMs with smaller, custom models. These models should be simple, scalable, and maintain acceptable quality.
- Scaling the model to work on datasets containing 500 and 1000 reviews, which are currently in the top 100 reviews.
- Observation: By employing Knowledge Distillation, we leverage an LLM (Teacher) to train a set of Logistic Regression “Expert” models (Students). These models achieve an impressive 85%+ agreement with the LLM while incurring a 99.9% lower cost.

### Subtask 4: Model Deployment using AWS

- Deploy the model on AWS SageMaker 

### Additional notes:
    1. - Input data: iPhone reviews downloaded from Kaggle (https://www.kaggle.com/datasets/mrmars1010/iphone-customer-reviews-nlp)
    2. - Data cleaning and preprocessing: To enhance prediction accuracy.
    3. - Sentiment analysis: To delve into the major issues reported in the reviews.
    4. - ASBA: To explore the possibility of replacing expensive and slow LLMs with smaller, custom models. These models should be simple, scalable, and maintain acceptable quality.
    5. Model deployment: We’ll use AWS SageMaker. We’ll monitor data drift and performance and retrain the model every six months once we have enough new reviews. We’ll share the deep insights with business development teams so they can take necessary actions to improve customer satisfaction.
