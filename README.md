# BloomFilters-Benchmarking
 Bloom filter is a probabilistic data structure that is similar to hash tables and allow the trade-oﬀ between false positive rate of querying data and the storage space reduction. 
 ## Filters Included in Benchmark: 
  #### 1. Standard Bloom Filter
  #### 2. Counting Bloom Filter:
    Dillinger P.C., Manolios P., Bloom Filters in Probabilistic Verification. In: Hu A.J., Martin A.K. (eds) Formal Methods in Computer-Aided Design. FMCAD 2004. Lecture Notes in Computer Science, vol 3312. Springer, Berlin, Heidelberg
  #### 3. Ternary Bloom Filter:
    Lim H, Lee J, Byun H, Yim C. Ternary Bloom Filter Replacing Counting Bloom Filter. IEEE Communications Letters. 2017; 21: 278–281.
  #### 4. Auto-Scaling Bloom Filter:
    Denis Kleyko, Abbas Rahimi, Evgeny Osipov: Autoscaling Bloom Filter: Controlling Trade-off Between True and False Positives. CoRR abs/1705.03934, 2017
  #### 5. Deletable Bloom Filter:
    C. E. Rothenberg, C. A. B. Macapuna, F. L. Verdi, and M. F. Magalhaes, “The deletable bloom filter: a new member of the bloom family”, IEEE Communications Letters, vol. 14, no. 6, pp. 557–559, 2010

### Repository Contents:
  > <i> /Experiments</i> 
  Code of experiment held for comparison between different filters + Results of the experiment.
  
  > <i> /Filters Implementation</i>
  Classes of implementation of filters.
  
  > <i> /URLShortener_App</i>
  Django Application for URL Shortening

# URL-Shortening Application:
  One of the applications that can use Bloom Filters is the URL Shortening Applications. The process is to make a call to the server, which generates a fresh URL and sends it back. A bloom filter can be used to tell if this URL has already been generated earlier, and keep generating new ones till it returns false. As the filter is in memory, this tends to be cheaper than querying a database.
<img src="https://github.com/mmaher22/BloomFilters-Benchmarking/blob/master/URLShortener_App/AppDiagram.png" width=300>  
  We have implemented a Web Application for URL shortening. You can try it in both cases of using Standard Bloom Filter or directly accessing the database and measure the time difference. Our application shows that we get faster performance using Std. Bloom Filter by around 14.6 times which will get much more by filling the database more with URLs. 
  

### Experiment:
As our application is related to URL shortening: 
  1. a dataset of 15k URLs were collected.  
  2. Unique Random Codes are generated for each URL. 
  3. Each code is converted to a unique integer using ASCII values of characters in code.
  4. 12.5k codes are going to be stored in each filter and 5k codes are going to be queried in the filter where 50% of them only are already stored in the filter to count false negatives while the other 50% are used to count false positives.

<img src="https://github.com/mmaher22/BloomFilters-Benchmarking/blob/master/Experiment/Experiment_Diagram.png" width=300>  

### Results:
The plot below shows logarithm of the number of false positives from each filter type Vs the filter size.

<img src="https://github.com/mmaher22/BloomFilters-Benchmarking/blob/master/Experiment/Results/FPs_VS_FilterSize.png" width=300>  
The plots below shows logarithm of the number of false positives and false negatives from each filter type Vs number of elements deleted from filters.

<img src="https://github.com/mmaher22/BloomFilters-Benchmarking/blob/master/Experiment/Results/FNs_VS_deletedItems.png" width=300>  
<img src="https://github.com/mmaher22/BloomFilters-Benchmarking/blob/master/Experiment/Results/FPs_VS_deletedItems.png" width=300>  
  - <b>Ternary Filter</b> has many indeterminable events which leads  to least FPR, and FNR.
  
  - <b>Standard Filter</b> has almost similar FPR like other filters and it doesn’t support deletion. So, no False negatives.
  
  - <b>AutoScaling Filter</b> has the largest FNR but by deleting more elements its FRP decreases. This can be tuned by having different decision threshold, and binarization values.
  
  - <b>Counting Filter</b> has no FNR, and also least FPR by deleting more elements from the filter. However, the filter size is the largest.
  
  - <b>Deletable Filter</b> has no false negatives and almost similar FPR as Standard Filter. The allowed deletions are smaller than other filters but it has less size than Counting Filter.

### Summary:
<img src="https://github.com/mmaher22/BloomFilters-Benchmarking/blob/master/Experiment/Results/summary.jpg" width=300>  

##### [Project Poster](https://github.com/mmaher22/BloomFilters-Benchmarking/blob/master/Project_Poster.pdf)
