# Exercise 2 - Playing with waves

In this exercise, you are going to build a simple app without any line of code, only by describing your pipeline in the YAML syntax. 
The goal is for you to get acquainted with this syntax. 


## Exercise statement
In this exercise, you will : 

1. generate a noisy signal : sum a carrier wave of 1Hz and line noie of 50Hz (this has already been done for you) <br>
1. lowpass the summed signal (this is [Part 1](#part_1))
1. display the signal using the UI monitoring (this is [Part 2](#part_2))
1. save the data in a HDF5 file (this is [Part 3](#part_3))
1. design a feedback with timeflux.js (this is [Part 4](#part_4))
1. *(bonus) play around with parameters*

## Getting started

In this exercise, you will be editing a YAML graph and run it using timeflux command line. 

First, let's have a look at the graph. 

<img src="img/hello_sinus_exercise.png" alt='graph_exercise'>

```yaml
graphs:
  - id: hello_sinus
    nodes:
      - id: noisy_sinus
        module: timeflux_audio.nodes.signal
        class: Additive
        params: 
          frequencies: [1, 50] # Frequency of signal (1Hz) and line noise (50Hz)
          resolution: 128 # Sampling rate of th signal (128Hz)
          amplitudes:  [1, 0.2] # Amplitudes of signal (1) and line noise (0.2)
          name: noisy

      - id: display
        module: timeflux.nodes.debug
        class: Display

      # part 1
      # TODO: add a lowpass filter to filter the summed signal
      # Hint: https://doc.timeflux.io/latest/api/timeflux_dsp.nodes.filters.html

      # part 2
      # TODO: add an UI to monitor the signal before and after filtering
      
      # part 4
      # TODO: Add a route in the UI to your own app

    edges:
      - source: noisy_sinus
        target: display

      # part 1
      # TODO: plug the noisy signal to the filter

      # part 2
      # TODO: plug the signals to the UI

    rate: 32

  # part 3
  # TODO: Create a second graph to save the data into a file
```


### Command line 
- Open a terminal 
- Activate your environment:  
	```
	conda activate timeflux-hackathon
	```
- Run the app in debug mode: 
	```
	timeflux -d "exercises/solutions/Exercise 2/hello_sinus_exercise.yaml"
  ```

## <a href='#part_1'>Part 1</a> : Filter a signal 
Filter the summed signal to retrieve the carrier wave. 

**Hint:** Have a look at [this](https://doc.timeflux.io/projects/timeflux-dsp/en/stable/api/timeflux_dsp/nodes/filters/index.html) piece of doc.

Answer the TODO of part 1 and again, in a terminal, run:

```
timeflux graphs/hello_sinus_exercise.yaml -d
```


One solution is given [here](./solutions/Exercise%2/hello_sinus_solution_part1.yaml)

<img src="img/hello_sinus_solution_part1.png" alt='hello_world'>


## <a href='#part_2'>Part 2</a> :  Visualize the signals   
Use timeflux UI monitoring to display pre/post signals in your browser.

**Hint:** [Here](https://doc.timeflux.io/projects/timeflux-ui/en/stable/) is the doc.

Answer the TODO of part 2 and again, in a terminal, run:

```
timeflux graphs/hello_sinus_exercise.yaml -d
```

You may now open your browser at `http://localhost:8000/monitor/` and monitor your time-series ! 


<img src="img/hello_sinus.gif" alt='screenshot_part2'>


One solution is given [here](./solutions/Exercise%2/hello_sinus_solution_part3.yaml)

<img src="img/hello_sinus_solution_part2.png" alt='graph_part2'>


## <a href='#part_3'>Part 3</a> : Save your data in HDF5

Save your data in HDF5. <br>

**Hint:** Check [this](https://doc.timeflux.io/latest/usage/use_case.html) use case!

<div class="alert alert-info">
Until here, we only had one graph running at 32 Hz. In this part, we want to save the data to a file, which does not have to be done 32 times per seconds, and could lead to congestion. Therefore, it's highly recommanded to run the HDF5 recorder in a separate graph running at a lower rate.
</div>

<span style="color:red">**=> Pitfall #3 don't forget a Broker !!**</span>


In a terminal, run:

```
timeflux graphs/hello_sinus/hello_sinus_exercise.yaml -d
```

One solution is given [here](./solutions/Exercise%2/hello_sinus_solution_part3.yaml)

<img src="img/hello_sinus_solution_part3.png" alt='graph_part3'>


## <a href='#part_4'>Part 4</a> : Design a feedback with timeflux.js  

The idea here is to use [timeflux Javascript API](https://github.com/timeflux/timeflux_ui/blob/master/timeflux_ui/www/common/assets/js/timeflux.js)
 to design a feedback on the sinus amplitude in your browser. 
 For example, 
 
**Hint:** Check [these available example apps](https://github.com/timeflux/timeflux_ui/tree/master/apps).
 
 Something like: 
 
 <img src="img/hello_sinus_ui.gif" width="60%">

 
 One solution is given [here](./solutions/Exercise%2/hello_sinus_solution_part4.yaml) with the app code [there](./solutions/Exercise%2/app).

## <a href='#bonus'>Bonus</a> : Play around with the parameters

Now, time to play around with the parameters. 

For example, you may investigate the followin questions: 

### Questions
1.  What happens if you change the order of lowpass filter from 3 to 10? 
2.  What happens if you increase/decrease the rate of the graph? 

### Answers
1.  See bellow. 
<img src="img/hello_sinus_phaseshift_screenshot.png" alt='hello_world'>
IIRFilter is a nonlinear phase filter (in passband), it distorts the frequency contents of passband region of signal.
when working offline, one prefer to use a forward-backward filter ( [filtfilt](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html) ), which is not trivial online (but coming very soon!). 


2.  If you increase (too much) the rate of your graph, you'll notice some 'congestion' warnings in the console, it means that your nodes are still working when the scheduler updates. 
    In you decrease (too much) the rate of your graph, you'll notice that the time gets late, and that signals kind of stutter. 
