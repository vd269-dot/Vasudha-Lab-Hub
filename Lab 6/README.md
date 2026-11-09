# Distributed Interaction


### TELE-ABSENCE: A Tiny Network for Missing Someone

**Collaborators:** Jaclyn Pham, Vasudha Devkota and Demi Hu

---

# 1. Project Description

## What if we could send a message to someone that we miss ?

We wanted to make a distributed system about something that usually isn't treated like a technical problem: **missing someone.**

When you miss a person, you might text them, call them, send a photo, or wait for a notification. Most of these interactions often happen through screens. What could happen if that feeling could travel through a collection of small physical objects instead.

Our project is a playful exploration of **touch deprivation, presence, affection, and connection**.

We built a small network of Raspberry Pis that communicate through MQTT. Each Pi has its own personality and role in the interaction. One device can sense something happening, another can receive the message, and another can turn that message into a physical response.

Instead of one giant smart device doing everything, we wanted to create a tiny **community of devices** that have to talk to one another.

The result is somewhere between a communication system, a tiny orchestra, and a group of machines trying their best to comfort a human.

### Our question

> **Can a network of small machines create a feeling of presence when the person you want to be with isn't there?**

We are not trying to replace human touch.

Instead, we're interested in the little things technology can do to help us **hold onto a feeling**.

---

## The experience

Imagine two people are far apart.

One person interacts with their device.

That action becomes a message.

The message travels through the network.

Somewhere else, another Raspberry Pi receives it.

Instead of simply displaying:

**"MESSAGE RECEIVED."**

it responds with something a little more human:

**a glow.**

**a movement.**

**a sound.**

**a tiny harp.**

The important part is that the response happens somewhere else.

The device in front of you is connected to something you cannot see.

That distance is part of the experience.

---
## 🎥 See TELE-ABSENCE in Action

> **What happens when you send a message to someone you miss?**

Watch our project demo to see the interaction from beginning to end — from the physical gesture, through the MQTT network, to the response on the other side.

**[▶️ Watch the TELE-ABSENCE Demo on YouTube](https://youtu.be/xix3lFBBjuw?is=lJhrNe3feQKZ9PwR)**

The video shows:
- The physical interaction with the sending device
- The message traveling through MQTT
- The 3D-modeled hand responding on the receiving device
- The OLED feedback
- The distributed interaction between the Raspberry Pis

*The video is the shortest way to experience the project before diving into how we built it.*

# 2. Why Distributed?

We could have built everything on one Raspberry Pi.

We intentionally didn't.

The physical separation between the devices is part of the concept.

A distributed system gives us a way to represent **distance**.

One device can be here.

Another can be somewhere else.

MQTT becomes the invisible thread connecting them.

```text
       HUMAN A
          |
       touches
          |
          v
   +--------------+
   |  RASPBERRY   |
   |     PI 1     |
   +--------------+
          |
          | "I felt something."
          |
          v
   +--------------+
   | MQTT BROKER  |
   |  the middle  |
   +--------------+
          |
          | "Someone is thinking of you."
          |
          v
   +--------------+
   |  RASPBERRY   |
   |     PI 2     |
   +--------------+
          |
          v
     sound / light
       / motion
          |
          v
       HUMAN B
```

The MQTT broker acts almost like a **postal service for feelings**.

A device doesn't need to know exactly where another device is.

It simply publishes a message.

The broker takes care of finding the subscribers.

---

# 3. Meet the Devices

We think of the Raspberry Pis as characters rather than interchangeable computers.

## Pi 1 — The Listener

Pi 1 watches for physical input.

It can sense the environment through its sensors and translate physical events into digital messages.

**Input:** physical interaction / sensor data

**Computation:** interpret sensor event

**Output:** MQTT message

---

## Pi 2 — The Receiver

Pi 2 waits for something to arrive.

When it receives a message, it turns that invisible network event into something physical.

Our 3d Modeled Hand shows that the yearner at the other end has sent a message across- an invitation.



**Input:** MQTT message

**Computation:** interpret incoming event

---

## Pi 3 — The Feedback Loops

**Output:** OLED

The OLED shows that the yearsner has sent a messsage, and the receiver is also accepting the message.

---

# 4. How the Devices Talk

Our devices communicate using MQTT.

MQTT uses a publish/subscribe model.

Instead of Pi 1 directly calling Pi 2, it publishes a message to a topic.

```text
Pi 1
 |
 | publish
 v
IDD/ourteam/...
 |
 v
MQTT Broker
 |
 | subscribe
 v
Pi 2
```

This means the devices don't need to know everything about each other.

They only need to agree on the language.

### Our MQTT topics

| Topic | Publisher | Subscriber | Meaning |
|---|---|---|---|
| `IDD/djv/text` | [Pi] | [Pi] | Sends a text message |
| `IDD/ourteam/...` | [Pi] | [Pi] | [Describe] |
| `[FINAL TOPIC]` | [Pi] | [Pi] | [Describe] |

The topic structure gives each device a little vocabulary.

For example, a message could mean:

```text
"someone touched the device"
```

rather than simply:

```text
"1"
```

That distinction becomes important when designing distributed systems.

The network doesn't automatically know what our messages mean.

**We have to teach it the meaning.**

---

# 5. The Physical Build

Our system combines networking with physical computing.

### Hardware

- Raspberry Pi × 3
- APDS-9960 RGB/proximity sensor
- OLED display
- Qwiic/I²C connections
- Additional physical interaction hardware

The APDS-9960 gives the system a way to sense the physical world.

We can detect RGB values and proximity information and turn those physical events into MQTT messages.

To inspect the I²C bus:

```bash
i2cdetect -y 1
```

Our APDS-9960 appears at:

```text
0x39
```

The OLED uses I²C as well.

This creates a nice physical-to-digital-to-physical loop:

```text
        PHYSICAL WORLD
              |
              v
          SENSOR
              |
              v
       RASPBERRY PI
              |
              v
            MQTT
              |
              v
       RASPBERRY PI
              |
       +------+------+
       |             |
       v             v
     OLED          HARP
       |             |
       +------+------+
              |
              v
        PHYSICAL WORLD
```

Something happens in one place.

It becomes data.

The data travels.

Then it becomes something physical again.

---



A traditional notification says:

> **You have a message.**

Our device says:

> **Someone reached you.**

That difference is what we were interested in.


It is necessary for the **experience** we wanted to create.

---

# 7. Building the System

Each Raspberry Pi runs its own Python environment.

```bash
cd ~/Vasudha-Lab-Hub/Lab\ 6
source .venv/bin/activate
```

The Pi dependencies include the libraries required for MQTT, sensors, displays, and physical interaction.

MQTT communication is handled using Paho.

A simplified subscriber looks conceptually like:

```python
def on_message(client, userdata, msg):
    message = msg.payload.decode()

    display_message(message)
    play_harp()
```

The interesting part is what happens after the message arrives.

The network message becomes:

**data → interpretation → physical experience**

That is the central pattern of our project.

---

# 8. User Testing

We wanted to see whether people understood the interaction without us explaining everything first.

We tested the system with people outside our team.

## Participant 1

**Before interacting:**
The participant assumed it was a scary ghost like experience.

**What happened:**

They were pleasantly surprised to see the small hand movement, and noticed the message pop up as well.

**What surprised them:**

The message on the small LED screen

**What they would change:**
The said to prototype a hand sculpture that makes it easier for the mototr to run that isnt as heavy.

(https://drive.google.com/drive/folders/1SWNd8mpQCBsUyH--O63RVbbPssq6Nhnj)

---


## What we learned

We were particularly interested in whether people understood that the response was coming from another device rather than from the device directly in front of them.

We realized that we should have printed lighted models for the small smotor to be able to lift the fingers easier, and also that we needed more sensitive sensors.

This helped us think about an important question:

**How much does a person need to understand the network for a distributed interaction to feel meaningful?**

Ideally, the person doesn't need to understand MQTT.

They just need to feel that **something happened somewhere else because of what they did here.**

---

# 9. Reflection

## What worked?

The strongest part of the project was seeing an invisible network become physical.

MQTT messages are normally just text traveling through a network.

We turned those messages into things people could see and hear.

The OLED made the communication visible.

The harp made it audible.

The sensor made it physical.

Together, these components made the distributed system feel less like networking infrastructure and more like an interaction.

---

## What was difficult?

Distributed systems are difficult because the problem is rarely in only one place.

When something doesn't work, we have to ask:

- Is the sensor working?
- Is the Raspberry Pi connected?
- Is the Python environment correct?
- Is MQTT connected?
- Is the message being published?
- Is the topic correct?
- Is the other Pi subscribed?
- Is the receiving callback running?
- Is the output hardware working?

A single-device project can fail in one place.

A distributed project can fail **between places**.

That became one of our biggest lessons.

---

## What did we learn about sensor events?

Sensors are not automatically meaningful.

A sensor might produce:

```text
255, 136, 146
```

But a human doesn't experience those numbers.

We have to decide what they mean.

For our project, we experimented with turning sensor events into messages that could cause responses on another device.

This made us think about the translation between:

**physical event → data → meaning → response**

That translation is where much of the interaction design happens.

---

# 10. Where Does the Computation Happen?

We intentionally distribute computation across the system.

Here is a storyboard of our intent of use:
https://drive.google.com/file/d/1fHgQ8BSjocSsP8nNx9QxBR6NAcb-LIHZ/view?usp=drive_link

### On the Raspberry Pis

The Pis handle:

- Sensor input
- MQTT publishing/subscribing
- Message interpretation
- OLED rendering
- Audio playback
- Physical outputs

### On the MQTT broker

The broker handles:

- Receiving published messages
- Routing messages to subscribers

The broker does not decide what the message means.

**We do.**

This separation makes the system flexible.

A new device can join the network simply by subscribing to the appropriate topic.

---

# 11. What We Would Improve

If we continued developing this project, we would make the physical interactions more expressive.

Right now, the system demonstrates that a physical event can travel through a network and become another physical response.

We would like to push that further.

For example:

- A gentle touch could produce a gentle response.
- A long interaction could produce a longer sound.
- Different gestures could communicate different emotions.
- Multiple people could contribute to the same shared interaction.
- The system could remember recent interactions.
- The devices could develop different "personalities."
- The physical objects could become more tactile and less screen-like.

We are especially interested in making the interaction feel **less like sending a message and more like leaving a trace of yourself somewhere else.**

---

# 12. Final Reflection

This project started as an exercise in making Raspberry Pis communicate.

It became an exploration of something much more human.

MQTT gave us the technical infrastructure to send information between devices.

But the interesting question was not:

> **Can we send a message?**

We already know we can.

The interesting question was:

> **What should a message feel like when it arrives?**

A text message is visual.

A phone call is auditory.

A hug is physical.

Our project sits somewhere in between.

We are interested in the possibility that connected devices don't always have to make communication faster, more efficient, or more productive.

Sometimes they can simply make a person feel:

**"Someone is there."**

Even if that someone is several devices, a network broker, and a tiny Raspberry Pi away.

---

# 13. Evidence

### Hardware

- [ ] Raspberry Pi 1 photo
- [ ] Raspberry Pi 2 photo
- [ ] Raspberry Pi 3 photo
- [ ] Sensor photo
- [ ] OLED photo
- [ ] Speaker photo

### Software

- [ ] MQTT message screenshot
- [ ] OLED output screenshot/photo
- [ ] Terminal showing MQTT subscriber
- [ ] Code snippets

### User testing

- [ ] Participant 1 photo/video
- [ ] Participant 2 photo/video
- [ ] Participant observations
- [ ] Participant feedback

### Design

- [ ] Architecture diagram
- [ ] Final system diagram
- [ ] Photos of final setup

---

# The Big Idea

**Three Raspberry Pis.  
One invisible network.  
A few sensors.  
A tiny harp.  
And a question about what it means to feel close to someone when they're far away.**

That is our distributed interaction.
## Part A: MQTT Messaging

MQTT = lightweight messaging for IoT. Publish/subscribe model with central broker.

**Concepts:**
- **Broker**: `farlab.infosci.cornell.edu:1883`
- **Topic**: Like `IDD/bedroom/temperature` (use `#` wildcard)
- **Publish/Subscribe**: Send and receive messages

**Install MQTT tools on your Pi:**
```bash
sudo apt-get update
sudo apt-get install -y mosquitto-clients
```

**Test it:**

**Subscribe to messages (listener):**
```bash
mosquitto_sub -h farlab.infosci.cornell.edu -p 1883 -t 'IDD/#' -u idd -P 'device@theFarm'
```

**Publish a message (sender):**
```bash
mosquitto_pub -h farlab.infosci.cornell.edu -p 1883 -t 'IDD/test/yourname' -m 'Hello!' -u idd -P 'device@theFarm'
```

> **💡 Tips:**
> - Replace `yourname` with your actual name in the topic
> - Use single quotes around the password: `'device@theFarm'`
> - For your own projects, publish under your team's topic space: `IDD/<yourteam>/...` (for example `IDD/team3/bedroom/light`). Everyone shares one broker login, so anything you publish can reach everyone's projects.

**🔧 Debug Tool:** View all MQTT messages in real-time at `http://farlab.infosci.cornell.edu:5001`

![MQTT Explorer showing messages](imgs/MQTT-explorer.png)

**💡 Brainstorm 5 ideas for messaging between devices**

MQTT agrees on almost nothing in advance: you invent the topics and what the messages mean. Smart-home standards like Matter fix the vocabulary instead (every "light" behaves the same). Keep this trade-off in mind when you design your topics in Part C.

---

## Part B: Collaborative Pixel Grid

Each Pi = one pixel, controlled by RGB sensor, displayed in real-time grid.

**Architecture:** `Pi (sensor) → MQTT → Server → Web Browser`

**Setup:**

1. **Sensor**

#### Light/Proximity/Gesture sensor (APDS-9960)
We use this sensor [Adafruit APDS-9960](https://www.adafruit.com/product/3595) for this exmaple to detect light (also RGB)
 
<img src="https://cdn-shop.adafruit.com/970x728/3595-06.jpg" width=200>

Connect it to your pi with Qwiic connector


<img src="imgs/IMG_0270.jpg" height="200" />
We need to use the screen to display the color detection, so we need to stop the running piscreen.service to make your screen available again

```bash
# stop the screen service
sudo systemctl stop piscreen.service
```

if you want to restart the screen service
```bash
# start the screen service
sudo systemctl start piscreen.service
```
 
2. **Server** (one person on laptop):
```bash
cd "Lab 6"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-server.txt
python app.py
```

2. **View in browser:**
   - Grid: `http://farlab.infosci.cornell.edu:5000`
   - Controller: `http://farlab.infosci.cornell.edu:5000/controller`

3. **Pi publisher** (everyone on their Pi):
```bash
# First time setup - create virtual environment
cd "Lab 6"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-pi.txt

# Run the publisher
python pixel_grid_publisher.py
```

Hold colored objects near sensor to change your pixel!

![Pixel grid with two devices](imgs/two-devices-grid.png)




**Your README = story of what YOU built!**

---

Resources: [MQTT Guide](https://www.hivemq.com/mqtt-essentials/) | [Paho Python](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php) | [Flask-SocketIO](https://flask-socketio.readthedocs.io/)
