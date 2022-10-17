# Hack yourself!

## NeuroTechX & Timeflux @ 42

[Timeflux](https://timeflux.io) is an open-source Python framework for acquiring and processing biosignals in real-time.

The event happen online and at select venues accross the world. In Paris, it will take place at 42, on October 28-30, 2022. It will be preceded by a workshop on October 20.

More information:
- [In-person event, in Paris](https://coglab.fr/ntxhack2022/)
- [Online event, anywhere](https://neurotechx.com/hackathon2022/)

## Organization 

### Hack your mind and body

- **Team up**
- Select the **input** (brain, heart, muscle, data)
- We provide **plug-and-play** processing **pipelines** (but you can make your own if you feel like it)
- **Connect** everything (0MQ, Websockets, OSC, LSL)
- Build the **output** (Python, JavaScript, Unity, Arduino, other)
- Have **fun**!

## Masterclass materiel 

### Installation

Follow the guidelines from this [Getting started](https://doc.timeflux.io/latest/usage/getting_started.html). 

Once you have everything ready (git, anaconda and timeflux installed), you may clone this repository:  
```
git clone https://github.com/timeflux/hackathon
```

If you still need to install a timeflux environment: 

- Conda env

```bash
conda env create -f environment.yml
conda activate timeflux-hackathon
```

- Virtual env 
```
python3 -m venv  venv
source venv/bin/activate
pip install -r requirements.txt
```

### Exercices
Here, you'll find the material for the Masterclass exercises: 

- [Exercise 1](exercises/Exercise 1 - Your very first graph.md): Run your very first graph with timeflux
- [Exercise 2](exercises/Exercise 2 - Playing with waves .md): Edit a YAML graph, play-around with sinus and learn more advance features step by step: 
	1. Learn to use multiple ports 
	2. Practice basic filtering with dsp pluggin
	3. Display your signal in the UI
	4. Save your data into a file and understand ZMQ purpose for multiple graph
	5. Design a feedback with timeflux.js
	6. (bonus) Play around with the parameters to avoid pitfalls. 


## Demos
We'll show you how to reproduce the demonstrations from the Masterclass! 
### Hardware
- Bitalino ([eeg sensors](https://bitalino.com/datasheets/REVOLUTION_EEG_Sensor_Datasheet.pdf)), #3 ([ecg sensors](https://bitalino.com/datasheets/REVOLUTION_ECG_Sensor_Datasheet.pdf)), #4. ([emg sensors](https://bitalino.com/datasheets/REVOLUTION_EMG_Sensor_Datasheet.pdf)). 

 <img src="img/device_bitalino.png" width="60%">
 
**NB:** There's a *direction* for plugging in the sensor. 

**NBB:** The sensor are bipolar, that is you have 3 electrodes: ground (white), IN- (black), IN+(red). 

### Code 
It's all in the [demos repository](https://github.com/timeflux/demos)

- [Cardiac coherence](https://github.com/timeflux/demos/tree/main/coherence) 
- [Roshambo EMG gesture detection](https://github.com/timeflux/demos/tree/main/roshambo) 
- [EEG bands neurofeedback](https://github.com/timeflux/demos/tree/main/neurofeedback/bands) 

## Getting help 

### Community
- [Timeflux slack](https://timeflux.slack.com/join/shared_invite/enQtNjM1MDA1MTI1MTU1LWFjNGQxYmY0ZDgxMDI5MWU3ZDE2ZDMyYjBiNGNjMGZmNmNkNDAzNjM0NmE0MDY3ZWM3MGIzZTFiZjA5ZDNmYjM)
- [NeurotechX slack](https://neurotechx.com/slack/) 
- Or email us a name@imeflux.io with name being pierre, raphaelle, sylvain, .. (depending on your needs !) 

### Helpful Links
- To have a better understanding of digial signal processing, [Raphael Vallat website](https://raphaelvallat.com/) is very nice.
- List of BCI-related ressource by NTX [here](https://github.com/NeuroTechX/awesome-bci)
- In [Neurotechedu](http://learn.neurotechedu.com/lessons/), you will find our educational content grouped by related clusters
- Timefluw documentation [here](https://doc.timeflux.io/latest/)

## Pitffalls

### Timeflux 


#### Check your graphs! 

| Subject        | Symptoms      | Possible answer  |
| -------------- |:-------------:| ----------------:|
| terminal: env  | `command not found: timeflux` | `activate your timeflux environment`  |
| network: ZMQ   |  multiple graphs cannot communicate      |   You need Pub, Sub AND broker. |
| network: LSL   | stream received through LSL live in a different age      |  Check parameter [`sync`](https://doc.timeflux.io/latest/api/timeflux.nodes.lsl.html) |
| scheduler lags | ![](img/late_schedule.gif)        |    Increase the rate of your graph (default is 1 refresh per sec) |
| UI routes        | You cannot find your app in the browser    |   You need to launch the timeflux command from where the route to your app is refered in your graph.   |
| subject        | symptoms    |    Possible answer  |
| subject        | symptoms    |    Possible answer  |
| subject        | symptoms    |    Possible answer  |


### Signals processing: 
**Check I/O does what you think!**

command not found: timeflux

- **High filter order and induced delay & phase distortions:**
 IIRFilter is a nonlinear phase filter (in passband), it distorts the frequency contents of passband region of signal. Get convinced yourself with [bonus part of exercise 2.](exercises/Exercise 2 - Playing with waves .md). 
 <img src="exercises/img/hello_sinus_phaseshift_screenshot.png" width="80%">

 
- **Windowing** (the slower, the smoother): Real time is a lie, we do **pseudo-real-time**. Indeed,  Machine learning pipelines usually require the extraction of features that have the ability to represent each class in a representative way in order to be possible to distinguish them. For example, we can use windows of 1 second with or without overlap and represent each of these windows by a set of features, such as the mean, standard deviation, among others. We achieve this by using the [Window](https://doc.timeflux.io/latest/api/timeflux.nodes.window.html) node of timeflux. There are two ways of managing windowed extraction: 
	- **either** you add a node `Window` in your graph and plug it between your signal and your feature extractor (see [welch example](https://github.com/timeflux/hackathon/blob/f15f5582d08d85be30e4365a8200c429984ff2dd/graphs/ecg_coherence/biomarkers.yaml#L156-L163)); 
	- **or** you extend the class `Window` and exploit the output (see [moving average example](https://github.com/timeflux/hackathon/blob/f15f5582d08d85be30e4365a8200c429984ff2dd/modules/nodes/filters.py#L7-L45)). 


### Device installation 
**Always have a look at the monitor!**

- Unplug your laptop ! ! 
![unplug-effect](img/unplug_effect.gif)
- Ensure you that sensors are plugged the right way 
 <img src="img/bitalino_montage.png" width="30%">

- Signal quality: always keep a SQI tracker
- Sensors montage: ask google! 

### Commands 
**Keep safeguards!(!!)**

- [False positive](https://en.wikipedia.org/wiki/False_positives_and_false_negatives) **always happen** and can cause damage if you don't keep safeguards in your design. 

 <img src="img/false_positive.jpg" width="80%">


Imagine you associate a brain state to a command of a drone, it could scratch for example brain because you blinked and the model mistakes. A nice practice is to ask yourself: *how bad is it to classify wrong?*
When you work with more than 2 class, you may look at [confusion matrix](https://en.wikipedia.org/wiki/Confusion_matrix) that represents pairwised false positives. 

- **Dynamic of the feedback** (one more word) should work together with the dynamic of the command. Often, you'll have to choose the length of a rolling window to estimate your markers. In general, if you want to give the user the feeling of control over the interface, the dynamic should be "_as fast as possible_' (ie. short window). It's all a compromise betweeen responsivness (dynamic) and robustness (accuracy). 
![feedback_dynamic](img/feedback_dynamic.gif)

- For continuous feedback **the Value range** of the feedback is important as well. Indeed, your feedback needs to know the boundaries of the markers it represents, to be able to gradually adapt the feedback (eg. color, sound, circle radius...). One trick is to use a baseline: either fixed or adaptive, to calibrate the min/max values. Then, to make sure the feedback won't saturate (safeguard again!!) or to go from a continuous feedback to a discrete one, you may use an [activation function](https://en.wikipedia.org/wiki/Activation_function#Comparison_of_activation_functions). 
