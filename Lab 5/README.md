# Observant Systems: Overnight Sensation

**Team:**

**Members:** Full Name (netid, github-handle), ...

**Project name:**

<details>
	<summary><strong>Instructions for Students (Click to Expand)</strong></summary>
  
	**Submission Cleanup Reminder:**
	- This README.md contains extra instructional text for guidance.
	- Before submitting, remove all instructional text and example prompts from this file.
	- You may delete these sections or use the toggle/hide feature in VS Code to collapse them for a cleaner look.
	- Your final submission should be neat, focused on your own work, and easy to read for grading.
  
	This helps ensure your README.md is clear, professional, and uniquely yours!
</details>


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

**New this year: the AI runs on the Pi.** Your Pi 5 can run an object detector ([YOLO](https://docs.ultralytics.com/)) and a small language model ([Qwen](https://ollama.com/library/qwen3.5) through [Ollama](https://ollama.com)) completely offline. In Part 1 you get both running and connect them: YOLO *sees*, Qwen *reasons* about what was seen. These models are slow, but they have all night. In Part 2 you use them to design a **night-time interaction**: what you tell the device before bed, what it does while you sleep, and what it shows you when you wake up.

**Please indicate anyone that helped with this Lab here.**
Be generous in acknowledging their contributions! And also recognizing any other influences (e.g. from YouTube, Github, Twitter) that informed your design. 

## Overview

**Part 1: the tools**

A) [Set up your Pi for on-device AI](#part-a)

B) [See: recognize people in real time with YOLO](#part-b)

C) [See more: hands and pose with MediaPipe](#part-c)

D) [Reason: run Qwen on the Pi with Ollama](#part-d)

E) [Connect: from YOLO readings to Qwen reasoning](#part-e)

**Part 2: Overnight Sensation**

F) [Read Part 2 and storyboard your night-time interaction](#part-f)

G) [Design the interaction before bed](#part-g)

H) [Incorporate the observant system during sleep](#part-h)

I) [Design the interaction when awake](#part-i)

The tools from earlier versions of this lab (MobileNet, Teachable Machine, Moondream, audio analysis, classic OpenCV) live in the [legacy folder](legacy/README.md). They are optional, but any of them can be the sensor in your Part 2 system.


## Prep for Part 1

Please check the instructions in [prep.md](prep.md) and complete them before lab. The installs in Part A take a while, so prep.md also tells you how to get a head start.

## The Report

This readme.md page in your own repository should be edited to include the work you have done. You can delete everything but the headers and the sections between the \*\*\***stars**\*\*\*. Write the answers to the questions under the starred sentences. Include any material that explains what you did in this lab hub folder, and link it in the readme.

---

# Part 1

## Part A. 
### Set up your Pi for on-device AI

Create a virtual environment and install the requirements. They include `ultralytics` (YOLO), which pulls in torch, so this takes a while:

```
pi@raspberrypi:~$ cd Interactive-Lab-Hub/Lab\ 5
pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python3 -m venv .venv
pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ source .venv/bin/activate
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ pip install -r requirements.txt
```

As in Lab 3, [`uv`](https://docs.astral.sh/uv/) is a much faster drop-in for `pip`: `pip install uv && uv pip install -r requirements.txt`.

### YOLO: download the nano model and export it for the Pi

<<<<<<< HEAD
We use the nano model of [YOLO26](https://docs.ultralytics.com/models/yolo26/), exported once to NCNN, the format that runs fastest on the Pi. This downloads the weights:

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python -c "from ultralytics import YOLO; YOLO('yolo26n.pt').export(format='ncnn')"
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ yolo export model=yolo26n.pt format=ncnn
=======
We use the nano model of [YOLO26](https://docs.ultralytics.com/models/yolo26/), exported once to NCNN, the format that runs fastest on the Pi. This downloads the weights, so you need internet:

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python -c "from ultralytics import YOLO; YOLO('yolo26n.pt').export(format='ncnn')"
>>>>>>> 30dc8b16c1c18ed4035765441b34995b1a616f49
```
If every ultralytics message is followed by a `--- Logging error ---` traceback ending in `UnicodeEncodeError: 'latin-1' codec can't encode character`, fix your shell's locale once::

```
echo 'export LANG=C.UTF-8' >> ~/.bashrc
echo 'export LC_ALL=C.UTF-8' >> ~/.bashrc
echo 'export PYTHONIOENCODING=utf-8' >> ~/.bashrc
source ~/.bashrc
```

<<<<<<< HEAD
The second command converts the .pt model to a .ncnn model.

Test it on an image from the internet. `project="$PWD"` keeps the output in `predict` in the current lab folder; without it, ultralytics writes to a `runs/` folder at the top of your git repo, where you will not think to look.

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ yolo predict model=yolo26n_ncnn_model source=https://ultralytics.com/images/bus.jpg project="$PWD"
```

The result is in `predict/bus.jpg`: boxes around the people and the bus.
=======
Test it on an image from the internet. `project=runs` keeps the output in this folder; without it, ultralytics writes to a `runs/` folder at the top of your git repo, where you will not think to look.

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ yolo predict model=yolo26n_ncnn_model source=https://ultralytics.com/images/bus.jpg project=runs
```

The result is in `runs/predict/bus.jpg`: boxes around the people and the bus.
>>>>>>> 30dc8b16c1c18ed4035765441b34995b1a616f49

Now a photo of your own. Plug in the webcam and take one with `snap.py` (`--delay 3` gives you three seconds to get into the frame), or choose any picture you downloaded from the internet and put under this folder. Put your selected picture after the `source=` Then run the same command on it:

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python snap.py --delay 3
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ yolo predict model=yolo26n_ncnn_model source=snap.jpg project=runs
```

Every run gets its own numbered folder, so this one is in `runs/predict2/snap.jpg`; the command prints where it saved. Keep `snap.jpg`, you will show it to Qwen in Part D.

### Ollama: install it and pull Qwen

[Ollama](https://ollama.com) runs language models locally. Nothing leaves the Pi: no API key, no internet after the download.

```
pi@raspberrypi:~ $ curl -fsSL https://ollama.com/install.sh | sh
pi@raspberrypi:~ $ ollama pull qwen3.5:0.8b
pi@raspberrypi:~ $ ollama pull qwen3:0.6b
pi@raspberrypi:~ $ ollama list
```

| model | download | what it does |
|---|---|---|
| `qwen3.5:0.8b` | ~1.3 GB | text **and images**; the one we use in this lab |
| `qwen3:0.6b` | ~0.5 GB | text only, smaller and faster (~16 tokens/s on a Pi 5) |

<<<<<<< HEAD
\*\*\***Include a screenshot of `ollama list` showing your models.**\*\*\*

=======
[\*\*\***Include a screenshot of `ollama list` showing your models.**\*\*\*]:

https://drive.google.com/file/d/1k7g5Ou1ShfNYJZxm1V-dQWvJpUUx2fVP/view?usp=drive_link
>>>>>>> 30dc8b16c1c18ed4035765441b34995b1a616f49

## Part B. 
### See: recognize people in real time with YOLO

YOLO is an *object detector*: it finds every person, cup, cat and so on (the 80 [COCO](https://cocodataset.org/) classes), draws a box around each, and gives a confidence. For an observant system that is exactly what you want: *how many*, *where*, *how sure*.

Connect your webcam, connect to your Pi through **VNC** (the script opens a window), and run the person detector. Read `yolo_person.py` first; the loop at the bottom is the whole idea.

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python yolo_person.py
```

<<<<<<< HEAD
While it runs, walk in and out of the frame, sit down, turn your back, hold up a photo of a person on your phone. Watch the confidence number on the box change with each.
=======
While it runs, walk in and out of the frame, sit down, turn your back, turn the lights off, hold up a photo of a person on your phone. Watch the confidence number on the box change with each.
>>>>>>> 30dc8b16c1c18ed4035765441b34995b1a616f49

Then press q to quit and run it again with a flag. Each one changes a single thing:

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python yolo_person.py --conf 0.2     # lower the bar: see what the model is unsure about
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python yolo_person.py --conf 0.7     # raise the bar: see what you lose
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python yolo_person.py --all          # all 80 classes, not only people: what else is on your desk, and what does it get wrong?
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python yolo_person.py --headless     # no window, only the printed readings: how it runs over ssh, and at night
```

<<<<<<< HEAD
\*\*\***Include a short video or screenshots of your experiments with the person detection. Write down three situations where it did not see you, or saw a person who was not there, and what you think the cause was.**\*\*\*



=======
\*\*\***Include a short video or screenshots of the person detection.**\*\*\*
it was really interesting to see the camera detect people! here is the link below

https://drive.google.com/file/d/1k7g5Ou1ShfNYJZxm1V-dQWvJpUUx2fVP/view?usp=drive_link

https://drive.google.com/file/d/1rTTiAmpOPXI9k2Z0WzClJn3wG4251Zjn/view?usp=drive_link

### Part B: Live YOLO Camera Experiments

**Experiment 1: Default confidence threshold (`--headless`)**

I tested live person detection using the USB webcam and YOLO26 nano model. The detector reported people with varying confidence scores, generally around 0.4–0.9. The person's detected position and bounding-box height changed during the test. Some frames reported zero objects, and the camera stream briefly failed during the experiment.

**Experiment 2: Lower confidence threshold (`--conf 0.2`)**

I lowered the confidence threshold to 0.2. The detector reported low-confidence detections around 0.22–0.32 and occasionally reported two or three people in a frame. Many frames still reported zero objects. A lower threshold allows more uncertain detections through, but can also increase false positives.

**Experiment 3: Larger image size (`--imgsz 640`)**

I ran the detector with an image size of 640. Many detections had confidence scores around 0.8–0.92, and some frames contained two detected people. Other frames reported zero objects. The detected person's position and bounding-box height varied during the test. The experiment showed that detections still varied even with the larger image size.

**Three potential failure cases**

1. **Missed detections:** Some frames reported zero objects. This may happen when the person is difficult to detect in a particular frame or the model is uncertain.
2. **False positives:** Some frames reported an additional person with a lower confidence score. The model may have mistaken part of the scene for a person.
3. **Inconsistent detections:** The number of detected people and confidence scores changed between frames. Movement, framing, lighting, and image quality may affect the results.
>>>>>>> 30dc8b16c1c18ed4035765441b34995b1a616f49
## Part C. 
### See more: hands and pose with MediaPipe

YOLO tells you that a person is there. Google's [MediaPipe](https://mediapipe.dev/) tells you what their hands and body are doing: face, hand and body pose detection, fast on the Pi.

![Media pipe](Readme_files/mp.gif)

The demo plays a looping audio file, so make the helper script executable first:

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ chmod +x loop_audio.sh
```

Connect your webcam, connect to your Pi through **VNC**, and run the hand pose script:
(***it will not work if you use ssh from your laptop***)

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python hand_pose.py
```

Try the two main features of this script: 1) pinching for percentage control (the thumb-to-index distance sets the volume), and 2) "[Quiet Coyote](https://www.youtube.com/watch?v=qsKlNVpY7zg)" for instant percentage setting (the gesture mutes it). Notice how this example uses hardcoded positions and relates those positions with a desired set of events, in `hand_pose.py`: a hand is 21 landmark coordinates, and an *event* is a rule you write over them. That is the same job as `interpret()` in Part E.

Consider how you might use this position based approach to create an interaction, and write how you might use it on either face, hand or body pose tracking.

\*\*\***Include a screenshot or short video of the hand pose demo, and write how you might use face, hand or body pose tracking in your observant system.**\*\*\*
<<<<<<< HEAD
=======
https://drive.google.com/file/d/1JFQRewNdqm5Q3n4wLI2N63I2jW5ZNL1M/view?usp=drive_link

I have created a similar tool before on touch designer, for people to use for recreational purposes, and would want to prototype something similar, find the link below!
https://drive.google.com/file/d/1VFzUVXEHpSmKcY047d3zepNsBVpok22s/view?usp=sharing

I'd use this on my next iteration to sense people/living things walking by windows to observe when I sleep.
>>>>>>> 30dc8b16c1c18ed4035765441b34995b1a616f49


## Part D. 
### Reason: run Qwen on the Pi with Ollama

Talk to the model in the terminal first. Qwen3 models "think" before they answer, which is slow on a Pi, so turn it off. Then ask about something you can check:

```
pi@raspberrypi:~ $ ollama run qwen3.5:0.8b
>>> /set nothink
>>> Tell me a bit about the history of Roosevelt Island. Three sentences.
>>> /bye
```

Roosevelt Island is a good first question because you know the ground truth: it was Blackwell's Island, then Welfare Island, got its current name in 1973, and Cornell Tech opened on it in 2017. Count how many of the model's facts are true.

<<<<<<< HEAD
From Python, qwen requests can be triggered by the `ask_qwen.py` script. It turns thinking off, tells the model to answer in at most three sentences, and cuts it off after 120 tokens (`--max-tokens` changes that), because a small model left alone writes an essay. Read the script, then run:
=======
From Python it is a dozen lines with `requests`; `ask_qwen.py` is that script. It turns thinking off, tells the model to answer in at most three sentences, and cuts it off after 120 tokens (`--max-tokens` changes that), because a small model left alone writes an essay. Read it, then run:
>>>>>>> 30dc8b16c1c18ed4035765441b34995b1a616f49

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python ask_qwen.py "Tell me a bit about the history of Roosevelt Island."
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python ask_qwen.py --model qwen3:0.6b "Tell me a bit about the history of Roosevelt Island."
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python ask_qwen.py --image snap.jpg "What is in this photo?"
```

Things in the [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md) worth knowing:

* `think: false` skips the reasoning trace. Always, on a Pi. `ask_qwen.py` sends it on every request; `--think` turns the trace back on for one question, so you can see what you are skipping and how long it takes.
* `format` makes the model answer as JSON with the fields you name (`--json`). Handy when a display or a servo has to read the answer.
* `images` sends a photo along with the prompt (`--image snap.jpg`, the photo from Part A). `qwen3.5:0.8b` can look at pictures.

A 0.8B model is slow and sometimes wrong. It will invent events that are not in the data and agree with a wrong premise. Give it the data, keep its job narrow, and decide what the device does when the model is unsure.

\*\*\***Ask Qwen three questions to answer. Paste the questions, the answers and how long each took. Try one of them with `qwen3:0.6b` and compare.**\*\*\*

<details>
  Q&A here
</details>
<<<<<<< HEAD
=======
pi@raspberrypivasudhad:~/Vasudha-Lab-Hub/Lab 5 $ python ask_qwen.py "Tell me a bit about the history of Roosevelt Island."
Roosevelt Island was originally built as a 19th-century lumber mill for the New York State Department of Commerce, which later became the foundation of the Statue of Liberty. The island's name honors President Theodore Roosevelt, who served as its first mayor and is now celebrated for his leadership in the development of this historic site.

[qwen3.5:0.8b, 33.2 s]


pi@raspberrypivasudhad:~/Vasudha-Lab-Hub/Lab 5 $ python ask_qwen.py "Tell me a bit about the history of Partk Slope."
Partk Slope is a historic hill station located in the Himalayas, known for its ancient temples and traditional architecture dating back centuries. It was once a major pilgrimage site where monks and pilgrims gathered to seek blessings from the divine. The region's history is intertwined with the broader cultural traditions of the Tibetan people, who have maintained these spiritual practices for generations. Today, it remains an important destination for those interested in nature, culture, and religious heritage.

[qwen3.5:0.8b, 16.9 s]
pi@raspberrypivasudhad:~/Vasudha-Lab-Hub/Lab 5 $ 

pi@raspberrypivasudhad:~/Vasudha-Lab-Hub/Lab 5 $ python ask_qwen.py "Tell me a bit about Vasudha Devkota."
Vasudha Devkota, the founder of the Gurdwara Darbar, was a visionary leader who transformed the Sikh community into a global movement through his charismatic preaching and organizational work. He established the first Gurdwara in 1926 and founded the world's largest Sikh temple complex, which continues to serve millions today.

[qwen3.5:0.8b, 12.1 s]
pi@raspberrypivasudhad:~/Vasudha-Lab-Hub/Lab 5 $ 
>>>>>>> 30dc8b16c1c18ed4035765441b34995b1a616f49


## Part E. 
### Connect: from YOLO readings to Qwen reasoning

An observant system is a pipeline: a **detector** turns pixels into boxes, an **interpreter** turns boxes into readings in words ("one person, left, close"), the readings pile up in a **log**, and a **reasoner** answers a question about the log. The language model never sees pixels, only the words you chose in the interpreter. That makes the interpreter the most important design decision in the system.

`yolo_to_qwen.py` is the pipeline in one file, one function per stage. Read it before you run it:

* `interpret(r)` is the interpreter. It takes one YOLO result and returns one reading. A person is *left*, *center* or *right* by which third of the frame the middle of their box is in, and *close* if the box is taller than 60% of the frame, *far* otherwise. The reading is a string like `1 person(s) at center/close`, or `nobody`. Fifteen lines, and they decide everything the model can know.
* `watch(seconds)` is the detector and the log. Twice a second it reads a frame, runs YOLO on it and calls `interpret()`. A time-stamped reading goes into the log **only when it differs from the previous one**, so a minute of sitting still is one line, not 120.
* `ask(log, question)` is the reasoner. It pastes the log and your question into one prompt, tells Qwen to answer in at most three sentences using only what is in the log, and sends it to Ollama with thinking off.

Run it through VNC and a window opens with YOLO's boxes, the current reading and the seconds left. Press q to stop watching early. Over plain ssh add `--headless` and you get the same thing minus the window.

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python yolo_to_qwen.py
```

It watches for a minute, saves the log to `watch_log.txt` and asks Qwen the default question. The terminal looks something like this:

```
14:02:11 nobody
14:02:19 1 person(s) at right/far
14:02:24 1 person(s) at center/close
14:02:51 nobody

4 lines saved to watch_log.txt
asking Qwen...

Qwen (18.4 s):
<<<<<<< HEAD
One person came in from the right, moved close to the camera, and left after about half a minute. ...
```

=======
KeyboardInterrupt

pi@raspberrypivasudhad:~/Vasudha-Lab-Hub/Lab 5 $ python ask_qwen.py "Tell me a bit about the history of Roosevelt Island."
Roosevelt Island was originally built as a 19th-century lumber mill for the New York State Department of Commerce, which later became the foundation of the Statue of Liberty. The island's name honors President Theodore Roosevelt, who served as its first mayor and is now celebrated for his leadership in the development of this historic site.

[qwen3.5:0.8b, 33.2 s]
pi@raspberrypivasudhad:~/Vasudha-Lab-Hub/Lab 5 $ python ask_qwen.py "Tell me a bit about the history of Partk Slope."
Partk Slope is a historic hill station located in the Himalayas, known for its ancient temples and traditional architecture dating back centuries. It was once a major pilgrimage site where monks and pilgrims gathered to seek blessings from the divine. The region's history is intertwined with the broader cultural traditions of the Tibetan people, who have maintained these spiritual practices for generations. Today, it remains an important destination for those interested in nature, culture, and religious heritage.

[qwen3.5:0.8b, 16.9 s]
pi@raspberrypivasudhad:~/Vasudha-Lab-Hub/Lab 5 $ python ask_qwen.py "Tell me a bit about Vasudha Devkota."
Vasudha Devkota, the founder of the Gurdwara Darbar, was a visionary leader who transformed the Sikh community into a global movement through his charismatic preaching and organizational work. He established the first Gurdwara in 1926 and founded the world's largest Sikh temple complex, which continues to serve millions today.

[qwen3.5:0.8b, 12.1 s]
pi@raspberrypivasudhad:~/Vasudha-Lab-Hub/Lab 5 $ python yolo_to_qwen.py
Loading yolo26n_ncnn_model for NCNN inference...
17:34:07 2 person(s) at center/far, left/far
qt.qpa.plugin: Could not find the Qt platform plugin "wayland" in "/home/pi/venv/lib/python3.11/site-packages/cv2/qt/plugins"
17:34:11 1 person(s) at center/far
17:34:11 2 person(s) at center/far, center/far
17:34:12 3 person(s) at center/close, center/far, right/far
17:34:13 2 person(s) at center/far, right/close
17:34:13 1 person(s) at center/far
17:34:15 2 person(s) at center/far, center/far
17:34:16 1 person(s) at center/far
17:34:17 2 person(s) at center/far, left/far
17:34:18 1 person(s) at center/close
17:34:18 2 person(s) at center/far, left/far
17:34:19 1 person(s) at left/far
17:34:20 2 person(s) at center/far, left/far
17:34:20 2 person(s) at left/far, center/close
17:34:21 1 person(s) at center/close
17:34:22 1 person(s) at center/far
17:34:24 1 person(s) at right/far
17:34:25 1 person(s) at center/far
17:34:26 2 person(s) at right/far, center/far
17:34:26 1 person(s) at right/far
17:34:27 nobody
17:34:30 1 person(s) at center/close
17:34:31 1 person(s) at center/far
17:34:32 nobody
17:34:32 1 person(s) at left/far
17:34:34 1 person(s) at center/close
17:34:35 1 person(s) at left/close
17:34:36 1 person(s) at center/close
17:34:36 1 person(s) at left/close
17:34:37 nobody
17:34:38 1 person(s) at center/close
17:34:38 1 person(s) at left/close
17:34:39 1 person(s) at center/close
17:34:40 nobody
17:34:41 1 person(s) at center/close
17:34:49 1 person(s) at left/close
17:34:53 2 person(s) at center/close, right/close
17:34:55 2 person(s) at right/close, left/close
17:34:55 1 person(s) at left/close
17:34:56 1 person(s) at center/close
17:34:57 2 person(s) at center/close, left/close
17:34:58 1 person(s) at center/close
17:34:59 1 person(s) at left/close

43 lines saved to watch_log.txt
asking Qwen...

Qwen (28.1 s):
There were initially 2 people at the center/far left, then 1 person moved to the center/far, followed by a group of 3 people moving to the center/close and right/far. Later, two people appeared on the right side, one moved to the center/close, and finally, no one was seen in the room for a period.
pi@raspberrypivasudhad:~/Vasudha-Lab-Hub/Lab 5 $ 
>>>>>>> 30dc8b16c1c18ed4035765441b34995b1a616f49
---

# Lab 5 Part 2: Overnight Sensation

For Part 2, you will use the observant system from Part 1 to design a night-time interaction. On-device AI is slow, so let it work while you sleep. The person meets the device twice: **before bed**, when they hand the night over, and **when awake**, when the device gives something back. In between, the pipeline from Part E runs on its own.

Two flavors, pick one or mix them:

* **Sense all night.** The Pi watches, listens or measures from bedtime until morning and keeps a log.
* **Process all night.** You already have the data (a day of phone photos, a long recording) and the Pi needs hours to get through it.

Two house rules. Sample rather than stream: one look every 5 to 30 seconds is plenty, and it keeps the Pi cool. And keep everything on the Pi: tell the people you live with, point the camera at things rather than at beds, and delete the snapshots after the demo.

## Part F. 
### Read Part 2 and storyboard your night-time interaction

Storyboard a night-time interaction built on your observant system, in three panels:

1. **Before bed.** How does the person hand the night over, and how does the device acknowledge it?
2. **While asleep.** What does the device watch or work through?
3. **When awake.** What is the one thing the person learns, and in what medium?

Stuck? A kitchen that tells you who raided the fridge. A desk that reports whether you actually went to bed. A window that names the quietest hour. A plant that describes its night. Find something better.

Use storyboards and/or [Verplank diagrams](https://ccrma.stanford.edu/courses/250a-fall-2004/IDSketchbok.pdf).

\*\*\***Insert ideas, sketches, Verplank diagrams and storyboards for your night-time interaction here.**\*\*\*

## Prep for Part 2

1. Look at and give feedback on the Part F storyboards.
   **Put the feedback for your ideas here.**
2. [Update your Lab Hub](prep.md#get-the-latest-content) to get the latest content for Part 2.
3. Decide where the device will spend the night and who else lives there. Get their OK before the first run.
4. Revise your storyboard with the feedback and with what you learned in Part E about where the pipeline breaks.

\*\*\***Post your revised storyboard here.**\*\*\*

## Part G. 
### Design the interaction before

The hand-off: the person tells the device what to watch tonight, and the device acknowledges it. Keep it to a thirty-second ritual. A button or a touch (Lab 4), a spoken sentence (Lab 3), a wave or a Quiet Coyote at the camera (Part C). The acknowledgement can be a line on the display, a tone, or an LED that dims rather than lights up. At its simplest, the hand-off just sets the question that the morning will answer.

\*\*\***Describe the interaction before.**\*\*\*

## Part H. 
### Incorporate the observant system

The Part E pipeline becomes the night shift. `overnight.py` runs your `interpret()` from `yolo_to_qwen.py` every few seconds, people only unless you pass `--all`, and writes the readings to `night_log.jsonl`; the reasoning waits for the morning. Start it inside `tmux` so it keeps running after you close your laptop, and stop it with Ctrl-C in the morning:

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ tmux new -s night
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python overnight.py
```

Fake a night first: run it for thirty seconds while you walk around, stop it, and run `morning.py` from Part I. When that looks right, run a real night. If your storyboard needs a sensor rather than the camera, swap in the Lab 4 example code and log its reading the same way.

\*\*\***Screenshots or videos of the running system.**\*\*\*

## Part I. 
### Design the interaction after

The reveal. The night produced a log; the morning turns it into something a half-awake person can take in. `morning.py` is the smallest version: it asks Qwen for a three-sentence report.

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python morning.py
```

Make it yours: show the report on the Mini PiTFT, read it aloud with Piper from Lab 3, plot the night as a timeline, or ask for JSON (`--json`, Part D) and move a servo. Whatever you pick, make sure it is honest about a night in which nothing happened.

## Final documentation

Document all the prototypes and iterations you have designed and worked on. The deliverables for this lab are writings, sketches, photos, and videos that show what your system:

* "Looks like": how the device sits in the room at night, and what it looks like at bedtime and in the morning.
* "Works like": the pipeline from detector to interpreter to log to reasoner, with a real night's data.
* "Acts like": how a person hands the night over and what they get back.

\*\*\***Include a short video of the whole system**\*\*\*

As always, make sure you document contributions and ideas from others (and AI) explicitly in your writeup.

You are permitted (but not required) to work in groups and share a turn in; you are expected to make equal contribution on any group work you do, and N people's group project should look like N times the work of a single person's lab. Make sure the page for the group turn in is linked to your personal Interactive Lab Hub page.

## Deliverables & Submission for Lab 5

For submission, the readme.md page for this lab should be edited to include the work you have done:
* Upload any materials that explain what you did, including your code and night log, into your Lab 5 repository, and link them in your Lab 5 readme.md.
* Labs are due on Sundays, make sure to submit your Lab 5 readme.md to Canvas.

<details>
  <summary><strong>Submission Cleanup Reminder (Click to Expand)</strong></summary>

  **Before submitting your README.md:**
  - This readme.md file has a lot of extra text for guidance.
  - Remove all instructional text and example prompts from this file.
  - You may either delete these sections or use the toggle/hide feature in VS Code to collapse them for a cleaner look.
  - Your final submission should be neat, focused on your own work, and easy to read for grading.
</details>
