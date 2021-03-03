# BinningValueProblem
Suppose that we are given a set of bins, 
![formula](https://render.githubusercontent.com/render/math?math=B%20=%20\{1,%202,%20\ldots,%20n\}). 

Each of which has been assigned a value, given by the set ![formula](https://render.githubusercontent.com/render/math?math=V%20=%20\{v_1,%20v_2,%20\ldots,%20v_n\}) where ![formula](https://render.githubusercontent.com/render/math?math=v_i) is the value assigned to bin ![formula](https://render.githubusercontent.com/render/math?math=i).

Next, suppose we are given an array of floating point numbers ![formula](https://render.githubusercontent.com/render/math?math=F%20=%20\{f_1,%20,f_2,%20,\ldots,%20f_m\}) and an objective function ![formula](https://render.githubusercontent.com/render/math?math=O). The problem which we wish to solve is to place the values of ![formula](https://render.githubusercontent.com/render/math?math=F) into each of the bins, so as to minimize the average Objective function across the difference between the sum of the values within each bin and the value assigned to each bin. 

If we add an index to the floating point numbers such that ![formula](https://render.githubusercontent.com/render/math?math=f_i) becomes ![formula](https://render.githubusercontent.com/render/math?math=f_{ij}) where ![formula](https://render.githubusercontent.com/render/math?math=i%20%20\epsilon%20\{1,%202,%20\ldots,%20m\}) and 
![formula](https://render.githubusercontent.com/render/math?math=j%20%20\epsilon%20B) where j indicates which bin the floating point value has been place in, our goal can be expressed as follows:

We wish to minimize the expression:
![formula](https://render.githubusercontent.com/render/math?math=\frac{1}{n}\sum_{j=1}^{n}O((\sum_{i=1}^{m}f_{ij})-v_j))

This python program seeks to solve this problem using a divide-and-conquer algorithm to create a recursive tree and by pruning sub-optimal branches of said tree.
