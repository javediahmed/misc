#!/usr/bin/env python
# coding: utf-8

# # Spam Classification with PySpark
# 
# Let's use PySpark to classify SMS texts as either spam or ham. 

# In[ ]:


import pyspark
import string
import re


# Before we begin, we need to download the stopwords for nltk which we will be using later.

# In[ ]:


import nltk
nltk.download("stopwords")


# First we begin by creating the spark session.

# In[ ]:


spark = pyspark.sql.SparkSession.builder.getOrCreate()


# ## Import the data
# 
# Next we load the train and test spam email data.

# In[ ]:


get_ipython().system(' head -n 4 data/spam_train.txt')


# In[ ]:


# Import the data
train = spark.read.csv('data/spam_train.txt', 
                       sep='\t',
                       header=True,
                       inferSchema=True)

test = spark.read.csv('data/spam_test.txt', 
                       sep='\t',
                       header=True,
                       inferSchema=True)

train.show(3)


# ## Preprocess text
# 
# To begin, the text will be processed to remove punctuation and alphanumerical words. We will slso perform stemming. These tasks don't have a PySpark-specific implementation, so we will be using a standard Python function that will be converted to one that acts on PySpark dataframes. To do this, we will use something called a "user defined function" (UDF) in PySpark.
# 
# Note that stopwords were not removed here, although they could have been. Instead, we will remove them later using a PySpark function.

# In[ ]:


from nltk.stem.snowball import SnowballStemmer
from pyspark.sql.functions import udf

# Create the function that performs the text conversion

sn = SnowballStemmer('english')

def clean_text(text, sn=sn):
 
    # Regular expression substitutions
    punc_re = re.compile('[%s]' % re.escape(string.punctuation + '£'))
    text = punc_re.sub(' ', ' '+text.lower()+' ') # Pad with spaces for easier stopword removal

    # Remove numbers
    num_re = re.compile('(\\d+)')
    text = num_re.sub(' ', text)
    
    # Remove alphanumerical words
    alpha_num_re = re.compile("^[a-z0-9_.]+$")
    text = alpha_num_re.sub(' ', text)
    
    # Stemming
    text = sn.stem(text)
    
    # Regex for multiple spaces
    spaces_re = re.compile('\s+')
    text = spaces_re.sub(' ', text.strip())

    return text

# Convert the function to a UDF
clean_text = udf(clean_text)


# Convert the text in the train and test data by applying the UDF to each row of text.

# In[ ]:


train = train.withColumn('text', clean_text(train['text']))
test  = test.withColumn('text', clean_text(test['text']))

train.show(4)


# Next, we need to convert the ham/spam label column (what we are predicting) into a numerical index. We will use PySpark's `StringIndexer` for this. It works much like Scikit-learn's `LabelEncoder`.

# In[ ]:


from pyspark.ml.feature import StringIndexer

# Convert the column labels
si = StringIndexer(inputCol='label', outputCol='label_float')
si_model = si.fit(train)

train = si_model.transform(train)
test = si_model.transform(test)

# Drop the string column and rename the numerical one to 'label'
train = train.drop('label')
train = train.withColumnRenamed('label_float', 'label')

test = test.drop('label')
test = test.withColumnRenamed('label_float', 'label')

train.show(4)


# ## Feature encoding and model building
# 
# Now we will train some models and compare the results! We will be using several different feature engineering methods for natural language processing. Naive Bayes will be used to predict if the message is spam or ham.
# 
# We will be using PySpark's [`Pipeline`](https://spark.apache.org/docs/latest/ml-pipeline.html) to create processing pipelines. We will also be using [`ParamGridBuilder`](https://spark.apache.org/docs/latest/api/python/pyspark.ml.html#pyspark.ml.tuning.ParamGridBuilder) to create a grid of parameters to search during cross-validation (done later).
# 
# Create four pipelines with the following features:
# 
#     1. TF-IDF and Naive Bayes
#     2. CountVectorizer and Naive Bayes
#     3. BiGrams, CountVectorizer, and Naive Bayes
#     4. Word2Vec, CountVectorizer, and Naive Bayes
#     
# Note that the output of PySpark's Word2Vec model already has vector averaging performed, so we don't need to do so in this case.
# 
# First, let's do some pre-processing on the data.

# In[ ]:


from nltk.corpus import stopwords
from pyspark.ml.feature import Tokenizer, StopWordsRemover, MinMaxScaler, VectorAssembler
from pyspark.ml.feature import HashingTF, IDF, CountVectorizer, NGram, Word2Vec
from pyspark.ml.classification import NaiveBayes
from pyspark.ml import Pipeline
from pyspark.ml.tuning import ParamGridBuilder

####### More Preprocessing #######
# These steps are done for all pipelines

# Tokenize (split) words
tk = Tokenizer(inputCol="text", outputCol='tokens')

# The stopword removal function
sw = StopWordsRemover(inputCol=tk.getOutputCol(),
                             outputCol='stopwords')
sw = sw.setStopWords(stopwords.words('english'))


# Now let's create the first pipeline with TF-IDF and Naive Bayes.

# In[ ]:


####### The first ML pipeline #######
# TF-IDF and Naive Bayes

htf = HashingTF(inputCol=sw.getOutputCol(),
                      outputCol='hashing')
idf = IDF(inputCol=htf.getOutputCol(),
          outputCol='idf')

va = VectorAssembler(inputCols=[idf.getOutputCol()], outputCol='features')

nb = NaiveBayes()

# Assemble the pipeline
pipeline1 = Pipeline(stages=[tk, sw, htf, idf, va, nb])

# Setup parameters to optimize
paramgrid1 = (ParamGridBuilder().addGrid(htf.numFeatures, [20])
                                .addGrid(idf.minDocFreq, [1])              
                                .addGrid(nb.smoothing, [0.0, 1.0])
                                .build())


# Here is the second pipeline with Count Vectorizer and Naive Bayes.

# In[ ]:


####### The second ML pipeline #######
# CountVectorizer and Naive Bayes
cntv = CountVectorizer(inputCol=sw.getOutputCol(),
                       outputCol='cntv')

va = VectorAssembler(inputCols=[cntv.getOutputCol()], outputCol='features')

# Assemble the pipeline and set parameters to optimize in gridsearch
pipeline2 = Pipeline(stages=[tk, sw, cntv, va, nb])

# Setup parameters to optimize
paramgrid2 = (ParamGridBuilder().addGrid(cntv.minTF, [1.0, 3.0])
                                .addGrid(cntv.minDF, [1.0])              
                                .addGrid(nb.smoothing, [0.0, 1.0])
                                .build())


# Now let's add bigrams into the mix.

# In[ ]:


####### The third ML pipeline #######
# BiGrams, CountVectorizer, and Naive Bayes

ng2 = NGram(n=2, inputCol=sw.getOutputCol(),
                  outputCol='ngrams2')

# Need separate count vectorizer for single words and bigrams
cntv1 = CountVectorizer(inputCol=sw.getOutputCol(),
                       outputCol='cntv1')
cntv2 = CountVectorizer(inputCol=ng2.getOutputCol(),
                       outputCol='cntv2')

va = VectorAssembler(inputCols=[cntv1.getOutputCol(),
                                cntv2.getOutputCol()], outputCol='features')

# Assemble the pipeline and set parameters to optimize in gridsearch
pipeline3 = Pipeline(stages=[tk, sw, cntv1, ng2, cntv2, va, nb])

# Setup parameters to optimize
paramgrid3 = (ParamGridBuilder().addGrid(cntv1.minTF, [1.0])
                                .addGrid(cntv1.minDF, [1.0])
                                .addGrid(cntv2.minTF, [1.0])
                                .addGrid(cntv2.minDF, [1.0, 3.0])
                                .addGrid(nb.smoothing, [0.0, 1.0])
                                .build())


# Finally add word2vec as well.

# In[ ]:


####### The fourth ML pipeline #######
# CountVectorizer, Word2Vec, MinMaxScaler, and Naive Bayes

wv = Word2Vec(inputCol=tk.getOutputCol(),
              outputCol='w2v')

# Naive Bayes requires positive features and 
# Word2Vec features are sometimes negative
# So the values are rescaled to between [0.0, 1.0]
mm = MinMaxScaler(inputCol=wv.getOutputCol(),
                  outputCol='mm')

cntv = CountVectorizer(inputCol=sw.getOutputCol(),
                       outputCol='cntv')

va = VectorAssembler(inputCols=[mm.getOutputCol(), 
                                cntv.getOutputCol()], outputCol='features')

# Assemble the pipeline and set parameters to optimize in gridsearch
pipeline4 = Pipeline(stages=[tk, sw, wv, mm, cntv, va, nb])

# Setup parameters to optimize
paramgrid4 = (ParamGridBuilder().addGrid(cntv.minTF, [1.0])
                                .addGrid(cntv.minDF, [1.0, 3.0])              
                                .addGrid(nb.smoothing, [0.0, 1.0])
                                .build())


# Finally, we train each of these models using cross validation and output the one with the best f1 score. 

# In[ ]:


from pyspark.ml.tuning import CrossValidator
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluator = MulticlassClassificationEvaluator(predictionCol='prediction', 
                                              labelCol='label', 
                                              metricName='f1')

# List to store the fit model in
cvModel_list = list()

for lab,pipeline,paramgrid in zip(['TF-IDF', 'CountVectorizer',
                                   'CountVectorizer+BiGrams', 'Word2Vec'],
                                  [pipeline1, pipeline2, pipeline3, pipeline4],
                                  [paramgrid1, paramgrid2, paramgrid3, paramgrid4]):

    
    # Columns to remove in between fits
    drop_cols = [x for x in test.columns if x not in ['text', 'label']]

    for col in drop_cols:
        train = train.drop(col)
        test  = test.drop(col)
    
    cv = CrossValidator(estimator=pipeline, 
                        estimatorParamMaps=paramgrid, 
                        evaluator=evaluator, 
                        numFolds=4)
    
    cvModel = cv.fit(train)
    test = cvModel.transform(test)
    print(lab, evaluator.evaluate(test))
    
    cvModel_list.append(cvModel)
    


# If we wanted to use the best model to make other predictions, we could extract and serialize it.

# In[ ]:


best_spam_model = cvModel_list[2].bestModel

model_output_name = 'spam_model_pipeline_crossval'

# models will not overwrite existing ones of the same name
import shutil, os
if os.path.exists(model_output_name):
    shutil.rmtree(model_output_name)

best_spam_model.save(model_output_name)

get_ipython().system(' ls {model_output_name}')


# In[ ]:




