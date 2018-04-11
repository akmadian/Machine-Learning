# Machine-Learning
Machine-Learning does not use any third party ML libraries or data.

An extention of the Stock Monitor project, meant to predict whether or not the next scraped stock value will be higher, lower, or the same.

This project was completed in 28 days. It has exhibited that the more data is avaliable to the code, the more accurate it is; see the graph below.

![Accuracy over time](https://github.com/akmadian/Machine-Learning/blob/master/Graphs/Accuracy_Lines-Available.png)




___

## **Dependencies:**  
 \- lxml                    
 \- requests  
 \- twilio  
 \- bokeh  
 \- arrow  
 
 \- Node.JS



## **File Descriptions**  
**RDF.py**
 \- Gets the stock values and writes them to a CSV file.

**PRDF.py**  
 \- Generates Processed Data Files from Raw Data Files.


## **Acronyms**
RDF - Raw Data File, output of RDF.py  
PRDF - Processed Data File, output of PRDF.py  
uod - Up or Down, refers to a value and whether or not the next value is up, down, or same.  



## **Data File Structure**
\- RDF  
Entry Number - Value - Generic Timestamp - Custom Timestamp - uod state - Streak Length
    
\- PRDF
Number of rows used - Accuracy - Numbers of uods - Largest Streaks - Current Streaks - For Every uod - Value of the Stock - Timestamp - Loop time delta - Probability List - Guess List
