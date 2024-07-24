
![disguisedata_tool_logo](https://github.com/dahmansphi/disguisedata/blob/main/assets/disguesdata_logo_gif.gif) 

> [!TIP]
> This project complements the __Differential Privacy with AI & ML__ project available in the [repository](https://github.com/dahmansphi/differential_privacy_with_ai_and_ml). To fully grasp the concept, make sure to read both documentations.

# About the Package
## Author's Words
Welcome to the first edition of the Disguise Data Tool official documentation. I am Deniz Dahman, Ph.D., the creator of the [BireyselValue](https://github.com/dahmansphi/bireyselvalue_v1) algorithm and the author of this package. In the following section, you will find a brief introduction to the principal idea of the __disguisedata__ tool, along with a reference to the academic publication on the method and its mathematical foundations. Before proceeding, I would like to inform you that I have conducted this work as an independent scientist without any funding or similar support. I am dedicated to continuing and seeking further improvements on the proposed method at all costs. If you wish to contribute in any way to this work, please find further details in the contributing section.
  
## Contributing 

If you wish to support the creator of this project, you might want to explore possible ways on:

> `Thank you for your willingness to contribute in any way possible. You can check links below for more information on how to get involved.` :

1. view options to subscribe on [Dahman's Phi Services Website](https://dahmansphi.com/subscriptions/)
2. subscribe to this channel [Dahman's Phi Services](https://www.youtube.com/@dahmansphi)     
3. you can support on [patreon](https://patreon.com/user?u=118924481) 


If you prefer *any other way of contribution*, please feel free to contact me directly on [contact](https://dahmansphi.com/contact/). 

*Thank you*

# Introduction

## History and Purpose of Synthetic Data
 
The concept of synthetic data has roots in scientific modeling and simulations, dating back to the early 20th century. For instance, audio and voice synthesis research began in the 1930s. The development of software synthesizers in the 1970s marked a significant advancement in creating synthetic data. In 1993, the idea of fully synthetic data for privacy-preserving statistical analysis was introduced to the research community. Today, synthetic data is extensively used in various fields, including healthcare, finance, and defense, to train AI models and conduct simulations. More importantly, synthetic data continues to evolve, offering innovative solutions to data scarcity, privacy, and bias challenges in the AI and machine learning landscape.

Synthetic data serves multiple purposes. It enhances AI models, safeguards sensitive information, reduces bias, and offers an alternative when real-world data is scarce or unavailable: 
- [x] __Training AI Models__: Synthetic data is widely used to train machine learning models, especially when real-world data is scarce or sensitive. It helps in creating diverse datasets that improve model accuracy and robustness, 
- [x] **Privacy Protection:** By using synthetic data, organizations can avoid privacy issues associated with real data, such as patient information in healthcare, 
- [x] **Testing and Validation:** Synthetic data allows for extensive testing and validation of systems without the need for real data, which might be difficult to obtain or use due to privacy concerns.  
- [x]  **Testing and Validation:** Synthetic data allows for extensive testing and validation of systems without the need for real data, which might be difficult to obtain or use due to privacy concerns.
- [x] **Bias Reduction:** It helps in reducing biases in datasets, ensuring that AI models are trained on balanced and representative data.


## disguisedata __version__1.0

![disguisedata_logo_png](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/disguesdata_logo_png.png) 

There are numerous tools available to generate synthetic data using various techniques. This is where I introduce the __disguisedata__ tool. This tool helps to disguise data based on a mathematical foundational concept. In particular, it relies on two important indicators in the original dataset: 

1. __The norm__: Initially, it captures the general norm of the dataset, involving every entry in the set. This norm is then used to scale the dataset to a range of values. It is considered the **secret key** used later to convert the synthetic data into the same scale as the original.

2. __The Geometrical Shape of a Data Point__: The second crucial indicator for the **disguisedata** method is the geometric shape of a data point in the original dataset. Each point can be represented as a right-angled triangle, which can be scaled up or down. Every point along the hypotenuse line of the triangle represents a potential replica of the original point. The accompanying figure demonstrates this concept.

![triangle_png](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/fig4.png) 


> [!IMPORTANT]
> **This tool demonstrates the proposed method solely for educational purposes. The author provides no warranty of any kind, including the warranty of design, merchantability, and fitness for a particular purpose**. 

# Installation 
> [!TIP]
> The simulation using __disguisedata__ was conducted on three datasets, which are referenced in the section below. 

## Data Availability
1. Breast Cancer Wisconsin (Diagnostic) Dataset available in [UCI Machine Learning Repository] at https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic , reference (Street 1993)
2. The Dry Bean Dataset available in [UCI Machine Learning Repository] at https://doi.org/10.24432/C50S4B , reference (Koklu 2020) 

## Install disguisedata

to install the package all what you have to do:
```
pip install disguisedata==1.0.4
```
You should then be able to use the package. It might be a good idea to confirm the installation to ensure everything is set up correctly.

```
pip show disguisedata
```
The result then shall be as:

```
Name: disguisedata
Version: 1.0.4
Summary: A tiny tool for generating synthetic data from the original one
Home-page: https://github.com/dahmansphi/disguisedata
Author: Deniz Dahman's, Ph.D.
Author-email: dahmansphi@gmail.com
```
> [!IMPORTANT]
> **Sometimes, the `seaborn` library isn't installed during setup. If that's the case, you'll need to install it manually.** 


## Employ the disguisedata -**Conditions**

> [!IMPORTANT]
> It's mandatory to provide the instance of the class with the **NumPy** array of the original dataset, which does not include the **y** feature or the target variable.

## Detour in the disguisedata package- Build-in
Once your installation is complete and all conditions are met, you may want to explore the built-in functions of the `disguisedata` package to understand each one. Essentially, you can create an instance from the `disguisedata` class as follows:

```
from disguisedata.disguisedata import Disguisedata
inst = Disguisedata()
```
Now this instance offers you access to the built-in functions that you need. Here is a screenshot:

![Screenshot of build-in functions of the disguisedata tool.](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/screenshoot.png)

Once you have the **disguisedata** instance, follow these steps to obtain the new disguised data:

### Control and Get the data format:

The first function you want to employ is `feedDs` using: 
```
data = inst.feedDs(ds=ds)
```
This function takes one argument, which is the NumPy dataset, and it controls the conditions and returns a formatted, scaled dataset that is ready for the action of disguise.

### Acquire two distinct variants of disguised synthetic data.:

The function `discover_effect` allows you to explore how the disguised data differs from the original data. It is called using: 
```
setData = inst.discover_effect(data=data, effect=effect)
``` 

This function takes **two arguments**: the first is the formatted dataset returned from the previous function, The second parameter is the effect value, denoted as ρ; this value should range from 0 to 0.9. For a detailed understanding of its function, one may consult the relevant academic paper. 

> [!IMPORTANT]
> The function should return two disguised synthetic datasets; one contains values that are to the left of the original, and the other contains values to the right. You can use the `setData[0]` or `setData[1]` variable to examine each one.

> [!TIP]
> It's important to observe how the screenshot shows the location of the disguised data from the original dataset. The report then illustrates how the values are altered according to the parameter adjustments. Additionally, it presents the differences in the mean and correlation between the original and disguised data.

Here are some outputs from the function using three different values of ρ (0.2; 0.5; and 0.9):


### at ρ = 0.2
![Screenshot of result1.](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/02fig1.png)

![Screenshot of result2.](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/02fig2.png)

![Screenshot of result3.](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/02r1.png)


### at ρ = 0.5
![Screenshot of result1.](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/05fig1.png)

![Screenshot of result2.](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/05fig2.png)

![Screenshot of result3.](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/05r1.png)

### at ρ = 0.9
![Screenshot of result1.](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/08fig1.png)

![Screenshot of result2.](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/08fig2.png)

![Screenshot of result3.](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/08r1.png)

## Conclusion on installation and employment of the method 
It is possible to test the results returned based on the proposed method. I used two predictive methods on the original and the disguised dataset to observe the effect on accuracy. The conclusion is that there are almost identical results between both predictions, which implies that the proposed method is effective in generating realistic disguised data that maintains privacy.

__at ρ = 0.2__

![Screenshot of result6.](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/02r2.png)

__at ρ = 0.5__

![Screenshot of result6.](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/05r2.png)

__at ρ = 0.8__

![Screenshot of result6.](https://raw.githubusercontent.com/dahmansphi/disguisedata/main/assets/08r2.png)


# Reference

please follow up on the [publication](https://dahmansphi.com/publications/) in the website to find the academic [published paper](https://dahmansphi.com)
 
