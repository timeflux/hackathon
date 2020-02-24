# Hack yourself! 

## Timeflux @ 42
[Timeflux](https://timeflux.io) is an open-source Python framework for building BCI

The event will take place at 42, on March 13-15. It will be preceded by one full day of
basic neurophysiological / BCI theory and by a Timeflux practical workshop on February 26.


On the hardware side, we have partnered with MindAffect (https://www.mindaffect.nl), who will
provide 3D-printed headsets with integrated TMSI electrodes. Their recognition algorithm will
also be integrated in Timeflux. In addition, we are in the process of validating a collaboration
with Bitalino (https://bitalino.com). We would love to have OpenBCI on board too.

These are the tracks we have imagined for this event:

- Noise tagging BCI (occiptal) — MindAffect + OpenBCI
- Neurofeedback (pre-frontal, bipolar) — Bitalino
- Cardiac coherence (ECG, PPG) — Bitalino
- Gestures (EMG) — Bitalino


Thanks to everybody for making this event possible:

- [Bitalino](https://www.mbed.com/en/) for sponsoring the biosignal (ECG, EMG, frontal EEG) hardware, 
- [OpenBCI](https://openbci.com/) for sponsoring the EEG boards
- [MindAffect](https://www.mindaffect.nl/) for the EEG headset, the Noise-Tagging demo, and the staff
- [NeurotechX/Coglab](https://neurotechx.com/) for the talks and staff  
- [Talent.io](https://www.talent.io/fr/) for the prizes
- **42 School of course** (especially Sophie, Benny and Fabienne) for support, accomodation & co! 


## What should you expect from the hackathon?

At this Timeflux event for [42](https://www.42.fr/) you bring your laptop and get the opportunity to use [bitalino](https://bitalino.com), [MindAffect](https://www.mindaffect.nl/) and [openBCI](https://openbci.com/) hardwares to discover and explore real-time processing, biofeedback and brain-computer interfaces. The [timeflux](https://timeflux.io/) team and [neurotechX/coglab](https://neurotechx.com/) team will show participants how to get started with the framework, the devices, the signal processing & co, and be on-site for support throughout the event.

Our Theme -- Hack yourself! :

- The aim is to developp an application/experiment/installation (whatever :) ) that somehow makes use of bio/neuro-signals 
- Teams will have ~~48 hours  to create their app;
- Prizes will be given at the end for the best realizations;
- Food and drinks will also be provided.

## Teams inscriptions
- Team of 5
- Choose a track
- Name the person responsible
- Fullfill the table -> 
- 
- todo ??? 

## Submissions & Prize Jury
todo ! 

How to sign up for the prizes:

- one or more photos/screenshots/videos of your project;
- one paragraph describing your solution;
- submission deadline is Sunday the 15th at 6pm (??)
- 
- todo ??? 

# Let's go !
## Installation
## Repository organization
### App
### Data
### Exercises
### Graphs
### Modules

## Workshop
## Hackathon
### Hardware

### Tracks
#### Noise tagging BCI (occiptal) — MindAffect + OpenBCI

#### Neurofeedback (pre-frontal, bipolar) — Bitalino

#### Cardiac coherence (ECG, PPG) — Bitalino

#### Gestures (EMG) — Bitalino


## Piffalls
###Timeflux 
Check your graphs! 

#### Basics: 
1. Did you activate your environment? `conda activate timeflux`  
2. If multiple graphs => you need Pub, Sub AND broker
3. Check graph rates if you feel your scheduler is getting late (default is 1Hz) or if you get congestion logs. 
4. If using LSL, be careful on what syncho you use 

### Signals processing: 
Check I/O does what you think!
 
- Filter order and induced delay, phase distortions 
- Dynamic of feedback (the slower, the smoother ) 

### Device installation 
Always have a look at the monitor! 

- Ensure you that sensors are plugged the right way
- Signal quality: always keep a SQI light
- Sensors montage: ask google! 

### Commands 
Keep safeguards!(!!)

- False positive
- Dynamic of the feedback
Value range of the feedback (tricks: baseline, tanh) 

