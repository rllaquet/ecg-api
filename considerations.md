# Considerations

## Summary

I'll just rant a bit here about why I made some decisions and go a bit over how I 
structured the code, enjoy!

## Code structure

I've never worked on big projects using FastAPI so there might be other ways to 
structure files, I made sure to have some separation of concerns:
- main.py as the entry point
- dependencies.py for, well, dependencies. For now, it's just authentication checks 
  and the DB, in case of having more there could be a folder with different files 
  for different types of dependencies.
- utils, for utility functions
- schemas, for pydantic models of input and output data, for validation and nice 
  out-of-the-box documentation, more can be done to have even better docs.
- models, for the data models, which are the ones that interact with the database. 
  For now, it's just functions for the needed operations
- routers, for the API endpoints, which are the ones that interact with the models 
  and the schemas.

## Data storage

In terms of database, I ended up picking MongoDB as I feel NoSQL databases are more 
appropriate for this kind of data. Reasons being:
- We probably wouldn't fully take advantage of a relational model, as we're not 
  going to be doing queries with complex joins. (at least as far as I can tell)
- We might want to expand the data model with more statistics in the future, and 
  NoSQL databases are more flexible for that.
- If we want to have our service running on a cloud provider such as AWS, we could 
  easily translate this to a DynamoDB table to take advantage of the efficiency
  and scalability
- Scales better horizontally, given huge amounts of data, things like computing 
  stats on big chunks of data wouldn't quickly become a bottleneck.

## Data processing

The API will be responsible for processing the zero crossings metric, and one of the 
main questions regarding that was where to compute this value. Given that 
ECG signals in the DB are not prone to updates and that computing the metric is a 
fast process, I considered doing that before storing the data in the DB.

If signals were prone to updates, or the algorithm was dependent on dynamic 
parameters, I would've considered computing it when retrieving the data and caching it

And if metrics were introduced down the line with a much higher computational cost,  
I would consider delegating the computation to a different service and having a state to 
control when the ECG is ready to be fetched.

As for the algorithm itself, I ended up using numpy. If we knew that the size of the 
signals we'll be receiving is small, and that it's going to be the only signal  
processing we're going to need, a pure python solution could've been enough. But 
given the nature of the API it's likely that we'll encounter larger signals and  
more complex signal processing in the future, so I considered numpy to be a good choice.

I did a first implementation using only pure python, and then I did a bit more 
research to make sure the solution is efficient enough. Here is the initial pure python
implementation, which is pretty similar to the numpy alternative:

```python
def zero_crossings(signal: list[int]):
    # Remove zeros to avoid detecting them as zero crossings
    non_zero_signal = [x for x in signal if x != 0]

    # Count the number of zero crossings by counting sign changes
    crossings_count = 0
    for i in range(len(non_zero_signal) - 1):
        if non_zero_signal[i] * non_zero_signal[i + 1] < 0:
            crossings_count += 1

    return crossings_count
```
